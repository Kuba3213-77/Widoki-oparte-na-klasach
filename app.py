from flask import Flask

from repository import RepozytoriumKsiazek
from controller import KontrolerKsiazek
from views import WidokListyKsiazek, WidokSzczegolowKsiazki


def utworz_aplikacje() -> Flask:
    aplikacja = Flask(__name__)

    repozytorium = RepozytoriumKsiazek()
    kontroler = KontrolerKsiazek(repozytorium)

    widok_listy_ksiazek = WidokListyKsiazek.as_view("lista_ksiazek", kontroler=kontroler)
    widok_szczegolow_ksiazki = WidokSzczegolowKsiazki.as_view("szczegoly_ksiazki", kontroler=kontroler)

    aplikacja.add_url_rule("/books", view_func=widok_listy_ksiazek, methods=["GET", "POST"])
    aplikacja.add_url_rule("/books/<int:id>", view_func=widok_szczegolow_ksiazki, methods=["GET", "PUT", "DELETE"])

    return aplikacja


if __name__ == "__main__":
    aplikacja = utworz_aplikacje()
    aplikacja.run(debug=True)
