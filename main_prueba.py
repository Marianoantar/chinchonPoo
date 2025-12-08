"""Modulo inicial (entrypoint)."""
from __future__ import annotations
from typing import Dict, List, Tuple
from players_manager import iniciar_jugadores
from system import  comienzo_juego, borrar_pantalla, barajar_y_dar

Card = Tuple[int, str]
PlayerDict = Dict[int, List]

def inicializar(cantidad_jugadores: int = 2) -> Tuple[dict, List[Card], List[Card]]:
    """
    Inicializa jugadores, deck(mazo y descarte) (mantiene la interfaz original).
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
    
    # Trampita...
    print(f"\njugador1.cartas(antes de trampa): {jugadores["Jugador_1"].mano}\n") #!!!!!!
    acomodar_cartas(jugadores) 
    acomodar_descarte((10,"basto"),deck) # Primera carta de descarte que sea 5 de basto
    
    
    print(f"\njugador1.cartas: {jugadores["Jugador_1"].mano}\n") #!!!!!!
    
    comienzo_juego(jugadores, deck)
    
def acomodar_cartas(jugadores):
    # 1 pierna de unos + 1 escalera de basto (7,8,9). Libre 11 de espadas
    # jugadores["Jugador_1"] = [[(7, 'basto'), (1, 'copa'), (1, 'oro'), (8, 'basto'), (9, 'basto'), (1, 'espada'), (11, 'espada')], [], [(7, 'basto'), (1, 'copa'), (1, 'oro'), (8, 'basto'), (9, 'basto'), (1, 'espada'), (11, 'espada')], 0, True] 

    # 1 escalera de copas(1,2,3) + 1 escalera de basto (7,8,9). Libre 11 de espadas
    # jugadores["Jugador_1"] = [[(7, 'basto'), (1, 'copa'), (2, 'copa'), (8, 'basto'), (9, 'basto'), (3, 'copa'), (11, 'espada')], [], [(7, 'basto'), (1, 'copa'), (2, 'copa'), (8, 'basto'), (9, 'basto'), (3, 'copa'), (11, 'espada')], 0, True]

    # 2 escalera de basto(1,2,3) y (7,8,9). Libre 11 de espadas
    jugadores["Jugador_1"].mano = [(1, 'basto'), (2, 'basto'), (3, 'basto'), (4, 'basto'), (7, 'basto'),  (8, 'basto'), (9, 'basto')]
    # jugadores["Jugador_2"].puntos= 95

    # CHINCHON
    # jugadores["Jugador_1"] = [[(1, 'basto'), (2, 'basto'), (3, 'basto'), (4, 'basto'), (5, 'basto'),  (6, 'basto'), (7, 'basto')], [], [], 0, True]
    
def acomodar_descarte(carta, deck):
    """
    acomodo la primer carta del descarte para probar programa
    """
    deck.descarte.append(carta)
    return
        
# Arranque
if __name__ == "__main__":
    run()
