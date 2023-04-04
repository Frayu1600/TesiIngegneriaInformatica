import raddoppi_ripetuti
import point 
import EC_DRBG
import prime_elliptic_curve

# tonelli-shanks
# source: https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
def modular_sqrt(a, p):

    def legendre_symbol(a, p):
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

# verifica se la coordinata x ha associata una coordinata y, cioè se esiste un punto nella curva Ep(a,b) che ha coordinate (x,y)
def eval_cubica(x:int, a:int, b:int, p:int):
    ysquared = (pow(x, 3) + a * x + b) % p
    
    return modular_sqrt(ysquared, p)

# CURVE A DISPOSIZIONE
# y^2 = x^3 + ax + b mod p
# prese da https://neuromancer.sk/std/ (NIST)

P192 = prime_elliptic_curve.prime_elliptic_curve(
    0xfffffffffffffffffffffffffffffffeffffffffffffffff,
    0xfffffffffffffffffffffffffffffffefffffffffffffffc,
    0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1,
    point.point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811), 
    192,
    "P-192" 
)

P224 = prime_elliptic_curve.prime_elliptic_curve(
    0xffffffffffffffffffffffffffffffff000000000000000000000001,
    0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe,
    0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4,
    (0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21, 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34),
    224,
    "P-224",
)

P256 = prime_elliptic_curve.prime_elliptic_curve(
    0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
    0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
    (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5),
    256,
    "P-256" 
)

P384 = prime_elliptic_curve.prime_elliptic_curve(
    0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff,
    0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000fffffffc,
    0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef,
    (0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7, 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f),
    384,
    "P-384" 
)

P521 = prime_elliptic_curve.prime_elliptic_curve(
    0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
    0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc,
    0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00,
    (0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66, 0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650),
    521,
    "P-521" 
)

while(True):
    scelta = input("Scegliere la curva ellittica da impiegare sul DRBG (P-192, P-224, P-256, P-384, P-521): ")

    if(scelta == P192.name):
        curva_scelta = P192
        break
    elif(scelta == P224.name):
        curva_scelta = P224
        break
    elif(scelta == P256.name):
        curva_scelta = P256
        break
    elif(scelta == P384.name):
        curva_scelta = P384
        break
    elif(scelta == P521.name):
        curva_scelta = P521
        break
    else:
        print("Inserire una curva ellittica tra quelle elencate!\n")

# prendiamo Q pari al punto base G della curva per semplicità
Q = curva_scelta.G

# introduciamo la backdoor, cioè poniamo calcoliamo P = eQ
e = 0xdeadbeef
P = raddoppi_ripetuti.raddoppi_ripetuti(Q, e, curva_scelta.a, curva_scelta.b, curva_scelta.p)

# supponiamo che il generatore di cui vogliamo conoscere lo stato utilizzi P, Q con la backdoor (P = eQ)
generatore_sicurissimo = EC_DRBG.EC_DRBG(P, Q, curva_scelta)
# attenzione: non stiamo usando i P, Q dati dal NIST, poichè non sappiamo se ci sia veramente una relazione tra P, Q

# generiamo un pò di bit
niterazioni = 10
print(f"Eseguo {niterazioni} iterazioni dell'EC-DRBG...")
generatore_sicurissimo.generate_bits(niterazioni)

# supponiamo di ottenere i bit generati alla i-esima iterazione
ri = generatore_sicurissimo.generate_bits()
ri_plus_one = generatore_sicurissimo.generate_bits()

si_plus_one = 0

# applichiamo l'attacco shumow-ferguson e dimostriamo di saper generare correttamente i bit da qui in avanti
# conosciamo P, Q, a, b, p, e

# enumeriamo tutti i possibili rimanenti 16 bit più significativi che possono essere stati omessi e otteniamo i possibili punti della curva
# alla fine otterremo che circa la metà degli x ammettono radici nel campo
# è più veloce prima trovare gli R candidati (poichè sono 2^15 anzichè 2^16)
print(f"Cerco candidati punti R della curva {curva_scelta.name} da testare...")
candidatiR = []
for guess in range(0, pow(2, 16)):

    rix = int(bin(guess)[2:].zfill(16) + str(ri), 2)

    # se è un residuo quadratico, aggiungiamo alla lista
    riy = eval_cubica(rix, curva_scelta.a, curva_scelta.b, curva_scelta.p)
    if(riy != 0):
        candidato_R = point.point(rix, riy)
        candidatiR.append(candidato_R)

# ci sarà sicuramente il punto R relativo allo stato successivo, andiamo a controllare quale sia (alla peggio sono 2^15 iterazioni)
#i = 0
print(f"Verifico i candidati punti R della curva ellittica {curva_scelta.name}...")
for R in candidatiR:
    #print(f"verifico il candidato {i}")
    #i += 1
    possible_si_plus_one = raddoppi_ripetuti.raddoppi_ripetuti(R, e, curva_scelta.a, curva_scelta.b, curva_scelta.p).x

    possible_ri_plus_one = bin(raddoppi_ripetuti.raddoppi_ripetuti(Q, possible_si_plus_one, curva_scelta.a, curva_scelta.b, curva_scelta.p).x)[2:].zfill(curva_scelta.keysize)[16:]

    if(possible_ri_plus_one == ri_plus_one):
        si_plus_one = possible_si_plus_one
        print(f"Trovato lo stato successivo: s[i+1] = {si_plus_one}")    
        break

# P-256 con seed 0xdeadbeef e optional 0x0:
#next_state = 47207521221421821650194576114806312832850024674388177198523513678368120817067

print(f"\nVerifica iterazioni successive:")
print(f"\n-- iterazione i+2 --")

ri_plus_two_drbg = generatore_sicurissimo.generate_bits()
print(f"r[i+2] DRBG: {ri_plus_two_drbg}")

si_plus_two_attack = raddoppi_ripetuti.raddoppi_ripetuti(P, si_plus_one, curva_scelta.a, curva_scelta.b, curva_scelta.p).x
ri_plus_two_attack = bin(raddoppi_ripetuti.raddoppi_ripetuti(Q, si_plus_two_attack, curva_scelta.a, curva_scelta.b, curva_scelta.p).x)[2:].zfill(curva_scelta.keysize)[16:]
print(f"r[i+2] ottenuto: {ri_plus_two_attack}")

print(f"sono uguali?: {ri_plus_two_drbg == ri_plus_two_attack}")

print(f"\nAttacco eseguito correttamente.")