import random


# This is main function that is connected to the Test button. You don't need to touch it.
def prime_test(N, k):
    return fermat(N, k), miller_rabin(N, k)


# You will need to implement this function and change the return value.
def mod_exp(x, y, N):
    if y == 0:
        return 1
    z = mod_exp(x, y // 2, N)
    if y % 2 == 0:
        return pow(z, 2) % N
    else:
        return x * pow(z, 2) % N


# You will need to implement this function and change the return value.   
def fprobability(k):
    return 1 - pow(.5, k)


# You will need to implement this function and change the return value.   
def mprobability(k):
    return 1 - pow(.25, k)


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low,hi) which gives a random integer between low and
# hi, inclusive.
def fermat(N, k):
    # generate a set of k unique random numbers with a value between 2 and N - 1
    randNums = []
    while len(randNums) < k:
        randNum = random.randint(2, N - 1)
        if randNum not in randNums:
            randNums.append(randNum)

    # if a^(N-1) mod N = 1, then maybe it's prime, but if not, it's not prime
    for a in randNums:
        if mod_exp(a, N - 1, N) == 1:
            continue
        else:
            return "composite"
    return "prime"


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low,hi) which gives a random integer between low and
#  hi, inclusive.
def miller_rabin(N, k):
    # base cases of n < 3
    if N == (2 | 3):
        return 'prime'
    if N % 2 == 0:
        return 'composite'

    # generate a set of k unique random numbers with a value between 2 and N - 1
    randNums = []
    while len(randNums) < k:
        randNum = random.randint(2, N - 1)
        if randNum not in randNums:
            randNums.append(randNum)

    # find r and d such that d is odd and d*2r = N - 1
    r = 0
    d = N - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for a in randNums:
        x = mod_exp(a, d, N)
        if x == 1 or x == N - 1:
            continue
        for i in range(r - 1):
            x = mod_exp(x, 2, N)
            if x == N - 1:
                break
        else:
            return 'composite'
    return 'prime'
