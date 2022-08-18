import time, random, hashlib
start = time.clock()
while True:
    nonce = random.randint(1,10**32)
    h = hashlib.sha256(str(nonce).encode('utf-8')).hexdigest()
    if h<"00000f0000000000000000000000000000000000000000000000000000000000":
        print(h)
        print(nonce)
        end = time.clock()
        print(end - start)
        break
