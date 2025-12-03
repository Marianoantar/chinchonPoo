from __future__ import annotations
from typing import List, Tuple, Dict, Union, Optional, Any
Card = Tuple[int, str]
PlayerData = List[Any]  # [mano, juegos, libres, puntos, condicion]
PlayerKey = Union[str, int]
PlayersDict = Dict[PlayerKey, PlayerData]
def reporte(cartas: List[Card]) -> Optional[Tuple[Dict[int, int], Dict[str, List[int]]]]:
    """
    Recibe entre 3 y 8 cartas y devuelve (repeticiones, palos)
    repeticion: {numero: veces}
    palos: {palo: [valores]}
    """
    if len(cartas) < 3 or len(cartas) > 8:
        return None
    repeticiones: Dict[int, int] = {}
    palos: Dict[str, List[int]] = {}
    for carta in cartas:
        numero, palo = carta
        repeticiones[numero] = repeticiones.get(numero, 0) + 1
        palos.setdefault(palo, []).append(numero)
    return repeticiones, palos
def hay_escalera(palos: Dict[str, List[int]]) -> Tuple[bool, Dict[str, List[List[int]]], bool]:
    """
    Comprueba si hay escalera(s) por palo.
    Devuelve (es_escalera, escaleras_por_palo, chinchon_flag)
    """
    chinchon = False
    es_escalera = False
    escaleras: Dict[str, List[List[int]]] = {}
    for palo, numeros in palos.items():
        lista_de_numeros = sorted(numeros)
        if len(lista_de_numeros) < 3:
            continue
        secuencias: List[List[int]] = []
        temp: List[int] = [lista_de_numeros[0]]
        for i in range(1, len(lista_de_numeros)):
            if lista_de_numeros[i] == lista_de_numeros[i - 1] + 1:
                temp.append(lista_de_numeros[i])
            else:
                if len(temp) >= 3:
                    secuencias.append(temp)
                temp = [lista_de_numeros[i]]
        if len(temp) >= 3:
            secuencias.append(temp)
        if any(len(s) == 7 for s in secuencias):
            chinchon = True
        if secuencias:
            escaleras[palo] = secuencias
            es_escalera = True
    return es_escalera, escaleras, chinchon


def analizar(jugador: List[Any]) -> bool:
    """
    Analiza la mano del jugador (estructura original)
    jugador: [mano, posibles_juegos, cartas_libres, puntos_acumulados, sigue_jugando]
    Retorna True si hay chinchon (flag).
    """
    cartas = jugador.mano.copy()
    libres = jugador.mano.copy()
    jugador.juegos = []
    k = reporte(cartas)
    if k is None:
        jugador.libres = libres.copy()
        return False
    repeticiones, palos = k
    # tripletas y cuartetos
    for repeticion, veces in repeticiones.items():
        if veces >= 3:
            pierna = [c for c in jugador.mano if c[0] == repeticion]
            juego: List[Card] = []
            for carta in pierna:
                juego.append(carta)
                try:
                    libres.remove(carta)
                except ValueError:
                    pass
            jugador.juegos.append(juego)
    # escaleras
    escalera, cartas_escalera, chinchon = hay_escalera(palos)
    if escalera:
        for palo, secuencias in cartas_escalera.items():
            for lista in secuencias:
                juego = []
                for numero in lista:
                    carta = (numero, palo)
                    try:
                        libres.remove(carta)
                    except ValueError:
                        pass
                    juego.append(carta)
                jugador.juegos.append(juego)
        jugador.libres = libres.copy()
    else:
        jugador.libres = libres.copy()
    return chinchon


def analizar_cortar(jugador) -> Tuple[bool, Optional[Card]]:
    """
    Determina si puede cortar: si no quedan libres => puede cortar (pero no hay carta para devolver).
    Si quedan libres, calcula puntos y devuelve True/False y la carta candidata a cortes (la mayor).
    """
    print("\nAnalizando para cortar...")
    libres: List[Card] = jugador.libres
    if len(libres) == 0:
        return True, None
    libres_ordenadas = sorted(libres)
    carta = libres_ordenadas.pop()
    puntos = jugador.contar_puntos()
    return (True if puntos <= 7 else False), carta