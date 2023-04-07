from time import time
from EC_DRBG import *
from utils import *

print("\n-- SIMULAZIONE ATTACCO AL GENERATORE EC-DRBG TRAMITE BACKDOOR --\n")

# richiesta input all'utente
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

# prendiamo Q pari al punto base G della curva per semplicità (essendo un punto che ne appartiene)
Q = curva_scelta.G

# introduciamo la backdoor, cioè calcoliamo P = eQ
e = 0xdeadbeef
P = raddoppi_ripetuti(Q, e, curva_scelta)

# supponiamo che il generatore di cui vogliamo conoscere lo stato utilizzi P, Q con la backdoor (P = eQ)
generatore_vulnerabile = EC_DRBG(P, Q, curva_scelta)

# attenzione: non stiamo usando i P, Q dati dal NIST, poichè non sappiamo se ci sia veramente una relazione tra P, Q che fornisce il NIST

# generiamo un pò di bit
niterazioni = 10
print(f"\nEseguo {niterazioni} iterazioni dell'EC-DRBG...")
generatore_vulnerabile.generate_bits(niterazioni)

# supponiamo di ottenere i bit generati alla i-esima iterazione (che è facile, tipicamente sono mandati in chiaro nelle applicazioni in cui vengono usati)
ri = generatore_vulnerabile.generate_bits()
# generiamo anche i bit alla iterazione successiva, da usare nel confronto
ri_plus_one = generatore_vulnerabile.generate_bits()

# applichiamo l'attacco shumow-ferguson e dimostriamo di saper generare correttamente i bit da qui in avanti
# ipotizziamo di essere il NIST: generatore_vulnerabile è una istanza del generatore di cui non conosciamo il seed che però sappiamo utilizza i P, Q e la curva da noi consigliate
start_time = time()

# è più veloce prima trovare gli R candidati (poichè sono 2^15 anzichè 2^16)
candidatiR = []
# enumeriamo tutti i possibili 16 bit più significativi che sono stati scartati da ri, concateniamoli ad esso ottenendo rix e verifichiamo che esista una coordinata riy associata ad rix
# alla fine otterremo che circa la metà degli rix ammettono radici nel campo (quindi 2^15 con 16 bit da enumerare) 
niterazioni = pow(2, 16)
for guess in range(0, niterazioni):
    print(f"Concateno e verifico residuo quadratico per {guess} di {niterazioni}...", end='\r')
    # concateno
    rix = int(bin(guess)[2:].zfill(16) + str(ri), 2) 

    # se è un residuo quadratico, aggiungiamo alla lista
    riy = eval_cubica(rix, curva_scelta)
    if(riy != 0):
        candidato_R = point(rix, riy)
        candidatiR.append(candidato_R)

print(f"Concateno e verifico residuo quadratico per {niterazioni} di {niterazioni}...")

# ci sarà sicuramente il punto R relativo allo stato successivo, andiamo a controllare quale sia (alla peggio sono 2^15 iterazioni)
ncandidatiR = len(candidatiR)
i = 0
for R in candidatiR:
    print(f"Verifico i candidati punti R della curva ellittica {curva_scelta.name}, candidato {i} di {ncandidatiR}...", end='\r')
    i += 1
    # calcoliamo il possibile si_plus_one P = eR
    candidato_si_plus_one = raddoppi_ripetuti(R, e, curva_scelta).x
    # calcoliamo il blocco dei bit associati ad esso facendo si_plus_one Q
    candidato_ri_plus_one = bin(raddoppi_ripetuti(Q, candidato_si_plus_one, curva_scelta).x)[2:].zfill(curva_scelta.keysize)[16:]

    # se sono uguali a quelli del DRBG, con assoluta certezza lo stato utilizzato per ottenerli sarà lo stato interno successivo
    if(candidato_ri_plus_one == ri_plus_one):
        # generiamo una copia del DRBG, utilizzando come seed lo stato appena trovato
        generatore_clonato = EC_DRBG(P, Q, curva_scelta, candidato_si_plus_one)
        print(f"Verifico i candidati punti R della curva ellittica {curva_scelta.name}, candidato {i} di {ncandidatiR}...")
        print(f"\nTrovato lo stato successivo in {round(time() - start_time, 2)} secondi!")
        print(f"> s[i+1] = {hex(candidato_si_plus_one)}")
        print(f"> R = ({hex(R.x)}, {hex(R.y)})")
        break

# verifiche aggiuntive, non necessarie ma per scaramanzia 
print(f"\nVerifica iterazioni successive:")

n = 5
for i in range(1, n+1):
    print(f"\n-- iterazione i+{i+1} --")

    print(f"I due blocchi di bit generati sono uguali?: {generatore_vulnerabile.generate_bits() == generatore_clonato.generate_bits()}")

print(f"\nAttacco eseguito correttamente.")