import math
import time


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"


def progress_bar(current, total, start_time):
    percent = current * 100 / total
    speed = current / (time.time() - start_time + 1e-9)
    elapsed = time.time() - start_time
    eta = (total - current) / speed if speed > 0 else 0

    bar_len = 20
    filled_len = int(bar_len * percent // 100)
    bar = '█' * filled_len + '-' * (bar_len - filled_len)

    progress = (
        f"[{bar}] {percent:.2f}%\n"
        f"📥 {format_bytes(current)} / {format_bytes(total)}\n"
        f"⚡ Speed: {format_bytes(speed)}/s\n"
        f"⏳ Elapsed: {time_formatter(elapsed)} | ETA: {time_formatter(eta)}"
    )
    return progress


def time_formatter(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    elif m:
        return f"{m}m {s}s"
    else:
        return f"{s}s"
