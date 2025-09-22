#!/usr/bin/env python3
import sys
import re
from collections import Counter
import click

IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def aggregate_ips(lines, strict=False):
    """
    Given an iterable of text lines, return a Counter of IPv4 occurrences.
    If strict=True, only counts IPs with octets 0–255.
    """
    counts = Counter()
    for line in lines:
        for ip in IPV4_PATTERN.findall(line):
            if strict:
                parts = ip.split(".")
                try:
                    if all(0 <= int(o) <= 255 for o in parts):
                        counts[ip] += 1
                except ValueError:
                    # non-integer octet (shouldn't happen with the regex, but safe)
                    continue
            else:
                counts[ip] += 1
    return counts


@click.command()
@click.option("--file", "-f", type=click.File("r"), help="Read logs from a file instead of stdin.")
@click.option("--top", type=int, default=0, show_default=True, help="Show only the top N IPs (0 = all).")
@click.option("--sort", type=click.Choice(["count", "ip"], case_sensitive=False), default="count", show_default=True, help="Sort by count (desc) or IP (asc).")
@click.option("--strict/--no-strict", default=False, show_default=True, help="Validate 0–255 octets.")
def count_ips(file, top, sort, strict):
    source = file if file else sys.stdin
    counts = aggregate_ips(source, strict=strict)

    if not counts:
        return

    items = list(counts.items())
    if sort == "count":
        items.sort(key=lambda kv: (-kv[1], kv[0]))
    else:
        items.sort(key=lambda kv: kv[0])

    if top and top > 0:
        items = items[:top]

    for ip, cnt in items:
        click.echo(f"{cnt} {ip}")


if __name__ == "__main__":
    count_ips()
