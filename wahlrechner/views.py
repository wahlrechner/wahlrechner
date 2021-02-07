import urllib
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import These


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

    # Wenn letzte Frage beantwortet, leite zur Bestätigungsseite weiter
    if these_pk == 'c':
        response = redirect('confirm')
        response['Location'] += f'?{current_payload}'
        return response

    # Erhalte Objekt der aktuellen These von PK existiert, sonst 404
    current_these = get_object_or_404(These, pk=these_pk)

    # Erhalte Index der aktuellen These und Länge aller Thesen
    pos = (*these_list,).index(current_these)
    max_pos = len(these_list)

    # Payload anpassen auf nächste These, wenn Frage nicht bearbeitet
    print(type(these_list.reverse()[0].pk))
    print(type(these_pk))
    if these_pk not in payload:
        if these_list.reverse()[0].pk == int(these_pk):
            payload['t'] = 'c'
        else:
            next_these = these_list[pos + 1]
            payload['t'] = next_these.pk
    else:
        # Sonst bei aktueller These bleiben
        payload['t'] = these_pk

    # Versuche Key aus Payload zu entfernen
    try:
        del payload[these_pk]
    except:
        pass

    # Payload anpassen bei Zustimmung
    payload[these_pk] = 'a'
    payload_agree = urllib.parse.urlencode(payload)

    # Payload anpassen bei Ablehnung
    del payload[these_pk]
    payload[these_pk] = 'd'
    payload_disagree = urllib.parse.urlencode(payload)

    # Payload anpassen bei Neutral
    del payload[these_pk]
    payload[these_pk] = 'n'
    payload_neutral = urllib.parse.urlencode(payload)

    # Payload anpassen bei Überspringen
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
               'payload_skip': payload_skip
               }

    return render(request, 'wahlrechner/these.html', context)


def confirm(request):
    # Erhalte alle Thesen sortiert nach der Thesen-Nummer
    these_list = These.objects.all().order_by('these_nr')

    return render(request, 'wahlrechner/confirm.html', {'these_list': these_list})
