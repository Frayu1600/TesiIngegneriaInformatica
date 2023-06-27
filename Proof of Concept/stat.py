from statistics import mean, variance

curves = ["P-192", "P-224", "P-256", "P-384", "P-521"]
test_values = []

print("\n-- ANALISI DEI TEST PER L'ATTACCO SHUMOW-FERGUSON --\n")

for curve in curves:
    print("> " + curve)
    # apertura del file
    with open(curve + " benchmark tests.txt", "r") as file:

        content = file.readlines()

        # lettura riga per riga
        for line in content:
            # individuazione degli indici di inizio e fine
            start_index = line.find("in ") + 2
            end_index = line.find("secondi", start_index)

            if start_index != -1 and end_index != -1:
                test_value = float(line[start_index:end_index].strip())
                test_values.append(test_value)

    media = round(mean(test_values), 1)
    varianza = round(variance(test_values), 1)

    print("Media dei risultati: " + str(media) + " sec")
    print("Varianza dei risultati: " + str(varianza))
    print("\n")