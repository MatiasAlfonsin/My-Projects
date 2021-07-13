

class Carta(object):
    def __init__(self, numero, palo, tapada=False) -> None:
        self.__numero = int(numero)
        self.__palo = int(palo)
        self.__tapada = bool(tapada)

    def tapar(self) -> None:
        self.__tapada = True

    def destapar(self) -> None:
        self.__tapada = False

    def is_tapada(self):
        return self.__tapada == True

    def get_numero(self) -> int:
        return self.__numero

    def get_palo(self) -> int:
        return self.__palo

    def set_numero(self, numero) -> None:
        self.__numero = numero

    def set_palo(self, palo) -> None:
        self.__palo = palo

    def __str__(self) -> str:
        return "[{}{}]".format(self.dibujo_numero(), self.dibujo_palo())
        
    def dibujo_numero(self):
        pass

    def dibujo_palo(self):
        pass


class Carta_poker(Carta):
    def __init__(self, numero, palo, tapada=False) -> None:
        super().__init__(numero, palo, tapada)

    def dibujo_numero(self) -> str:
        cadena = ''
        numeros_posibles = ['#', 'A', '2', '3', '4',
                            '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        if self.is_tapada():
            cadena = numeros_posibles[0]
        else:
            cadena = numeros_posibles[self.get_numero()]

        return cadena

    def dibujo_palo(self):
        cadena = ''
        palos_posibles = ['#', '♥', '♦', '♣', '♠']
        if self.is_tapada():
            cadena = palos_posibles[0]
        else:
            cadena = palos_posibles[self.get_palo()]

        return cadena

    def es_figura(self) -> bool:
        es = False
        if self.get_numero() > 10:
            es = True
        return es


def main():
    c = Carta_poker(2, 3)
    print(c)
    if c.is_tapada():
        c.destapar()
    else:
        c.tapar()
    print(c)


if __name__ == "__main__":
    main()
