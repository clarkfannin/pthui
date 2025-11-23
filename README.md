# pthui

## Description

pthui is a neat, color-coded tui wrapper for watchdog. Install it globally and use it from anywhere!

## Prerequisites

Make sure you have Python, [watchdog](https://pypi.org/project/watchdog/) and [rich](https://pypi.org/project/rich/) installed:

```bash
pip install rich watchdog
```

## Installing globally

To run the script from anywhere:

1. Clone the repo:

```bash
git clone https://github.com/clarkfannin/pthui
```

2. Make `tui.py` executable:

```bash
chmod +x /path/to/tui.py
```

3. Create a symlink in a folder that's in your `PATH`:

```bash
sudo ln -s /path/to/tui.py /usr/local/bin/watch # optional: replace 'watch'
```

After that, you can run:

```bash
watch                # watches the current folder
watch /some/folder   # watches a specific folder
```
