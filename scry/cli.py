from __future__ import annotations

import argparse
import sys

from . import segments

DEFAULT_ORDER = ("uptime", "temperature", "load", "cpufreq", "ram", "disk", "timestamp")

SEGMENT_COLORS = {
    "uptime": "\033[1;37m",
    "temperature": "\033[1;33m",
    "load": "\033[33m",
    "cpufreq": "\033[1;36m",
    "ram": "\033[1;32m",
    "disk": "\033[1;35m",
    "timestamp": "\033[37m",
}
RESET = "\033[0m"


def _render(name: str, disk_mount: str, time_fmt: str) -> str:
    if name == "uptime":
        return segments.uptime()
    if name == "temperature":
        return segments.temperature()
    if name == "load":
        return segments.load()
    if name == "cpufreq":
        return segments.cpufreq()
    if name == "ram":
        return segments.ram()
    if name == "disk":
        return segments.disk(disk_mount)
    if name == "timestamp":
        return segments.timestamp(time_fmt)
    raise ValueError(f"unknown segment: {name!r}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="scry", description="One-line system status dashboard.")
    p.add_argument(
        "--segments",
        default=",".join(DEFAULT_ORDER),
        help=f"Comma-separated segment order (default: {','.join(DEFAULT_ORDER)}).",
    )
    p.add_argument("--disk", default="/", help="Mount point for the disk segment (default: /).")
    p.add_argument(
        "--time-format",
        default="%Y-%m-%d %H:%M:%S",
        help="strftime format for the timestamp segment (default: %%Y-%%m-%%d %%H:%%M:%%S).",
    )
    p.add_argument("--separator", default=" | ", help="Separator between segments.")
    p.add_argument(
        "--color",
        choices=("auto", "always", "never"),
        default="auto",
        help="Colorize output (default: auto).",
    )
    args = p.parse_args(argv)

    use_color = args.color == "always" or (args.color == "auto" and sys.stdout.isatty())

    parts: list[str] = []
    for name in (s.strip() for s in args.segments.split(",") if s.strip()):
        try:
            value = _render(name, args.disk, args.time_format)
        except ValueError as e:
            print(f"scry: {e}", file=sys.stderr)
            return 2
        if not value:
            continue
        if use_color and name in SEGMENT_COLORS:
            value = f"{SEGMENT_COLORS[name]}{value}{RESET}"
        parts.append(value)
    print(args.separator.join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
