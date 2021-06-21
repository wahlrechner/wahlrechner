from django.db import models

# Create your models here.


class These(models.Model):
    these_keyword_help = """<i>Maximal 40 Zeichen</i><br>
    Ein kurzes Schlagwort, um die These zu beschreiben. Wird in der
    Seitenleiste des Wahlrechners angezeigt.<br>
    <b>Beispiel:</b> Klimanotstand"""
    these_keyword = models.CharField(
        "Schlagwort", help_text=these_keyword_help, max_length=40)

    these_text_help = """<i>Maximal 400 Zeichen</i><br>
    Der vollständige Text der These.<br>
    <b>Beispiel:</b> Die Stadt XYZ sollte den Klimanotstand ausrufen."""
    these_text = models.TextField(
        "Vollständige These", help_text=these_text_help, max_length=400)

    these_nr_help = """Die Thesen-Nummer gibt Auskunft über die Reihenfolge, in der alle Thesen
    angezeigt werden. Dabei wird als erstes die These mit der niedrigsten Thesen-Nummer angezeigt,
    danach die These mit der jeweils nächst größeren Thesen-Nummer, usw. Die Thesen-Nummer lässt
    sich also als Priorität für die angezeigte Reihenfolge verstehen, und kann auch eine krumme
    Zahl sein.<br>
    <b>Beispiel:</b> Die These, die zuerst angezeigt werden soll, hat die Nummer 1. Die zweite These
    die Nummer 2, usw."""
    these_nr = models.FloatField(
        "Thesen-Nummer", help_text=these_nr_help, unique=True)

    def __str__(self):
        return self.these_keyword

    class Meta:
        verbose_name = "These"
        verbose_name_plural = "Thesen"


class Partei(models.Model):
    partei_name_help = """<i>Maximal 50 Zeichen</i><br>
    Gib den Namen der Partei an, der für den Benutzer angezeigt werden soll."""
    partei_name = models.CharField(
        "Name", help_text=partei_name_help, max_length=50)

    partei_beschreibung_help = """<i>Maximal 1000 Zeichen</i><br>
    Beschreibung für die Partei, wird auf der Ergebnis-Seite angezeigt."""
    partei_beschreibung = models.TextField(
        "Name", help_text=partei_beschreibung_help, max_length=1000)

    def __str__(self):
        return self.partei_name

    class Meta:
        verbose_name = "Partei"
        verbose_name_plural = "Parteien"


class Antwort(models.Model):
    antwort_these = models.ForeignKey(
        These, on_delete=models.CASCADE, verbose_name="These")
    antwort_partei = models.ForeignKey(
        Partei, on_delete=models.CASCADE, verbose_name="Partei")

    antwort_position_choices = [
        ('a', 'stimmt zu'),
        ('d', 'stimmt nicht zu'),
        ('n', 'neutral')
    ]
    antwort_position_help = """Wähle aus, wie sich die Partei zu der ausgewählten These positioniert."""
    antwort_position = models.CharField("Position zur These",
                                        choices=antwort_position_choices, help_text=antwort_position_help, max_length=1)

    antwort_text_help = """<i>Maximal 1000 Zeichen</i><br>
    Vollständige Antwort/Begründung der Partei zu ihrer Position."""
    antwort_text = models.TextField(
        "Antwort", help_text=antwort_text_help, max_length=1000, blank=True)

    def __str__(self):
        return f"{self.antwort_these.these_keyword} - {self.antwort_partei.partei_name}"

    class Meta:
        verbose_name = "Antwort"
        verbose_name_plural = "Antworten"
