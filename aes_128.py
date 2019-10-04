import aes_math

def key_initialise(inp):
    key = []
    explode = {}
    keys = {}

    for byte in inp:
        key.append(int(byte.encode("hex"), 16))

    w0, w1, w2, w3 = [], [], [], []

    for i in xrange(4):
        w0.append(key[i])
    for i in xrange(4):
        w1.append(key[i+4])
    for i in xrange(4):
        w2.append(key[i+8])
    for i in xrange(4):
        w3.append(key[i+12])

    explode['0'] = w0
    explode['1'] = w1
    explode['2'] = w2
    explode['3'] = w3

    keys['0'] = []

    for i in w0:
        keys['0'].append(i)
    for i in w1:
        keys['0'].append(i)
    for i in w2:
        keys['0'].append(i)
    for i in w3:
        keys['0'].append(i)

    i = 4
    pop = 0
    rcon = [1, 0, 0, 0]

    while i < 44:
        temp = []
        temp_2 = []

        for l in explode[str(i - 1)]:
            temp.append(l)

        for m in explode[str(i - 4)]:
            temp_2.append(m)
    
        if i % 4 == 0:
            k = 0

            pop = temp[0]
            temp[0] = sub_bytes(temp[1])
            temp[1] = sub_bytes(temp[2])
            temp[2] = sub_bytes(temp[3])
            temp[3] = sub_bytes(pop)

            if i < 35:
                rcon[0] = rcon[0] << (i/4 - 1)
            elif i == 36:
                rcon[0] = 0x1b
            elif i == 40:
                rcon[0] = 0x36

            combined = [rcon[0] ^ temp[0], temp[1], temp[2], temp[3]]
            
            wi = []

            for k in xrange(4):
                wi.append(combined[k] ^ explode[str(i - 4)][k])
                k += 1

            explode[str(i)] = wi

            rcon[0] = 1

        else:

            wi = [temp[0] ^ temp_2[0],
                  temp[1] ^ temp_2[1],
                  temp[2] ^ temp_2[2],
                  temp[3] ^ temp_2[3]]

            explode[str(i)] = wi

        i += 1
        
    for fig in xrange(11):
        if fig != 0:
            keys[str(fig)] = []

            for thing in explode[str(4 * fig + 0)]:
                keys[str(fig)].append(thing)
            for thing in explode[str(4 * fig + 1)]:
                keys[str(fig)].append(thing)
            for thing in explode[str(4 * fig + 2)]:
                keys[str(fig)].append(thing)
            for thing in explode[str(4 * fig + 3)]:
                keys[str(fig)].append(thing)

    return keys

def round_zero(plain, key):
    plain_exp = []
    key_exp = []

    for bit in plain:
        plain_exp.append(int(bit.encode("hex"), 16))
    for bit in key:
        key_exp.append(int(bit.encode("hex"), 16))

    zero = []
    a = 0

    for i in xrange(16):
        zero.append(plain_exp[a] ^ key_exp[a])

        a += 1

    return zero


def state(i):
    matrix = [[i[0], i[4], i[8],  i[12]],
              [i[1], i[5], i[9],  i[13]],
              [i[2], i[6], i[10], i[14]],
              [i[3], i[7], i[11], i[15]]
             ]

    return matrix

def sub_bytes(inp):
    out = aes_math.multiplicative_inverse(inp)
    out = aes_math.affine_transformation(out)

    return out

def sub_state(inp):
    matrix = [[0, 0, 0, 0], 
              [0, 0, 0, 0], 
              [0, 0, 0, 0], 
              [0, 0, 0, 0]]

    x, y = 0, 0

    for i in xrange(4):
        y = 0
        for j in xrange(4):
            matrix[x][y] = sub_bytes(inp[x][y])
            y += 1
        x += 1

    return matrix

def shift_rows(inp):
    shifted = [[inp[0][0], inp[0][1], inp[0][2], inp[0][3]],
               [inp[1][1], inp[1][2], inp[1][3], inp[1][0]],
               [inp[2][2], inp[2][3], inp[2][0], inp[2][1]],
               [inp[3][3], inp[3][0], inp[3][1], inp[3][2]]]

    return shifted

def mix_columns(s):
    for c in xrange(4):
        s0p = aes_math.gf_mult(0x02, s[0][c]) ^ \
              aes_math.gf_mult(0x03, s[1][c]) ^ \
              s[2][c] ^ s[3][c]
        s1p = s[0][c] ^ aes_math.gf_mult(0x02, s[1][c]) ^ \
              aes_math.gf_mult(0x03, s[2][c]) ^ s[3][c]
        s2p = s[0][c] ^ s[1][c] ^ aes_math.gf_mult(0x02, s[2][c]) ^ \
              aes_math.gf_mult(0x03, s[3][c])
        s3p = aes_math.gf_mult(0x03, s[0][c]) ^ s[1][c] ^ s[2][c] ^ \
              aes_math.gf_mult(0x02, s[3][c])
        
        s[0][c] = s0p
        s[1][c] = s1p
        s[2][c] = s2p
        s[3][c] = s3p

    return s

def read_out(inp):
    reading = []

    for i in xrange(4):
        for j in xrange(4):
            reading.append(inp[j][i])

    return reading

def add_round_key(inp, key, rnd):
    added = []

    for i in xrange(16):
        added.append(inp[i] ^ key[str(rnd)][i])

    return added

def main():
    #base = raw_input("Base: ")
    #a = raw_input("Please define a: ")
    plain_file = open("plain", "rb")
    plain = plain_file.read(16)
    key_file = open("key", "rb")
    key = key_file.read(16)

    keys = key_initialise(key)

    st = round_zero(plain, key)

    rd = 1

    for i in xrange(9):
        st = state(st)
        st = sub_state(st)
        st = shift_rows(st)
        st = mix_columns(st)
        st = read_out(st)
        st = add_round_key(st, keys, rd)

        rd += 1

    st = state(st)
    st = sub_state(st)
    st = shift_rows(st)
    st = read_out(st)
    st = add_round_key(st, keys, 10)

    for item in st:
        print hex(item)

    out_put = open("output", "wb")
    for item in st:
        out_put.write(chr(item))

    out_put.close()


if __name__ == '__main__':
    main()