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

| Segment | Linux | macOS |
|---|---|---|
| `uptime` | `/proc/uptime` | `sysctl -n kern.boottime` |
| `temperature` | `/sys/class/hwmon/...`, falling back to `/sys/class/thermal/...` | *unavailable without sudo or a third-party tool — segment skipped* |
| `load` | `/proc/loadavg` | `sysctl -n vm.loadavg` |
| `cpufreq` | `/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`, falling back to `/proc/cpuinfo` | `sysctl -n hw.cpufrequency` (Intel only — Apple Silicon has no fixed clock; segment skipped) |
| `ram` | `/proc/meminfo` (`MemTotal` − `MemAvailable`) | `sysctl -n hw.memsize` + `vm_stat` |
| `disk` | `df -P -k` on the configured mount | same |
| `timestamp` | `date(1)` with the configured format | same |

These are the same data sources [byobu](https://byobu.org) uses. `scry` is a single POSIX shell script — no runtime, no dependencies beyond standard Unix utilities (`awk`, `df`, `date`, `tr`, plus `sysctl`/`vm_stat` on macOS).

## Install

Via Homebrew (macOS or Linux):

```sh
brew install ankurkotwal/scry/scry
```

Or copy the script anywhere on your `$PATH`:

```sh
install -m 755 scry /usr/local/bin/scry
```

Or run it in place:

```sh
./scry
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

**zellij** — zellij's built-in status bar can't take a custom command, so the easiest path is the [zjstatus](https://github.com/dj95/zjstatus) plugin. Configure it with `command_scry_command "scry --color=always"` and reference `{command_scry}` in your `format_right`.

## Requirements

- POSIX shell (`/bin/sh`)
- `awk`, `df`, `date`, `tr` (any standard coreutils install)
- Linux (`/proc`, `/sys`) **or** macOS (`sysctl`, `vm_stat`)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
