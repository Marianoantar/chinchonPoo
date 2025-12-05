from __future__ import annotations
from typing import Dict, List, Tuple, Union, Any
import os
from deck import *
from players_manager import (
mostrar_cartas,
reiniciar_jugadores,
descartar,
proceso_descartar
)
from evaluador import *
Card = Tuple[int, str]
PlayerData = List[Any]  # [mano, juegos, libres, puntos, condicion]
PlayerKey = Union[str, int]
PlayersDict = Dict[PlayerKey, PlayerData]
def borrar_pantalla() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def mostrar_encabezado_turno(jugador: PlayerKey) -> None:
    print()
    print("*" * 41)
    print(f"       SIGUIENTE TURNO - {jugador}")
    print("*" * 41)


def repartir_cartas(jugadores: PlayersDict, deck : Any) -> None:
    for _round in range(7):
        for nombre, jugador in jugadores.items():
            if len(deck.mazo) == 0:
                print(
                    "*" * 20
                    + "\n El mazo quedó sin cartas\n Mezclando y generando mazo del descarte\n"
                    + "*" * 20
                )
                deck.rearmar_mazo_del_descarte()
            carta = deck.robar_carta_mazo()
            jugador.mano.append(carta)
            jugador.libres.append(carta)
            
            
def barajar_y_dar(jugadores: PlayersDict) -> Tuple[List[Card], List[Card]]:
    deck = Cartas()
    
    # Iniciar mazo
    deck.mazo = deck.crear_mazo()
    print("- Mazo Iniciado!!!")
    
    # Mezclar mazo
    random.shuffle(deck.mazo)
    print("- Mazo mezclado!!!")
    
    # Iniciar descarte
    deck.descarte = deck.iniciar_descarte()
    
    # repartir cartas
    repartir_cartas(jugadores, deck)
    # iniciar pila de descarte
    return deck


def mostrar_tabla_puntos(jugadores: PlayersDict) -> None:
    print()
    print("*" * 41)
    print(f"************ TABLA DE PUNTOS ************")
    for nombre, jugador in jugadores.items():
        print(f". {nombre}      {jugador.puntos} puntos - condicion en el juego: {jugador.condicion}")


def contar_jugadores_ok(jugadores: PlayersDict) -> List[PlayerKey]:
    return [nombre for nombre, jugador in jugadores.items() if jugador.condicion]


def cortar(nombre: PlayerKey, jugadores: PlayersDict) -> int:
    print(f"\n***** Iniciando Proceso de Corte de {nombre} *****\n")
    for jugador_nombre, jugador in jugadores.items():
        puntos_sumados = jugador.contar_puntos()
        jugador.puntos += puntos_sumados
        jugador.chequear_puntos()
    mostrar_tabla_puntos(jugadores)
    jugadores_ok = contar_jugadores_ok(jugadores)
    return len(jugadores_ok)
    ## el flujo del juego


def comienzo_juego(jugadores: PlayersDict, deck) -> None:
    print("\n***********************************************")
    print("************** COMIENZO DE JUEGO **************")
    print("***********************************************\n")
    chinchon: Dict[str, Union[bool, PlayerKey]] = {}
    chinchon["chinchon"] = [False, ""]
    descarte = deck.descarte
    mazo = deck.mazo

    while sum(1 for jugador in jugadores if jugadores[jugador].condicion) > 1 and not chinchon["chinchon"][0]:
        print("\n************** COMIENZO DE RONDA **************\n")
        mostrar_cartas(jugadores)
        print("\nCarta visible en pila de descarte: ", descarte[-1] if descarte else None)
        print("Cantidad de cartas en descarte: ", len(descarte))
        print("Cantidad de cartas en el mazo: ", len(mazo))
        corte = False
        while not corte:
            for nombre_jugador in jugadores:
                mostrar_encabezado_turno(nombre_jugador)
                if analizar(jugador=jugadores[nombre_jugador]):
                    chinchon["chinchon"] = [True, nombre_jugador]
                jugador = jugadores[nombre_jugador]
                jugador.mostrar_cartas_mano()
                while True:
                    carta = deck.levantar_carta()
                    if carta is None:
                        deck.rearmar_mazo_del_descarte()
                        continue
                    print(f"\n  .Carta levantada: {carta}\n")
                    break
                jugador.recibir_carta(carta)
                if analizar(jugador=jugador):
                    chinchon["chinchon"] = [True, nombre_jugador]
                jugador.mostrar_cartas_mano()
                puede_cortar, carta_corte = analizar_cortar(jugador)
                if puede_cortar:
                    print(f"\n¡¡¡¡¡¡ {jugador.nombre} ya puede cortar !!!!!\n")
                    decision = input(f"Quiere cortar(1) o seguir jugando(enter): ")
                    if decision == "1":
                        descartar(carta_corte, descarte, jugador)
                        corte = True
                        break
                if not corte:
                    print(f"{jugador.nombre} NO puede cortar\n")
                    proceso_descartar(jugador, descarte)
            if corte:
                cortar(jugador.nombre, jugadores)
        jugadores_ok = contar_jugadores_ok(jugadores)
        if len(jugadores_ok) == 1:
            print(f"\n************** El ganador es: {jugadores_ok} **************\n")
            break
        elif chinchon["chinchon"][0]:
            ganador = chinchon["chinchon"][1]
            print(f"\n************** El ganador es: {ganador} **************\n")
            print("HA FORMADO CHINCHON!!!!!!!!!!!!!!!!")
            break
        seguir = input("Para seguir con la siguiente ronda pulsar enter(ingresa x para salir): ")
        if seguir.upper() == "X":
            print("Elegiste salir del juego")
            break
        borrar_pantalla()
        reiniciar_jugadores(jugadores)
        mazo, descarte = barajar_y_dar(jugadores)
    print("\n************** FIN DE JUEGO **************\n")
