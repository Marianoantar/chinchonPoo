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
    Entra: jugador: [mano, posibles_juegos, cartas_libres, puntos_acumulados, sigue_jugando, nombre]
    Retorna True si hay chinchon (flag).
    """
    cartas = jugador.mano.copy()
    libres = jugador.mano.copy()
    jugador.juegos = []
    
    resultado_reporte = reporte(cartas)
    if resultado_reporte is None:
        jugador.libres = libres.copy()
        return False
    
    repeticiones, palos = resultado_reporte
    
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

# --------------------
# elegir_carta_para_cortar()
# --------------------
def elegir_carta_para_cortar(juegos):
    '''
    Funcion que elije una carta para cortar sacada desde los juegos
    Entra: juegos
    Sale carta
    '''
    posible_carta = (0,"")
    for indice, juego in enumerate(juegos):
        
        # Revisamos el primer juego que tenga MAS de 3 cartas
        if len(juego) > 3 and posible_carta[0] == 0:
            posible_carta = juego.pop() # Directamente le asigna la ultima carta del juego y la borra
            continue
        
        # Si hay otro juego de MAS de 3 cartas
        if len(juego) > 3:
            print(f"\nposible_carta[0]: {posible_carta[0]}") #!!!!!!!!
            print(f"juego[-1]: {juego[-1]} - juego[-1][0]: {juego[-1][0]}\n") #!!!!!!!!
            
            # Si la última carta del juego actual es mas alta que la que la del anterior
            # restituye la anterior a su juego y marca la actual para cortar
            if posible_carta[0] <  juego[-1][0]:
                juegos[indice-1].append(posible_carta)
                posible_carta = juego.pop()
    
    carta = posible_carta
    return carta

def analizar_cortar(jugador) -> Tuple[bool, Optional[Card]]:
    """
    Determina si puede cortar: si no quedan libres => puede cortar (pero no hay carta para devolver).
    Si quedan libres, calcula puntos y devuelve True/False y la carta candidata a cortes (la mayor).
    """
    se_puede_cortar = False
    
    print("\nAnalizando para cortar...")
    libres: List[Card] = jugador.libres
    
    # Analizar -----------------------------------------------------------------------------------------
    
    # Si queda 1 carta libre( habiendo levantado) PUEDE CORTAR
    if len(libres) == 1: 
        return [True, libres[0]]
    
    # Si habiendo levantado una carta y TODAS las cartas en mano mas la carta levantada 
    # entran en juegos entonces libres está vacía.
    # Habria que cortar con la una carta que 
    #   -no rompa un juego(la cuarta de una pierna)
    #   -la ultima de una escalera de MAS de 3 cartas
    if len(libres) == 0: 
        carta_para_cortar = elegir_carta_para_cortar(jugador.juegos)
        # Borrar de juegos la carta para cortar
        print(f"\nCarta para cortar: {carta_para_cortar}\n") #!!!!!!!
        return [True, carta_para_cortar]
    
    libres_ordenadas = sorted(libres)
    carta_para_cortar = libres_ordenadas.pop()
    
    # Contar puntos de libres_ordenadas ya que la carta mas alta de libres_ordenadas YA FUE BORRADA
    # y se usaría para cortar (carta)
    puntos = sum(carta[0] for carta in libres_ordenadas)
    
    return [(True if puntos <= 7 else False), carta_para_cortar]
    