import random

def is_prime(n):
    print("made an edit to this file so another snapshot and stage should appear since the hash should be different")
    print("anddd....another")
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

for num in range(1, 101):
    if is_prime(num):
        print(f"{num} - {random.randint(1, 100)}")
    else:
        print(num)