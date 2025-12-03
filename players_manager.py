from __future__ import annotations
from typing import Dict, List, Union, Tuple, Any, Optional
Card = Tuple[int, str]
PlayerData = List[Any]  # [mano, juegos, libres, puntos, condicion]
PlayerKey = Union[str, int]
PlayersDict = Dict[PlayerKey, PlayerData]
from player import *

def iniciar_jugadores(cantidad: int) -> PlayersDict:
    """Crea diccionario de jugadores con la estructura original."""
    jugadores: PlayersDict = {}
    for numero in range(1, cantidad + 1):
        nombre_jugador = f"Jugador_{numero}"
        jugadores[nombre_jugador] = Jugador(nombre_jugador)  # mano, juegos, libres, puntos, estado
    return jugadores

def mostrar_cartas(jugadores: PlayersDict) -> None:
    print("Lista de jugadores y sus cartas *****")
    print("Jugador Cartas")
    for jugador in jugadores:
        print(jugador, jugadores[jugador].mano)

def reiniciar_jugadores(jugadores: PlayersDict) -> None:
    for jugador in list(jugadores.keys()):
        if jugadores[jugador].condicion:
            jugadores[jugador].mano = []
            jugadores[jugador].juegos = []
            jugadores[jugador].libres = []
        else:
            jugadores.pop(jugador)


def proceso_descartar(jugador: Jugador, descarte: List[Card]) -> None:
    print("\nProceso descarte...")
    
    for i, carta in enumerate(jugador.mano):
        print(f"{i} - {carta}")
    while True:
        elegida = input("Tipea el numero de carta que quieres descartar: ")
        try:
            elegida_i = int(elegida)
            if 0 <= elegida_i < len(jugador.mano):
                break
            else:
                print("Error: debes elegir el numero de carta válido")
        except ValueError:
            print("Error: La entrada no es válida. Inténtalo de nuevo.")
    carta = jugador.mano[elegida_i]
    descartar(carta, descarte, jugador)

def descartar(carta: Card, descarte: List[Card], jugador: str) -> None:
    print(f"\nDescartando {carta}...\n")
    try:
        jugador.mano.remove(carta)
        jugador.libres.remove(carta)
    except ValueError:
        pass
    descarte.append(carta)
