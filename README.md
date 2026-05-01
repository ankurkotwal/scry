# scry

A one-line system status dashboard for your terminal — like the byobu status bar, but as a standalone CLI you can drop into tmux, your shell prompt, a status bar, or anything that takes a string.

The name *scry* means "to see at a glance" — exactly what a status line is for.

## What it shows

By default, in this order:

```
uptime | temperature | load | cpufreq | ram | disk | timestamp
```

Example output:

```
15h43m | 34°C | 1.27 | 4.1GHz | 15.3GB 21% | 219GB 95% | 2026-05-01 12:21:11
```

| Segment | Source |
|---|---|
| `uptime` | `/proc/uptime` |
| `temperature` | `/sys/class/hwmon/hwmon*/temp*_input`, falling back to `/sys/class/thermal/thermal_zone*/temp` |
| `load` | `/proc/loadavg` (1-minute average) |
| `cpufreq` | `/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`, falling back to `/proc/cpuinfo` |
| `ram` | `/proc/meminfo` (`MemTotal` − `MemAvailable`) |
| `disk` | `os.statvfs()` on the configured mount |
| `timestamp` | `datetime.strftime` with the configured format |

These are the same data sources [byobu](https://byobu.org) uses, read directly — no `df`, `free`, `uptime`, or `sensors` subprocess. Pure Python stdlib, zero dependencies.

## Install

```sh
pip install -e .
```

Or run without installing:

```sh
python -m scry
```

## Usage

```sh
scry                                       # default order, auto color
scry --segments=timestamp,load,ram         # custom order and subset
scry --disk=/home                          # different mount for disk segment
scry --time-format='%H:%M'                 # 24h clock only
scry --separator=' • '                     # custom separator
scry --color=never                         # disable ANSI colors
```

Run `scry --help` for the full flag list.

## Integrating into a status bar

**tmux** — refresh every 2 seconds:

```tmux
set -g status-interval 2
set -g status-right "#(scry --color=never)"
```

**Shell prompt (bash/zsh/fish)** — call it from your prompt function:

```sh
scry --segments=load,ram,timestamp --color=never
```

## Requirements

- Python ≥ 3.10
- Linux (reads from `/proc` and `/sys`)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
