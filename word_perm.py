
def int2base(number,base):
    result = []
    while number > 0:
        result = [number % base] + result
        number /= base
    return result

def base2int(number,base):
    result = 0
    value = 1
    for digit in reversed(number):
        result+=digit*value
        value*=base
    
    return result

def word_permuter(alph_size, perm, word_length):
    # las perm son listas de [0...alph_size-1]
    def word_perm(index):
        result = int2base(index,alph_size)
        result = ((word_length - len(result)) * [0]) + result
        result = [perm[x] for x in result]
        return base2int(result,alph_size)
    return word_perm


def hit_p(T,H,perm):
    B_i = 0
    B_f = len(H[0])+1
    S 
