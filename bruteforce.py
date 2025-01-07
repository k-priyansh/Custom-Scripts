import itertools

passwords = itertools.product("abc123", repeat=4)
target_password = "abc1"

for attempt in passwords:
    attempt = ''.join(attempt)
    print(f"Trying: {attempt}")
    if attempt == target_password:
        print(f"Password found: {attempt}")
        break