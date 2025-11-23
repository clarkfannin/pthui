#!/usr/bin/env python3

import sys
import time
import os

from rich.console import Console
from rich.live import Live
from rich.table import Table
from watcher import start_watcher, event_queue

console = Console()

watch_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
if not os.path.isdir(watch_path):
    print(f"Error: '{watch_path}' is not a valid directory.")
    sys.exit(1)
observer = start_watcher(watch_path)

events = []


def render(events):
    table = Table(
        title=f"Now watching: {watch_path}",
        title_style="bold green",
        min_width=80
    )
    table.add_column("Action")
    table.add_column("File")
    table.add_column("Timestamp")

    for e, ts in events[-30:]:
        action = e.event_type
        style = (
            "green" if action == "created" else
            "red" if action == "deleted" else
            "blue" if action == "moved" else
            "yellow"
        )
        table.add_row(
            f"[{style}]{action}[/]",
            e.src_path.rsplit('/', 1)[-1],
            ts
        )

    return table


with Live(render(events), refresh_per_second=10) as live:
    try:
        while True:
            try:
                evt = event_queue.get_nowait()
                events.append(evt)
            except:
                pass

            live.update(render(events))
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()

observer.join()
