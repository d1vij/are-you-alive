#!./.venv/bin/python3

# A simple script which checks if a server is up or not (online and reachable)
# by initiating a tcp connection to the given port
# Displays notification if running on termux and termux-api is installed
# Otherwise prints results to a log file present at ~/who-all-are-alive.yaml
# or "./who-all-are-alive.yaml" (if no home directory found)
# I recommend running this python file as a cron-job on termux
# Configure the hosts and their respective port in config.yaml

import yaml
import shutil
import asyncio
import warnings
import subprocess
from os import path
from datetime import datetime

# Seconds after which to timeout tcp connection
TIMEOUT_S = 2
# Name of file where the status yaml would be dumped in case of absence of termux-notification API
OUT_FILENAME = "who-all-are-alive.yaml"

# Yaml file defining the hosts to ping
CONFIG_PATH = path.join(path.dirname(__file__), "config.yaml")

async def ping_server(host: str, port: str, timeout_s: float):
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout_s
        )
        writer.close()
        await writer.wait_closed()
        return True  # Ping to server successfull
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False  # Unable to ping server


def termux_notify(statuses: dict[str, bool]):

    if shutil.which("termux-notification") is None:
        warnings.warn(
            f"No termux-notification command found!! Writing to ~/{OUT_FILENAME}"
        )

        if (home := path.expanduser("~")) == "~":
            # Could not expand home path
            warnings.warn(
                f"Could not resolve $HOME path, defaulting to write to this script's root directory!!"
            )
            outPath = path.join(path.dirname(__file__), OUT_FILENAME)
        else:
            outPath = path.join(home, OUT_FILENAME)

        with open(outPath, "w") as file:
            yaml.dump(statuses, file)
        return


    NOTIFICATION_ID = "are_you_alive_status_update"
    NOTIFICATION_TITLE = "Who all are alive??"
    NOTIFICATION_ICON = "favorite"
    NOTIFICATION_BUTTON1_TEXT = "Check Again"

    script_dir = path.dirname(path.abspath(__file__))
    venv_python = path.join(script_dir, ".venv/bin/python3")
    script = path.abspath(__file__)
    NOTIFICATION_BUTTON1_ACTION = f"{venv_python} {script} "

    NOTIFICATION_CONTENT = "\n".join(
        f"{service} is {("alive" if status else "dead")}" for (service, status) in statuses.items()
    )
    NOTIFICATION_CONTENT += f"\n Checked at {datetime.now().strftime("%H:%M:%S")}"    

    # stdout for logging (if done in crontab)
    print(NOTIFICATION_CONTENT)

    # Displaying the notification in android
    subprocess.run([
        "termux-notification",
        "-t", NOTIFICATION_TITLE,
        "-c", f"{NOTIFICATION_CONTENT}",
        "--id", NOTIFICATION_ID,
        "--icon", NOTIFICATION_ICON,
        "--button1", NOTIFICATION_BUTTON1_TEXT,
        "--button1-action", NOTIFICATION_BUTTON1_ACTION,
        "--ongoing"
    ])

async def main():
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise RuntimeError("No config loaded!!")

    pings = []

    for name, C in config.items():

        host = C.get("host", None)
        port = C.get("port", None)

        if host is None:
            raise KeyError("No host provided for service " + name)
        if port is None:
            raise KeyError("No port provided for service " + name)

        if host.startswith("https://") or host.startswith("http://"):
            raise ValueError(
                'Hostnames cannot have protocol details in them.\nThat is use "example.com" instead of "https://example.com".'
            )
        pings.append(ping_server(host, port, TIMEOUT_S))

    statuses = {
        name: status
        for (name, status) in zip(config.keys(), await asyncio.gather(*pings))
    }
    termux_notify(statuses)


if __name__ == "__main__":
    asyncio.run(main())
