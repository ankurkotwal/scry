from __future__ import annotations

import datetime as dt
import glob
import os


def uptime() -> str:
    with open("/proc/uptime") as f:
        secs = int(float(f.read().split()[0]))
    if secs >= 86400:
        return f"{secs // 86400}d{(secs % 86400) // 3600}h"
    if secs >= 3600:
        return f"{secs // 3600}h{(secs % 3600) // 60}m"
    if secs >= 60:
        return f"{secs // 60}m"
    return f"{secs}s"


def temperature() -> str:
    candidates = (
        glob.glob("/sys/class/hwmon/hwmon*/temp*_input")
        + glob.glob("/sys/class/hwmon/hwmon*/device/temp*_input")
        + glob.glob("/sys/class/thermal/thermal_zone*/temp")
    )
    for path in candidates:
        try:
            with open(path) as f:
                millidegrees = int(f.read().strip())
        except (OSError, ValueError):
            continue
        if millidegrees > 0:
            return f"{millidegrees // 1000}°C"
    return ""


def load() -> str:
    with open("/proc/loadavg") as f:
        return f.read().split()[0]


def cpufreq() -> str:
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as f:
            khz = int(f.read().strip())
        return f"{khz / 1_000_000:.1f}GHz"
    except OSError:
        pass
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("cpu MHz"):
                    mhz = float(line.split(":", 1)[1].strip())
                    return f"{mhz / 1000:.1f}GHz"
    except OSError:
        pass
    return ""


def ram() -> str:
    info: dict[str, int] = {}
    with open("/proc/meminfo") as f:
        for line in f:
            tok, _, rest = line.partition(":")
            if tok in ("MemTotal", "MemAvailable"):
                info[tok] = int(rest.strip().split()[0])  # kB
                if len(info) == 2:
                    break
    total_kb = info["MemTotal"]
    used_kb = total_kb - info["MemAvailable"]
    pct = round(100 * used_kb / total_kb)
    if total_kb >= 1_048_576:
        total_str = f"{total_kb / 1_048_576:.1f}GB"
    else:
        total_str = f"{total_kb // 1024}MB"
    return f"{total_str} {pct}%"


def disk(mount: str = "/") -> str:
    s = os.statvfs(mount)
    total = s.f_blocks * s.f_frsize
    free = s.f_bavail * s.f_frsize
    used = total - free
    pct = round(100 * used / total) if total else 0
    if total >= 1024**4:
        size = f"{total / 1024**4:.1f}TB"
    elif total >= 1024**3:
        size = f"{total / 1024**3:.0f}GB"
    else:
        size = f"{total / 1024**2:.0f}MB"
    return f"{size} {pct}%"


def timestamp(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return dt.datetime.now().strftime(fmt)
