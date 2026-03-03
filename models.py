from dataclasses import dataclass, asdict


@dataclass
class Ksiazka:
    id: int
    tytul: str
    autor: str
    rok: int

    def na_slownik(self) -> dict:
        return asdict(self)
