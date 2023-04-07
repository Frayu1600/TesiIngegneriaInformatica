class point:
    def __init__(self, x = 'O', y = 'O'):
        self.x = x
        self.y = y

    def is_punto_infinito(self):
        return (str(self)) == 'O'

    def __str__(self):
        if self.x == 'O' and self.y == 'O': return f'O'
        else: return f'({self.x}, {self.y})'

class prime_elliptic_curve:
    def __init__(self, p:int, a:int, b:int, G:point, name: str):
        self.a = a
        self.b = b
        self.p = p 
        self.G = G
        self.keysize = len(bin(p)[2:])
        self.name = name

# CURVE A DISPOSIZIONE
# y^2 = x^3 + ax + b mod p
# prese da https://neuromancer.sk/std/ (NIST)

P192 = prime_elliptic_curve(
    p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff,
    a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc,
    b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1,
    G = point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811), 
    name = "P-192" 
)

P224 = prime_elliptic_curve(
    p = 0xffffffffffffffffffffffffffffffff000000000000000000000001,
    a = 0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe,
    b = 0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4,
    G = point(0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21, 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34),
    name = "P-224",
)

P256 = prime_elliptic_curve(
    p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
    b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    G = point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5),
    name = "P-256" 
)

P384 = prime_elliptic_curve(
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff,
    a = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000fffffffc,
    b = 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef,
    G = point(0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7, 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f),
    name = "P-384" 
)

P521 = prime_elliptic_curve(
    p = 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
    a = 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc,
    b = 0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00,
    G = point(0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66, 0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650),
    name = "P-521" 
)

# algoritmo di euclide esteso
# risolve l'identità di Bézout ax + by = gcd(a,b) 
# ritorna gcd(a,b), x, y
def EE(a: int, b: int):
    if b == 0: 
        return [a,1,0]

    d_, x_, y_ = EE(b, a % b)
    
    dxy = [d_, y_, x_ - a//b * y_]
    return dxy 

# calcola l'inverso moltiplicativo di a mod b 
# cioè risolve l'equazione x = a^-1 mod b
# a, b devono essere coprimi!
def inverso_moltiplicativo(a: int, b: int):
    gcdab, x, y = EE(a, b)
    if gcdab != 1:
        print(f'ERRORE: non posso calcolare l\'inverso moltiplicativo di {a} mod {b} poichè {a} e {b} non sono coprimi!')
        return 0
    else: return x

# controlla che il punto P appartenga alla curva ellittica prima Ep(a,b)
def appartiene_alla_curva(P: point, curva_ellittica:prime_elliptic_curve):
    if P.is_punto_infinito(): return True

    cubica = (pow(P.x, 3) + curva_ellittica.a * P.x + curva_ellittica.b) % curva_ellittica.p

    ysquared = pow(P.y, 2, curva_ellittica.p)

    if ysquared == cubica: 
        P.x %= curva_ellittica.p
        return True 
    return False

# algoritmo tonelli-shanks per il calcolo della radice in modulo p
# source: https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
def modular_sqrt(a: int, p: int):

    def legendre_symbol(a: int, p: int):
        """ Compute the Legendre symbol a|p using
            Euler's criterion. p is a prime, a is
            relatively prime to p (if p divides
            a, then a|p = 0)
            Returns 1 if a has a square root modulo
            p, -1 otherwise.
        """
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.
        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.
        0 is returned is no square root exists for
        these a and p.
        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

# verifica che x sia un residuo quadratico e le calcola la radice in modulo p
# ritorna int(0) se non ammette radice nel campo
def eval_cubica(x:int, curva_ellittica:prime_elliptic_curve):
    ysquared = (pow(x, 3) + curva_ellittica.a * x + curva_ellittica.b) % curva_ellittica.p
    
    return modular_sqrt(ysquared, curva_ellittica.p)

# calcola S = P + Q 
# accetta due point e ritorna un point
# la somma la effettua in una curva elitticha prima Ep(a,b)
# gestisce il caso se il punto è il punto all'infinito
def somma_di_punti(P: point, Q: point, curva_ellittica:prime_elliptic_curve):
    if curva_ellittica.p < -1 or curva_ellittica.p == 0:
        print(f'ERRORE: non posso fare la somma con p negativo o uguale a zero!')
        return -1

    S = point()
    
    if appartiene_alla_curva(P, curva_ellittica) == False:
        print(f'ERRORE: il punto P = {P} non appartiene alla curva ellittica specificata!')
        return -1 
    
    if appartiene_alla_curva(Q, curva_ellittica) == False:
        print(f'ERRORE: il punto Q = {Q} non appartiene alla curva ellittica specificata!')
        return -1
    
    if Q.is_punto_infinito(): 
        return P 

    if P.is_punto_infinito():
        return Q

    # caso in cui P = -Q
    if curva_ellittica.p - P.y == Q.y: 
        return S

    if P.x == Q.x and P.y == Q.y: 
        lambdaa = ((3 * (P.x ** 2) + curva_ellittica.a) * inverso_moltiplicativo(2 * P.y, curva_ellittica.p)) % curva_ellittica.p
    else: 
        lambdaa = ((Q.y - P.y) * inverso_moltiplicativo(Q.x - P.x, curva_ellittica.p)) % curva_ellittica.p 

    S.x = lambdaa ** 2 - P.x - Q.x
    S.x %= curva_ellittica.p
    
    S.y = -Q.y + lambdaa * (Q.x - S.x)
    S.y %= curva_ellittica.p
    
    return S 

# calcola Q = kP ove P appartiene alla curva ellittica prima Ep(a,b)
def raddoppi_ripetuti(P: point, k: int, curva_ellittica:prime_elliptic_curve):
    if k <= 0:
        print(f'ERRORE: non posso fare i raddoppi se k <= 0')
        return -1

    if curva_ellittica.p <= 0:
        print(f'ERRORE: non posso fare i raddoppi se p <= 0')
        return -1
    
    if appartiene_alla_curva(P, curva_ellittica) == False:
        print(f'ERRORE: il punto P = {P} non appartiene alla curva ellittica specificata!')
        return -1 

    bink = bin(k)[::-1][:-2]
    maxk = len(bink) 
    points = [P]

    for i in range(1, maxk):
        new = somma_di_punti(points[-1], points[-1], curva_ellittica)
        points.append(new)        

    result = -1
    for i, digit in enumerate(bink):
        if(digit == '1'): 
            if result == -1: result = points[i]
            else: result = somma_di_punti(result, points[i], curva_ellittica)

    return result