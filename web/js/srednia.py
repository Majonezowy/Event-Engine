import pickle
import os

BACKUP_FILE = "srednia_backup.pkl"

def save_backup(srednie, seria, i):
    with open(BACKUP_FILE, "wb") as f:
        pickle.dump((srednie, seria, i), f)

def load_backup():
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, "rb") as f:
            return pickle.load(f)
    return None

srednie = {}
seria = 1
i = 1

liczba_pokoi = 23

backup = load_backup()
if backup:
    srednie, seria, i = backup
    print("Przywrócono dane z kopii zapasowej.")
else:
    for idx in range(1, liczba_pokoi + 1):
        srednie[idx] = [0, 0]

while True:
    while i <= liczba_pokoi:
        try:
            wartosc = input(f"Podaj średnią dla pokoju {i} (seria {seria}): ")

            if not wartosc.isdigit() or not int(wartosc) in range(1, 9):
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
        save_backup(srednie, seria, i) 

    seria += 1
    i = 1
    save_backup(srednie, seria, i)
    if wartosc.lower() == 'koniec':
        break

for idx in range(1, liczba_pokoi + 1):
    if srednie[idx][1] > 0:
        srednie[idx][0] /= srednie[idx][1]
    print(f"Średnia dla pokoju {idx} [serie={srednie[idx][1]}]: {srednie[idx][0]:.2f}")

if os.path.exists(BACKUP_FILE):
    os.remove(BACKUP_FILE)