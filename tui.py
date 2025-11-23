#!/usr/bin/env python3

import sys
import time
import os

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.terminal_theme import MONOKAI

from watcher import start_watcher, event_queue

simple = False
export = True

console = Console(record=export)

watch_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
if not os.path.isdir(watch_path):
    print(f"Error: '{watch_path}' is not a valid directory.")
    sys.exit(1)
observer = start_watcher(watch_path)

events = []


def next_log_name():
    i = 1
    while True:
        name = f"watcher_log_{i}.html"
        if not os.path.exists(name):
            return name
        i += 1


def render(events):
    table = Table(
        title=f"Now watching: {watch_path}",
        title_style="bold green",
        min_width=200
    )
    table.add_column("Action")
    table.add_column("File")
    if (not simple):
        table.add_column("Is Synthetic")
    table.add_column("Timestamp")
    if (not simple):
        table.add_column("Destination Folder")

    for e, ts in reversed(events[-30:]):
        action = e.event_type
        style = (
            "green" if action == "created" else
            "red" if action == "deleted" else
            "blue" if action == "moved" else
            "yellow"
        )

        rel_path = os.path.relpath(e.src_path, watch_path)

        table.add_row(
            f"[{style}]{action}[/]",
            rel_path,
            *([str(e.is_synthetic)] if not simple else []),
            ts,
            *([os.path.dirname(os.path.relpath(e.dest_path, watch_path))] if not simple and hasattr(e, 'dest_path') and e.dest_path else []))

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
        if export:
            filename = next_log_name()
            console.print(render(events))
            console.save_html(filename, theme=MONOKAI)
            print(f"\nLog saved to {filename}")
        observer.stop()


observer.join()
