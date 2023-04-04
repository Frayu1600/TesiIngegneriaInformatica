import raddoppi_ripetuti
import secrets # libreria per la casualità, crittograficamente sicura
import point 
import prime_elliptic_curve

class EC_DRBG:
    def __init__(self, P: point.point, Q: point.point, pec: prime_elliptic_curve.prime_elliptic_curve):
        self.current_state = secrets.randbits(128)
        self.P = P
        self.Q = Q
        self.pec = pec

    # rimuove i 16 bit più significativi da x 
    def __phi(self, x):
        #print(len((bin(x)[2:].zfill(256)[16:])))

        # NOTA: 256 dipende dall'ordine della curva
        return bin(x)[2:].zfill(self.pec.keysize)[16:]
    
    # genera 240 bit pseudocasuali per iterazione
    def generate_bits(self, iterations = 1):
        output = ''

        for _ in range(iterations):
            next_state = raddoppi_ripetuti.raddoppi_ripetuti(self.P, self.current_state, self.pec.a, self.pec.b, self.pec.p).x
            self.current_state = next_state
            bits = self.__phi(raddoppi_ripetuti.raddoppi_ripetuti(self.Q, next_state, self.pec.a, self.pec.b, self.pec.p).x)
            output += bits

        return output