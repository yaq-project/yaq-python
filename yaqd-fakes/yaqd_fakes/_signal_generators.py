"""Generators for fake sensor signal generation."""


import random


def random_walk(min_, max_):
    # A random walk with weight. Will be held to the center of the dynamic range.
    center = (max_ + min_) / 2
    width = (max_ - min_) * 10
    val = center
    while True:
        yield val
        step = random.gauss(mu=0, sigma=(max_ - min_) / 25)
        step += (center - val) / width
        val += step
        # clip
        val = max(val, min_)
        val = min(val, max_)
