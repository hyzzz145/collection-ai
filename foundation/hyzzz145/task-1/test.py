import random, time, sys

def lucky_bar(prob, label="事件", width=40, duration=0.8, fps=40):
    hit = random.random() <= prob
    green = max(1, round(prob * width))
    target = random.randint(0, green - 1) if hit else random.randint(green, width - 1)

    total = int(duration * fps)
    for i in range(total + 1):
        t = i / total
        if i == total:
            pos = target
        else:
            amp = (width / 2) * (1 - t) ** 2
            pos = int(target + amp * random.uniform(-1, 1))
            pos = max(0, min(width - 1, pos))

        bar = "█" * green + "░" * (width - green)
        line = list(" " * width)
        line[pos] = "▲"
        sys.stdout.write(f"\r  [{bar}]\n\r  {''.join(line)}\033[1A")
        sys.stdout.flush()
        time.sleep(1 / fps)

    sys.stdout.write(f"\r  [{bar}]\n\r  {''.join(line)}\n")
    print(f"  {'✨ 命中' if hit else '✖ 未中'}：{label}")
    return hit

print(lucky_bar(0.3,"事件"))