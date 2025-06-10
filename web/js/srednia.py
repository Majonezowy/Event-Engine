srednie = {}
seria = 1

liczba_pokoi = 23
for i in range(1, liczba_pokoi + 1):
    srednie[i] = [0, 0]
i = 1
while True:
    while i <= liczba_pokoi:
        try:
            wartosc = input(f"Podaj średnią dla pokoju {i} (seria {seria}): ")

            if not int(wartosc) in range(1, 9):
                raise ValueError("Wartość musi być liczbą całkowitą od 1 do 8.")
            srednie[i][0] += int(wartosc)
            srednie[i][1] += 1
        except ValueError:
            if wartosc.lower() == 'koniec':
                break
            elif wartosc.lower() == 's':
                pass
            else:
                print("Błędna wartość, spróbuj ponownie.")
                continue
        i += 1

    seria += 1
    i = 1
    if wartosc.lower() == 'koniec':
        break

for i in range(1, liczba_pokoi + 1):
    if seria > 1:
        srednie[i][0] /= srednie[i][1]
    print(f"Średnia dla pokoju {i} [serie={srednie[i][1]}]: {srednie[i][0]:.2f}")