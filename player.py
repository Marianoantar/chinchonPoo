from __future__ import annotations
from typing import Dict, List, Tuple, Any, Union, Optional
Card = Tuple[int, str]
PlayerData = List[Any]  # [mano, juegos, libres, puntos, condicion]
PlayerKey = Union[str, int]
class Jugador:
    def __init__(self, nombre : str):
        self.mano = []
        self.juegos = []
        self.libres = []
        self.puntos = 0
        self.condicion = True
        self.nombre = nombre
    def recibir_carta(self, carta: Card) -> None:
        self.mano.append(carta)
    def mostrar_cartas_mano(self) -> None:
        print(f" . cartas en la mano: {self.mano}")
        print(f" . juegos posibles: {self.juegos}")
        print(f" . cartas libres: {self.libres}")
        print(f" . puntos en mano: {self.contar_puntos()}")
        
    def bajar_cartas(self) -> None:
        print(f"\nJugador {self.nombre}")
        print(f" . juegos armados: {self.juegos}")
        print(f" . cartas libres: {self.libres}")

    def contar_puntos(self) -> int:
        cartas: List[Card] = self.libres
        return sum(carta[0] for carta in cartas)
    
    def chequear_puntos(self) -> None:
        if self.puntos > 100:
            self.condicion = False
            print(f"\n********** ATENCION **********\nEl jugador {self.nombre} quedo ELIMINADO!!!!!")

