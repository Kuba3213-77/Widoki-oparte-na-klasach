from typing import List, Optional

from models import Ksiazka


class RepozytoriumKsiazek:
    def __init__(self) -> None:
        self._ksiazki: List[Ksiazka] = []
        self._nastepne_id: int = 1

    def pobierz_wszystkie(self) -> List[Ksiazka]:
        return list(self._ksiazki)

    def pobierz_po_id(self, id_ksiazki: int) -> Optional[Ksiazka]:
        return next((k for k in self._ksiazki if k.id == id_ksiazki), None)

    def utworz(self, tytul: str, autor: str, rok: int) -> Ksiazka:
        ksiazka = Ksiazka(id=self._nastepne_id, tytul=tytul, autor=autor, rok=rok)
        self._nastepne_id += 1
        self._ksiazki.append(ksiazka)
        return ksiazka

    def aktualizuj(self, id_ksiazki: int, tytul: str, autor: str, rok: int) -> Optional[Ksiazka]:
        ksiazka = self.pobierz_po_id(id_ksiazki)
        if ksiazka is None:
            return None
        ksiazka.tytul = tytul
        ksiazka.autor = autor
        ksiazka.rok = rok
        return ksiazka

    def usun(self, id_ksiazki: int) -> bool:
        ksiazka = self.pobierz_po_id(id_ksiazki)
        if ksiazka is None:
            return False
        self._ksiazki.remove(ksiazka)
        return True
