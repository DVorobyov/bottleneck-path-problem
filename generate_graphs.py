import random

for i in range(10, 10000, 10):
    with open(f"./graphs/graph_{i}.dot", "w") as f:
        for j in range(i):
            for k in range(j+1, i):
                print(f"{j} {k} {random.randint(1, 100)}", file=f)