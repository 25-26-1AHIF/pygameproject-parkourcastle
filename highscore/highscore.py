import pygame

def score_speichern(name: str, punkte: int, dateiname: str = "highscore_pygame.txt") -> None:
    with open(dateiname, "a") as fp:
        fp.write(f"{name}: {punkte}\n")

def score_laden(dateiname: str = "highscore_pygame.txt") -> list:
    ergebnisse: list = []
    try:
        with open(dateiname, "r") as fp:
            lines = fp.readlines()
    except FileNotFoundError:
        print(f"Datei '{dateiname}' konnte nicht geöffnet werden. Rückgabe: Leere Liste!")
        exit(0)
    for i in range(len(lines)):
        parts = lines[i].rstrip().split(";")
        if len(parts) != 2:
            print(f"Zeile {i+1} hat {len(parts)} Teile statt 2 - wird übersprungen.")
            continue
        name = parts[0]
        try:
            punkte = int(parts[1])
        except:
            print(f"Zeile {i+1} enthält keine ganze Zahl bei den Punkten - wird übersprungen.")
            continue
        ergebnisse.append((name, punkte))
    return ergebnisse

def bester_score(scores: list):
    if not scores:
        print("Keine Scores vorhanden")
        return
    best_name, best_punkte = scores[0]
    for i in range(1, len(scores)):
        name, punkte = scores[i]
        if punkte > best_punkte:
            best_name, best_punkte = name, punkte
    print(f"Bester Spieler: {best_name} mit {best_punkte} Punkten")

def scores_ausgeben(scores: list):
    if not scores:
        print("===== Highscore-Liste =====")
        print("Keine Scores vorhanden")
        return
    arr = []
    for i in range(len(scores)):
        arr.append(scores[i])
    n = 0
    while n < len(arr):
        max_idx = n
        j = n + 1
        while j < len(arr):
            if arr[j][1] > arr[max_idx][1]:
                max_idx = j
            j += 1
        if max_idx != n:
            temp = arr[n]
            arr[n] = arr[max_idx]
            arr[max_idx] = temp
        n += 1
    max_len = 0
    for i in range(len(arr)):
        if len(arr[i][0]) > max_len:
            max_len = len(arr[i][0])
    print("===== Highscore-Liste =====")
    rank = 1
    for i in range(len(arr)):
        name, punkte = arr[i]
        spacing = " " * (max_len - len(name))
        print(f"{rank}. {name}{spacing} {punkte} Punkte")
        rank += 1

if __name__ == "__main__":

    scores = scores_laden()
    for i in range(len(scores)):
        name, punkte = scores[i]
        print(f"{name} hat {punkte} Punkte")

    bester_score(scores)
    scores_ausgeben(scores)