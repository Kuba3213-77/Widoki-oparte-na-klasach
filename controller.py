from typing import List, Tuple

from repository import RepozytoriumKsiazek


class KontrolerKsiazek:
    def __init__(self, repozytorium: RepozytoriumKsiazek) -> None:
        self._repozytorium = repozytorium

    def pobierz_wszystkie_ksiazki(self) -> Tuple[List[dict], int]:
        ksiazki = self._repozytorium.pobierz_wszystkie()
        return [k.na_slownik() for k in ksiazki], 200

    def pobierz_ksiazke(self, id_ksiazki: int) -> Tuple[dict, int]:
        ksiazka = self._repozytorium.pobierz_po_id(id_ksiazki)
        if ksiazka is None:
            return {"blad": "Ksiazka nie znaleziona"}, 404
        return ksiazka.na_slownik(), 200

    def utworz_ksiazke(self, dane: dict) -> Tuple[dict, int]:
        if not dane or not all(k in dane for k in ("tytul", "autor", "rok")):
            return {"blad": "Brakujace pola: tytul, autor, rok"}, 400
        ksiazka = self._repozytorium.utworz(dane["tytul"], dane["autor"], int(dane["rok"]))
        return ksiazka.na_slownik(), 201

    def aktualizuj_ksiazke(self, id_ksiazki: int, dane: dict) -> Tuple[dict, int]:
        if not dane or not all(k in dane for k in ("tytul", "autor", "rok")):
            return {"blad": "Brakujace pola: tytul, autor, rok"}, 400
        ksiazka = self._repozytorium.aktualizuj(id_ksiazki, dane["tytul"], dane["autor"], int(dane["rok"]))
        if ksiazka is None:
            return {"blad": "Ksiazka nie znaleziona"}, 404
        return ksiazka.na_slownik(), 200

    def usun_ksiazke(self, id_ksiazki: int) -> Tuple[dict, int]:
        usunieto = self._repozytorium.usun(id_ksiazki)
        if not usunieto:
            return {"blad": "Ksiazka nie znaleziona"}, 404
        return {"wiadomosc": "Ksiazka usunieta"}, 200
