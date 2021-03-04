import urllib
import os
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import Antwort, Partei, These


def start(request):
    # Erhalte alle Thesen sortiert nach der Thesen-Nummer
    these_list = These.objects.all().order_by('these_nr')

    return render(request, 'wahlrechner/start.html', {'these_list': these_list})


def these(request):
    # Erhalte alle Thesen sortiert nach der Thesen-Nummer
    these_list = These.objects.all().order_by('these_nr')

    # Erhalte these_pk aus Parameter
    these_pk = request.GET.get('t', '')

    # 404 wenn kein Parameter angegeben
    if these_pk == '':
        raise Http404

    # Erhalte Payload aus den Get-Parametern
    payload = request.GET.copy()
    del payload['t']
    current_payload = urllib.parse.urlencode(payload)

    # Wenn letzte Frage beantwortet, leite zur Gewichtungsseite weiter
    if these_pk == 'c':
        response = redirect('confirm')
        response['Location'] += f'?{current_payload}'
        return response

    # Erhalte Objekt der aktuellen These von PK existiert, sonst 404
    current_these = get_object_or_404(These, pk=these_pk)

    # Erhalte Index der aktuellen These und Länge aller Thesen
    pos = (*these_list,).index(current_these)
    max_pos = len(these_list)

    # Falls letzte These beantwortet, zeige Weiter-Button
    if str(these_list.reverse()[0].pk) in payload:
        show_continue_button = True
    else:
        show_continue_button = False

    # Aktuelle These beantwortet?
    if these_pk in payload:
        these_beantwortet = True
    else:
        these_beantwortet = False

    # Payload anpassen für nächste These (nicht bei letzter These)
    if current_these != these_list.reverse()[0]:
        # Falls These beantwortet ändere TK um 1
        payload['t'] = these_list[pos + 1].pk
        payload_next = urllib.parse.urlencode(payload)
    else:
        payload_next = None

    # Payload anpassen für vorherige These (nicht bei erster These)
    if current_these != these_list[0]:
        payload['t'] = these_list[pos - 1].pk
        payload_previous = urllib.parse.urlencode(payload)
    else:
        payload_previous = None

    # Payload anpassen auf nächste These, wenn Frage nicht bearbeitet
    if these_pk not in payload:
        if current_these == these_list.reverse()[0]:
            # bei der letzten These ändern für Gewichtungs-Seite
            payload['t'] = 'c'
        else:
            next_these = these_list[pos + 1]
            payload['t'] = next_these.pk
    else:
        # Sonst bei aktueller These bleiben
        payload['t'] = these_pk

    # Payload anpassen für Zustimmung
    payload[these_pk] = 'a'
    payload_agree = urllib.parse.urlencode(payload)

    # Payload anpassen für Ablehnung
    del payload[these_pk]
    payload[these_pk] = 'd'
    payload_disagree = urllib.parse.urlencode(payload)

    # Payload anpassen für Neutral
    del payload[these_pk]
    payload[these_pk] = 'n'
    payload_neutral = urllib.parse.urlencode(payload)

    # Payload anpassen für Überspringen
    del payload[these_pk]
    payload[these_pk] = 's'
    payload_skip = urllib.parse.urlencode(payload)

    context = {'these_list': these_list,
               'aktuelle_these': current_these,
               'pos': pos + 1,
               'max_pos': max_pos,
               'current_payload': current_payload,
               'payload_agree': payload_agree,
               'payload_disagree': payload_disagree,
               'payload_neutral': payload_neutral,
               'payload_skip': payload_skip,
               'payload_next': payload_next,
               'payload_previous': payload_previous,
               'show_continue_button': show_continue_button,
               'these_beantwortet': these_beantwortet
               }

    return render(request, 'wahlrechner/these.html', context)


def confirm(request):
    # Erhalte alle Thesen sortiert nach der Thesen-Nummer
    these_list = These.objects.all().order_by('these_nr')

    # Payload für den Zurück-Knopf
    payload = request.GET.copy()
    current_payload = urllib.parse.urlencode(payload)
    payload['t'] = these_list.reverse()[0].pk
    payload_previous = urllib.parse.urlencode(payload)

    context = {'these_list': these_list,
               'current_payload': current_payload,
               'payload_previous': payload_previous,
               'aussagekraeftig': aussagekraeftig(request)
               }

    return render(request, 'wahlrechner/confirm.html', context)


def results(request):
    # Erhalte alle Thesen sortiert nach der Thesen-Nummer
    these_list = These.objects.all().order_by('these_nr')

    # Aktueller Payload
    payload = request.GET.copy()
    current_payload = urllib.parse.urlencode(payload)
    payload['t'] = these_list.reverse()[0].pk
    payload_previous = urllib.parse.urlencode(payload)

    results = calculate_results(request)

    context = {'these_list': these_list,
               'current_payload': current_payload,
               'payload_previous': payload_previous,
               'results': results,
               'aussagekraeftig': aussagekraeftig(request)}

    return render(request, 'wahlrechner/results.html', context)


def reason(request):
    # Erhalte alle Thesen sortiert nach der Thesen-Nummer
    these_list = These.objects.all().order_by('these_nr')

    # Erhalte Payload aus den Get-Parametern
    payload = request.GET.copy()
    del payload['t']
    current_payload = urllib.parse.urlencode(payload)

    # Erhalte these_pk aus Parameter
    these_pk = request.GET.get('t', '')

    # 404 wenn kein Parameter angegeben
    if these_pk == '':
        raise Http404

    # Erhalte Objekt der aktuellen These von PK existiert, sonst 404
    current_these = get_object_or_404(These, pk=these_pk)

    # Erhalte Index der aktuellen These und Länge aller Thesen
    pos = (*these_list,).index(current_these)
    max_pos = len(these_list)

    # Payload anpassen für nächste These (nicht bei letzter These)
    if current_these != these_list.reverse()[0]:
        # Falls These beantwortet ändere TK um 1
        payload['t'] = these_list[pos + 1].pk
        payload_next = urllib.parse.urlencode(payload)
    else:
        payload_next = None

    # Payload anpassen für vorherige These (nicht bei erster These)
    if current_these != these_list[0]:
        payload['t'] = these_list[pos - 1].pk
        payload_previous = urllib.parse.urlencode(payload)
    else:
        payload_previous = None

    # Berechne Ergebnisse
    results = calculate_results(request)

    # Erhalte Antworten der Parteien
    antworten = []
    for partei, _ in results:
        antwort = Antwort.objects.get(
            antwort_these=current_these, antwort_partei=partei)
        antworten.append(antwort)

    context = {'these_list': these_list,
               'current_payload': current_payload,
               'pos': pos + 1,
               'aktuelle_these': current_these,
               'payload_next': payload_next,
               'payload_previous': payload_previous,
               'antworten': antworten,
               'max_pos': max_pos,
               'results': results}

    return render(request, 'wahlrechner/reason.html', context)


def calculate_results(request):

    # Erhalte Cache falls vorhanden, sonst erstelle das globale Dictionary
    if not 'cache' in globals():
        global cache
        cache = {}

    # Erhalte Payload und entferne Parameter für die aktuelle These, falls vorhanden
    payload = request.GET.copy()
    if 't' in payload:
        del payload['t']

    # Sortiere die URL-Parameter und verwandel sie in einen String
    urlstr = urllib.parse.urlencode(sorted(payload.items()))

    # Erhalte Ergebnis aus Cache, falls vorhanden
    if urlstr in cache and bool(int(os.environ['WAHLRECHNER_CACHING'])):
        results = cache.get(urlstr)

    # Sonst berechne Ergebnis
    else:
        results = []

        for partei in Partei.objects.all():
            total_p = 0
            max_p = 0

            for antwort in Antwort.objects.filter(antwort_partei=partei):

                # Falls These nicht übersprungen
                if (position := request.GET.get(str(antwort.antwort_these.pk), "s")) != "s":

                    # Stimmt Position mit Antwort der Partei überein? (2 Punkte)
                    if position == antwort.antwort_position:
                        p = 2
                    # Teilweise Übereinstimmung, Position der Partei oder eigene Position neutral? (1 Punkt)
                    elif position == "n" or antwort.antwort_position == "n":
                        p = 1
                    # Keine Übereinstummung (0 Punkte)
                    else:
                        p = 0

                    # Ist These als wichtig makiert? (Doppelte Punkte)
                    if request.GET.get(f"p{antwort.antwort_these.pk}", False):
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
        results.sort(key=lambda partei: partei[1], reverse=True)

        # Füge Ergebnis dem Cache hinzu
        cache[urlstr] = results

    return results


def aussagekraeftig(request):
    skips = 0

    for these in These.objects.all():
        if request.GET.get(str(these.pk), "s") == "s":
            skips += 1

    if skips > These.objects.all().count() * 0.6:
        return False
    else:
        return True
