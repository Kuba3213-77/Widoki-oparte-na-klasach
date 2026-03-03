import json
from unittest.mock import MagicMock

import pytest
from flask import Flask

from controller import KontrolerKsiazek
from views import WidokListyKsiazek, WidokSzczegolowKsiazki

KSIAZKA = {"id": 1, "tytul": "Clean Code", "autor": "R. Martin", "rok": 2008}
DANE = {"tytul": "T", "autor": "A", "rok": 2000}


@pytest.fixture()
def mock_kontroler():
    return MagicMock(spec=KontrolerKsiazek)


@pytest.fixture()
def aplikacja(mock_kontroler):
    apka = Flask(__name__)
    apka.add_url_rule("/books",
        view_func=WidokListyKsiazek.as_view("lista_ksiazek", kontroler=mock_kontroler),
        methods=["GET", "POST"])
    apka.add_url_rule("/books/<int:id>",
        view_func=WidokSzczegolowKsiazki.as_view("szczegoly_ksiazki", kontroler=mock_kontroler),
        methods=["GET", "PUT", "DELETE"])
    return apka


@pytest.fixture()
def klient(aplikacja):
    return aplikacja.test_client()


def tresc(odp):
    return json.loads(odp.data)


class TestPobierzKsiazki:
    def test_pusta_lista(self, klient, mock_kontroler):
        mock_kontroler.pobierz_wszystkie_ksiazki.return_value = ([], 200)
        odp = klient.get("/books")
        assert odp.status_code == 200 and tresc(odp) == []

    def test_zwraca_ksiazki(self, klient, mock_kontroler):
        mock_kontroler.pobierz_wszystkie_ksiazki.return_value = ([KSIAZKA], 200)
        odp = klient.get("/books")
        assert odp.status_code == 200 and tresc(odp) == [KSIAZKA]

    def test_wywoluje_kontroler(self, klient, mock_kontroler):
        mock_kontroler.pobierz_wszystkie_ksiazki.return_value = ([], 200)
        klient.get("/books")
        mock_kontroler.pobierz_wszystkie_ksiazki.assert_called_once()


class TestPobierzKsiazke:
    def test_znaleziona(self, klient, mock_kontroler):
        mock_kontroler.pobierz_ksiazke.return_value = (KSIAZKA, 200)
        odp = klient.get("/books/1")
        assert odp.status_code == 200 and tresc(odp) == KSIAZKA

    def test_nie_znaleziona(self, klient, mock_kontroler):
        mock_kontroler.pobierz_ksiazke.return_value = ({"blad": "Ksiazka nie znaleziona"}, 404)
        assert klient.get("/books/999").status_code == 404

    def test_przekazuje_id(self, klient, mock_kontroler):
        mock_kontroler.pobierz_ksiazke.return_value = ({}, 200)
        klient.get("/books/42")
        mock_kontroler.pobierz_ksiazke.assert_called_once_with(42)


class TestUtworzKsiazke:
    def test_utworzona(self, klient, mock_kontroler):
        utworzona = {"id": 1, **DANE}
        mock_kontroler.utworz_ksiazke.return_value = (utworzona, 201)
        odp = klient.post("/books", json=DANE)
        assert odp.status_code == 201 and tresc(odp) == utworzona

    @pytest.mark.parametrize("dane", [{"tytul": "Tylko"}, {}])
    def test_bledne_dane(self, klient, mock_kontroler, dane):
        mock_kontroler.utworz_ksiazke.return_value = ({"blad": "..."}, 400)
        assert klient.post("/books", json=dane).status_code == 400

    def test_przekazuje_dane(self, klient, mock_kontroler):
        mock_kontroler.utworz_ksiazke.return_value = ({"id": 1, **DANE}, 201)
        klient.post("/books", json=DANE)
        mock_kontroler.utworz_ksiazke.assert_called_once_with(DANE)


class TestAktualizujKsiazke:
    def test_zaktualizowana(self, klient, mock_kontroler):
        zaktualizowana = {"id": 1, **DANE}
        mock_kontroler.aktualizuj_ksiazke.return_value = (zaktualizowana, 200)
        odp = klient.put("/books/1", json=DANE)
        assert odp.status_code == 200 and tresc(odp) == zaktualizowana

    def test_nie_znaleziona(self, klient, mock_kontroler):
        mock_kontroler.aktualizuj_ksiazke.return_value = ({"blad": "Ksiazka nie znaleziona"}, 404)
        assert klient.put("/books/999", json=DANE).status_code == 404

    def test_bledne_dane(self, klient, mock_kontroler):
        mock_kontroler.aktualizuj_ksiazke.return_value = ({"blad": "..."}, 400)
        assert klient.put("/books/1", json={"tytul": "Tylko"}).status_code == 400

    def test_przekazuje_id_i_dane(self, klient, mock_kontroler):
        mock_kontroler.aktualizuj_ksiazke.return_value = ({"id": 7, **DANE}, 200)
        klient.put("/books/7", json=DANE)
        mock_kontroler.aktualizuj_ksiazke.assert_called_once_with(7, DANE)


class TestUsunKsiazke:
    def test_usunieta(self, klient, mock_kontroler):
        mock_kontroler.usun_ksiazke.return_value = ({"wiadomosc": "Ksiazka usunieta"}, 200)
        odp = klient.delete("/books/1")
        assert odp.status_code == 200 and tresc(odp)["wiadomosc"] == "Ksiazka usunieta"

    def test_nie_znaleziona(self, klient, mock_kontroler):
        mock_kontroler.usun_ksiazke.return_value = ({"blad": "Ksiazka nie znaleziona"}, 404)
        assert klient.delete("/books/999").status_code == 404

    def test_przekazuje_id(self, klient, mock_kontroler):
        mock_kontroler.usun_ksiazke.return_value = ({"wiadomosc": "Ksiazka usunieta"}, 200)
        klient.delete("/books/5")
        mock_kontroler.usun_ksiazke.assert_called_once_with(5)
