from utils import point, prime_elliptic_curve, raddoppi_ripetuti
import secrets # libreria per la casualita', crittograficamente sicura

class EC_DRBG:
    def __init__(self, P: point, Q: point, prime_elliptic_curve: prime_elliptic_curve, seed = secrets.randbits(128)):
        self.__current_state = seed
        self.P = P
        self.Q = Q
        self.prime_elliptic_curve = prime_elliptic_curve

    # rimuove i 16 bit piu' significativi da x 
    def __phi(self, x):
        # notare che l'output dipende dalla grandezza della curva
        return bin(x)[2:].zfill(self.prime_elliptic_curve.keysize)[16:]
    
    # genera (self.prime_elliptic_curve.keysize - 16) bit pseudocasuali per iterazione
    def generate_bits(self, iterations = 1):
        output = ''

        for _ in range(iterations):
            # calcolo stato successivo
            next_state = raddoppi_ripetuti(self.P, self.__current_state, self.prime_elliptic_curve).x
            # aggiornamento stato successivo
            self.__current_state = next_state
            # generazione bit
            bits = self.__phi(raddoppi_ripetuti(self.Q, next_state, self.prime_elliptic_curve).x)
            # concatenazione
            output += bits

        return output