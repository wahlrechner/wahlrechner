from django.http.response import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string

from .parse import *


def start(request):
    context = {"thesen": alle_thesen(), "opinions": decode_zustand()}
    return render(request, "wahlrechner/start.html", context)


def these(request, these_pk, zustand):
    these_current = get_object_or_404(These, pk=these_pk)
    opinions = decode_zustand(zustand)

    thesen = alle_thesen()
    index = thesen_index(thesen, these_current)

    context = {
        "opinions": opinions,
        "index": index,
        "thesen": thesen,
        "these_current": these_current,
        "these_next": these_next(thesen, index),
        "these_prev": these_prev(thesen, index),
        "zustand_current": zustand,
        "zustand_agree": generate_zustand(opinions, these_current, "a"),
        "zustand_disagree": generate_zustand(opinions, these_current, "d"),
        "zustand_neutral": generate_zustand(opinions, these_current, "n"),
        "zustand_skip": generate_zustand(opinions, these_current, "s"),
    }

    return render(request, "wahlrechner/these.html", context)


def confirm(request, zustand):
    opinions = decode_zustand(zustand)
    thesen = alle_thesen()

    context = {
        "opinions": opinions,
        "thesen": thesen,
        "zustand_current": zustand,
    }

    return render(request, "wahlrechner/confirm.html", context)


def confirm_submit(request, zustand):
    opinions = decode_zustand(zustand)
    zustand = update_opinions(opinions, request.GET)
    return redirect("result", zustand)


def result(request, zustand):
    opinions = decode_zustand(zustand)
    thesen = alle_thesen()

    context = {
        "opinions": opinions,
        "thesen": thesen,
        "zustand_current": zustand,
        "result": calc_result(zustand, opinions),
        "aussagekraeftig": check_result(opinions),
    }

    increase_result_count()

    return render(request, "wahlrechner/result.html", context)


def reason(request, these_pk, zustand):
    these_current = get_object_or_404(These, pk=these_pk)
    opinions = decode_zustand(zustand)

    thesen = alle_thesen()
    index = thesen_index(thesen, these_current)

    context = {
        "opinions": opinions,
        "index": index,
        "thesen": thesen,
        "these_current": these_current,
        "these_next": these_next(thesen, index),
        "these_prev": these_prev(thesen, index),
        "zustand_current": zustand,
        "antworten": calc_antworten(zustand, opinions, these_current),
    }

    return render(request, "wahlrechner/reason.html", context)


def handler404(request, exception=""):
    return HttpResponseNotFound(render_to_string("error/404.html"))


def test404(request):
    return render(request, template_name="error/404.html")


def handler500(request):
    return HttpResponseServerError(render_to_string("error/500.html"))


def test500(request):
    return render(request, template_name="error/500.html")
