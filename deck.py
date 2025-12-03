"""tenemos que poner algo aca"""
from __future__ import annotations
from typing import List, Tuple, Optional
import random
Card = Tuple[int, str]
DeckList = List[Card]
class Cartas:
    """Operaciones sobre mazo y descarte."""
    def __init__(self):
        self.mazo = None
        self.descarte = None


    def mezclar_mazo(self) -> None:
        """Mezcla el mazo in-place."""
        random.shuffle(self.mazo)

    #----------------------------------------
    # iniciar_descarte(self)
    #----------------------------------------
    def iniciar_descarte(self) -> DeckList:
        """
        Inicia pila de descarte: quita la última carta del mazo y la devuelve en una lista.
        Modifica `mazo` in-place.
        """
        m : DeckList = self.mazo
        if not m:
            return []
        primer_carta = m.pop()
        return [primer_carta]

    #----------------------------------------
    # robar_carta_mazo(self)
    #----------------------------------------
    def robar_carta_mazo(self) -> Optional[Card]:
        """Saca la última carta del mazo y la devuelve o None si no hay."""
        m : DeckList = self.mazo
        if not m:
            return None
        return m.pop()

    #----------------------------------------
    # robar_carta_descarte()
    #----------------------------------------
    def robar_carta_descarte(self) -> Optional[Card]:
        """Saca la última carta del descarte y la devuelve o None si no hay."""
        d : DeckList = self.descarte
        if not d:
            return None
        return d.pop()

    #----------------------------------------
    # rearmar_mazo_del_descarte()
    #----------------------------------------
    def rearmar_mazo_del_descarte(self) -> None:
        """
        Vuelca el descarte en el mazo mezclado (in-place).
        Nota: si el descarte está vacío no hace nada.
        """
        m : DeckList = self.mazo
        d : DeckList = self.descarte
        if not d:
            return
        random.shuffle(d)
        # mover todas las cartas del descarte al mazo
        m.extend(d)
        d.clear()

    #----------------------------------------
    # crear_mazo()
    #----------------------------------------
    @staticmethod
    def crear_mazo() -> DeckList:
        """Crea mazo de cartas españolas (1..12 por cada palo)."""
        palos = ["oro", "espada", "basto", "copa"]
        valores = list(range(1, 13))
        mazo = [(valor, palo) for palo in palos for valor in valores]
        return mazo

    #----------------------------------------
    # levantar_carta()
    #----------------------------------------
    def levantar_carta(self) -> Optional[Card]:
        """
        Interacción con el usuario para levantar carta de M(azo) o D(escarte).
        Mantiene la misma interfaz que el código original.
        """
        print("\nLevantando carta...")
        pila = ""
        m : DeckList = self.mazo
        d : DeckList = self.descarte
        while pila == "":
            top_desc = d[-1] if d else None
            entrada = input(f'Elegir (M)azo | (D)escarte {top_desc}?: ')
            if not entrada:
                print("\nError: No ingresaste nada.\nVolvé a intentar...\n")
                continue
            pila = entrada[0].upper()
            if pila == "M":
                carta = self.robar_carta_mazo()
            elif pila == "D":
                carta = self.robar_carta_descarte()
            else:
                print("\nError: Opción no válida. Volvé a intentar...\n")
                pila = ""
                continue
            return carta
        return None