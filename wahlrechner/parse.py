import copy
import os

import numpy
from django.http.response import Http404

from .models import These, Partei, Antwort

SCHLUESSEL = {
    "0": [None, None],  # These nicht beantwortet (Null)
    "1": ["a", False],  # Agree
    "2": ["d", False],  # Disagree
    "3": ["n", False],  # Neutral
    "5": ["a", True],  # Agree (Priorisiert)
    "6": ["d", True],  # Disagree (Priorisiert)
    "7": ["n", True],  # Neutral (Priorisiert)
    "9": ["s", False],  # These übersprungen (Skip)
}


def get_key_from_value(d, val):
    """Gibt Key für Wert val im Dictionary d zurück."""
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None


def alle_thesen():
    """Gibt alle Thesen sortiert in einer Liste zurück."""
    return These.objects.all().order_by("these_nr")


def decode_zustand(zustand=0):
    """Dekodiert die Zustandsinformationen, gibt ein Opinions-Dictionary zurück."""

    # Kodiere den Zustand aus Base-36 in Base-10
    zustand = int(str(zustand).upper(), 36)

    # Erstelle ein Dictionary mit allen Thesen
    opinions = dict()
    for t in These.objects.all():
        opinions[t] = SCHLUESSEL.get("0").copy()

    for pk, status in enumerate(list(str(zustand))[::-1]):

        # Falls ein Status 4 oder 8 ist, muss es sich um einen ungültigen Zustand handeln
        if status in ["4", "8"]:
            raise Http404
        else:
            t = These.objects.filter(pk=pk).first()

            if t:
                opinions[t] = SCHLUESSEL.get(status).copy()

    return opinions


def encode_zustand(opinions):
    """Kodiert die Zustandsinformationen aus einem Opinions-Dictionary, gibt einen Zustand in Base-36 zurück."""

    opinions = list(opinions.items())
    zustand = 0

    for these, s in opinions:
        status = get_key_from_value(SCHLUESSEL, s)
        zustand += int(status) * (10**these.pk)

    zustand = numpy.base_repr(zustand, 36)

    return zustand


def generate_zustand(opinions, these, opinion):
    """Gibt einen Zustand zurück, bei dem die Position bei these zu opinion geändert wurde."""

    opinions = copy.deepcopy(opinions)

    if not (prio := opinions[these][1]) or opinion == "s":
        prio = False

    opinions[these] = [opinion, prio]

    return encode_zustand(opinions)


def thesen_index(thesen, these_current):
    """Berechnet die Position der aktuellen These im Vergleich zu allen Thesen.
    Gibt ein Tuple zurück: (aktuelle_pos, max_pos)"""
    aktuelle_pos = (*thesen,).index(these_current) + 1
    max_pos = len(thesen)

    return aktuelle_pos, max_pos


def these_next(thesen, index):
    """Gibt das Objekt der nachfolgenden These zurück."""
    if index[0] < index[1]:
        return thesen[index[0]]
    else:
        return None


def these_prev(thesen, index):
    """Gibt das Objekt der vorherigen These zurück."""
    if index[0] > 1:
        return thesen[index[0] - 2]
    else:
        return None


def update_opinions(opinions, get_dict):
    """Aktualisiert Opinion-Dictionary: Einträge ohne Positionierung werden als übersprungen markiert,
    Thesen mit einem passenden GET-Parameter werden als priorisiert markiert."""

    opinions = copy.deepcopy(opinions)

    for these in opinions.keys():
        if opinions[these] == [None, None]:
            # Markiere nicht beantwortete Thesen als Übersprungen
            opinions[these] = ["s", False]
        else:
            # Passe Priorisierung entsprechend der GET-Parameter an
            if get_dict.get(str(these.pk), False):
                opinions[these] = [opinions[these][0], True]
            else:
                opinions[these] = [opinions[these][0], False]

    return encode_zustand(opinions)


# noinspection PyGlobalUndefined,PyUnboundLocalVariable
def calc_result(zustand, opinions):
    """Berechnet die Übereinstimmung zwischen Nutzer und Parteien."""

    caching_enabled = bool(int(os.getenv("WAHLRECHNER_CACHING", 0)))

    # Erstelle Cache-Dictionary falls nicht vorhanden
    if "cache" not in globals():
        global cache
        cache = dict()

    # Erhalte Ergebnis falls im Cache
    if zustand in cache:
        results = cache.get(zustand)

    # Sonst berechne Ergebnis
    else:
        results = []

        for partei in Partei.objects.all():
            total_p = 0
            max_p = 0

            for antwort in Antwort.objects.filter(antwort_partei=partei):

                # Position des Nutzers
                opinion = opinions[antwort.antwort_these][0]
                prio = opinions[antwort.antwort_these][1]

                # Falls These nicht übersprungen
                if opinion != "s":

                    # Stimmt Position mit Antwort der Partei überein? (2 Punkte)
                    if opinion == antwort.antwort_position:
                        p = 2
                    # Teilweise Übereinstimmung, Position der Partei oder eigene Position neutral? (1 Punkt)
                    elif opinion == "n" or antwort.antwort_position == "n":
                        p = 1
                    # Keine Übereinstummung (0 Punkte)
                    else:
                        p = 0

                    # Ist These vom Nutzer priorisiert? (Doppelte Punkte)
                    if prio:
                        total_p += p * 2
                        max_p += 4  # bei einer wichtigen These sind maximal erreichbare Punkte 4
                    else:
                        total_p += p
                        max_p += 2  # bei einer normalen These sind maximal erreichbare Punkte 2

            if max_p == 0:
                percentage = 0
            else:
                percentage = round((total_p / max_p * 100), 1)

            results.append((partei, percentage))

        # Sortiere die Ergebnisse nach der prozentualen Übereinstimmung
        results.sort(key=lambda i: i[1], reverse=True)

        # Füge Ergebnis dem Cache hinzu
        if caching_enabled:
            cache[zustand] = results

    return results


def check_result(opinions):
    """Überprüft, ob ein Ergebnis aussagekräftig ist."""
    skips = 0

    for these in These.objects.all():
        if opinions[these][0] == "s":
            skips += 1

    if skips > These.objects.all().count() * 0.7:
        return False
    else:
        return True


def calc_antworten(zustand, opinions, these):
    antworten = []

    for partei, _ in calc_result(zustand, opinions):
        try:
            antwort = Antwort.objects.get(antwort_these=these, antwort_partei=partei)
            antworten.append(antwort)
        except Antwort.DoesNotExist:
            pass

    return antworten


def increase_result_count():
    """Erhöht den Zähler result_count.txt um 1."""

    # Lese den Zähler aus
    try:
        with open("wahlrechner/stats/result_count.txt", "r") as file:
            result_count = file.read()

        if result_count == "":
            result_count = 0
        else:
            result_count = int(result_count)

    except (FileNotFoundError, ValueError):
        result_count = 0

    # Erhöhe den Zähler um 1
    result_count += 1

    # Erstelle die Zähler-Datei, falls sie noch nicht existiert
    if not os.path.exists("wahlrechner/stats"):
        os.mkdir("wahlrechner/stats")

    # Aktualisiere den Zähler in der Zähler-Datei
    with open("wahlrechner/stats/result_count.txt", "w") as file:
        file.write(str(result_count))
