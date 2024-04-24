from gomoku import *
from random import randint, choice, shuffle
import os


location = os.path.dirname(__file__)

with open(os.path.join(location, "cases.txt"), "w") as f:
    for i in range(10):
        # Params in detect_rows
        f.write(f"{choice(['b', 'w'])}{randint(2, 8)},")

        # Elements in array
        s = list("b"*randint(8, 16) + "w"*randint(8, 16) + " "*randint(8, 16))
        for i in range(8):
            shuffle(s)
            f.write("".join(s[:8]))

        f.write("\n")
