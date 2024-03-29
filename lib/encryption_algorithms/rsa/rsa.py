import random


def get_primes(start, stop):
    if start >= stop:
        return []

    primes = [2]

    for n in range(3, stop + 1, 2):
        for p in primes:
            if n % p == 0:
                break
        else:
            primes.append(n)

    while primes and primes[0] < start:
        del primes[0]

    return primes


def are_relatively_prime(a, b):

    for n in range(2, min(a, b) + 1):
        if a % n == b % n == 0:
            return False
    return True


def make_key_pair(length):

    if length < 4:
        raise ValueError('cannot generate a key of length less '
                         'than 4 (got {!r})'.format(length))

    n_min = 1 << (length - 1)
    n_max = (1 << length) - 1

    start = 1 << (length // 2 - 1)
    stop = 1 << (length // 2 + 1)
    primes = get_primes(start, stop)

    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_candidates = [q for q in primes
                        if n_min <= p * q <= n_max]
        if q_candidates:
            q = random.choice(q_candidates)
            break
    else:
        raise AssertionError("cannot find 'p' and 'q' for a key of "
                             "length={!r}".format(length))

    stop = (p - 1) * (q - 1)
    for e in range(3, stop, 2):
        if are_relatively_prime(e, stop):
            break
    else:
        raise AssertionError("cannot find 'e' with p={!r} "
                             "and q={!r}".format(p, q))

    for d in range(3, stop, 2):
        if d * e % stop == 1:
            break
    else:
        raise AssertionError("cannot find 'd' with p={!r}, q={!r} "
                             "and e={!r}".format(p, q, e))

    # That's all. We can build and return the public and private keys.
    return p * q, e, d


def encrypt(data, e, n):

    if isinstance(data, str):
        data = data.encode('ascii')

    encrypted_data = []
    for byte in data:
        encrypted_data.append(pow(byte, e, n))

    print(encrypted_data)

    return encrypted_data


def decrypt(data, d, n):
    decrypted_data = []

    for byte in data:
        decrypted_data.append(pow(byte, d, n))

    print(decrypted_data)

    return bytes(decrypted_data).decode("utf8")


def main():

    with open("uu.py", "r") as file:

        data = file.read()

        print(data)

        n, e, d = make_key_pair(9)

        print (n, ' ', e, ' ', d)

        encrypted_data = encrypt(data, e, n)

        decrypted_data = decrypt(encrypted_data, d, n)
        print(decrypted_data)


if __name__ == '__main__':
    main()