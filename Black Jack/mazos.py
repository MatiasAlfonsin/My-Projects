from typing import SupportsRound
from cartas import Carta, Carta_poker
from random import shuffle, randint

class Mazo(object):
    def __init__(self) -> None:
        super().__init__()
        self.__las_cartas = []

    def get_las_cartas(self) -> list:
        return self.__las_cartas

    def poner(self, una_carta, index=None) -> None:
        if not isinstance(una_carta, Carta):
            raise TypeError("AL MAZO SOLO SE PUEDE AGREGAR CARTAS")
        if index == None:
            self.__las_cartas.append(una_carta)
        else:
            self.__las_cartas.insert(index, una_carta)

    def sacar(self, index=None) -> Carta:
        carta = None
        if index == None:
            carta = self.__las_cartas.pop(0)
        else:
            carta = self.__las_cartas.pop(index)
        return carta

    def ver(self, index=None) -> Carta:
        carta = None
        if index == None:
            carta = self.__las_cartas[0]
        else:
            carta = self.__las_cartas[index]
        return carta

    def isvacio(self) -> bool:
        return len(self.__las_cartas) == 0

    def hay_cartas(self) -> bool:
        return not self.isvacio()

    def mezclar(self) -> None:
        shuffle(self.__las_cartas)

    def __len__(self) -> int:
        return len(self.__las_cartas)

    def __str__(self) -> str:
        cadena = ""
        for carta in self.__las_cartas:
            cadena += str(carta)
        return cadena

    def llenar(self) -> None:
        raise Exception("NO SE PUEDE INSTANCIAR UN MAZO")

    def tapar(self):
        for carta in self.__las_cartas:
            carta.tapar()

    def destapar(self):
        for carta in self.__las_cartas:
            carta.destapar()


class Mazo_poker(Mazo):
    def __init__(self) -> None:
        super().__init__()

    def llenar(self) -> None:
        for numero in range(1, 14):
            for palo in range(1, 5):
                self.poner(Carta_poker(numero, palo))


class Mazo_black_jack(Mazo):
    def __init__(self) -> None:
        super().__init__()

    def llenar(self) -> None:
        for mazo in range(10):
            for numero in range(1, 14):
                for palo in range(1, 5):
                    self.poner(Carta_poker(numero, palo))

    def cantidad_unos(self):
        cantidad_unos = 0
        lista_cartas = self.get_las_cartas()
        for carta in lista_cartas:
            if carta.get_numero() == 1:
                cantidad_unos += 1
        return cantidad_unos

    def suma_cartas(self, primera_vez=False, suma_realizada=0) -> int:
        lista_cartas = self.get_las_cartas()
        cantidad_unos = self.cantidad_unos()
        if primera_vez:
            suma = 0
            suma_numeros = 0
            for carta in lista_cartas:
                numero = carta.get_numero()
                if numero < 10:
                    suma_numeros += numero
                else:
                    suma_numeros += 10

            if cantidad_unos == 0:
                suma = suma_numeros
            elif cantidad_unos == 1:
                if suma_numeros + 11 > 21:
                    suma = suma_numeros + 1
                else:
                    suma = suma_numeros + 11
            else:
                if suma_numeros + 11 + (cantidad_unos-1) > 21:
                    suma = suma_numeros + cantidad_unos
                else:
                    suma = suma_numeros + 11 + (cantidad_unos-1)
        else:
            suma = suma_realizada
            numero = lista_cartas[-1].get_numero()
            if numero == 1:
                if suma + 11 > 21:
                    suma += 1
                else:
                    suma += 11
            elif numero < 10:
                suma += numero
            else:
                suma += 10
        return suma

    def tiene_black_jack(self) -> bool:
        tiene = False
        lista = self.get_las_cartas()
        if len(lista) == 2:
            hay_figura = lista[0].es_figura() or lista[1].es_figura()
            hay_uno = lista[0].get_numero() == 1 or lista[1].get_numero() == 1
            tiene = hay_figura and hay_uno

        return tiene


def mezclar1(lista):
    for i in range(len(lista)*2):
        n = randint(0, len(lista)-1)
        elemento = lista.pop(n)
        lista.append(elemento)


def mezclar2(lista):
    for i in range(len(lista)*2):
        index_x = randint(0, len(lista)-1)
        index_y = randint(0, len(lista)-1)
        auxiliar = lista[index_x]
        lista[index_x] = lista[index_y]
        lista[index_y] = auxiliar


def mezclar3(lista):
    shuffle(lista)


def main():
    mb = Mazo_black_jack()
    mb.poner(Carta_poker(12, 2))
    mb.poner(Carta_poker(1, 3))
    mb.poner(Carta_poker(3, 1))
    mb.poner(Carta_poker(5, 4))
    mb.suma_cartas()


if __name__ == "__main__":
    main()
