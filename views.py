from flask import request, jsonify
from flask.views import MethodView

from controller import KontrolerKsiazek


class WidokListyKsiazek(MethodView):
    def __init__(self, kontroler: KontrolerKsiazek) -> None:
        self.kontroler = kontroler

    def get(self):
        dane, status = self.kontroler.pobierz_wszystkie_ksiazki()
        return jsonify(dane), status

    def post(self):
        dane, status = self.kontroler.utworz_ksiazke(request.get_json(silent=True) or {})
        return jsonify(dane), status


class WidokSzczegolowKsiazki(MethodView):
    def __init__(self, kontroler: KontrolerKsiazek) -> None:
        self.kontroler = kontroler

    def get(self, id: int):
        dane, status = self.kontroler.pobierz_ksiazke(id)
        return jsonify(dane), status

    def put(self, id: int):
        dane, status = self.kontroler.aktualizuj_ksiazke(id, request.get_json(silent=True) or {})
        return jsonify(dane), status

    def delete(self, id: int):
        dane, status = self.kontroler.usun_ksiazke(id)
        return jsonify(dane), status
