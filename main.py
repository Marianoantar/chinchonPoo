"""Modulo inicial (entrypoint)."""
from __future__ import annotations
from typing import Dict, List, Tuple
from players_manager import iniciar_jugadores
from system import  comienzo_juego, borrar_pantalla, barajar_y_dar

Card = Tuple[int, str]
PlayerDict = Dict[int, List]

def inicializar(cantidad_jugadores: int = 2) -> Tuple[dict, List[Card], List[Card]]:
    """
    Inicializa jugadores, mazo y descarte (mantiene la interfaz original).
    """
    jugadores = iniciar_jugadores(cantidad_jugadores)
    print("- jugadores Iniciados!!!")
    deck = barajar_y_dar(jugadores)
    return jugadores, deck
def run() -> None:
    borrar_pantalla()
    print("Bienvenido al juego del CHINCHON\n")
    while True:
        cant = input("Cuantos jugadores quieres crear? (2-3-4): ")
        try:
            cant = int(cant)
            if cant in range(2, 5):
                break
            else:
                print("Error: Debes Ingresar un numero entre 2 y 4, luego pulsa enter")
        except ValueError:
            print("Error: Debes Ingresar un numero entre 2 y 4, luego pulsa enter")
    jugadores, deck = inicializar(cant)
    comienzo_juego(jugadores, deck)
## lo tengo en vs
if __name__ == "__main__":
    run()
