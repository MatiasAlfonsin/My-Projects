from mazos import Mazo, Mazo_black_jack
from cartas import Carta, Carta_poker
from random import randint


class Jugador_cartas(object):
    def __init__(self, nombre, mazo) -> None:
        super().__init__()
        if not isinstance(mazo, Mazo):
            raise Exception("EL JUGADOR USA UN MAZO ")
        self.__nombre = str(nombre)
        self.__mano = mazo

    def get_nombre(self) -> str:
        return self.__nombre

    def get_mano(self) -> Mazo:
        return self.__mano

    def sacar(self) -> Carta:
        return self.get_mano().sacar()

    def poner(self, una_carta) -> None:
        self.get_mano().poner(una_carta)

    def tiene_cartas(self) -> bool:
        return self.get_mano().hay_cartas()

    def __str__(self) -> str:
        return "{} - {}  ".format(self.get_nombre(), str(self.get_mano()))


class jugador_black_jack(Jugador_cartas):
    def __init__(self, nombre) -> None:
        super().__init__(nombre, Mazo_black_jack())
        self.__suma_cartas = 0

    def get_suma_cartas(self):
        return self.__suma_cartas

    def set_suma_cartas(self, value):
        self.__suma_cartas = value

    def get_mano(self) -> Mazo_black_jack:
        return super().get_mano()

    def suma_cartas(self) -> int:
        return self.get_mano().suma_cartas()

    def __str__(self) -> str:
        return "{} {}".format(self.get_nombre(), str(self.get_mano()))

    def me_planto(self) -> bool:
        raise Exception("EL JUGADOR DE BLACK JACK NO SE PUEDE INSTANCIAR")


class Croupier(jugador_black_jack):
    def __init__(self, nombre) -> None:
        super().__init__(nombre)

    def me_planto(self, primera_vez=False) -> bool:
        respuesta = False
        suma = self.get_mano().suma_cartas(primera_vez, self.get_suma_cartas())
        self.set_suma_cartas(suma)
        print("Suma: ", suma)
        if suma > 21:
            respuesta = True
        elif suma > 17:
            print("Se planto")
            respuesta = True
        return respuesta


class Cliente(jugador_black_jack):
    def __init__(self, nombre, fichas) -> None:
        super().__init__(nombre)
        self.__fichas = fichas

    def get_fichas(self) -> int:
        return self.__fichas

    def perder(self, fichas) -> None:
        self.__fichas -= fichas

    def ganar(self, fichas) -> None:
        self.__fichas += fichas

    def tiene_fichas(self) -> bool:
        tiene = False
        if self.get_fichas() > 0:
            tiene = True
        return tiene

    def me_planto(self) -> bool:
        raise Exception("EL JUGADOR CLIENTE NO SE PUEDE INSTANCIAR")

    def apostar(self) -> int:
        raise Exception("EL JUGADOR CLIENTE NO SE PUEDE INSTANCIAR")


class Computadora(Cliente):
    #   1 TRANQUILO
    # 100 COMO LOCO

    def __init__(self, nombre, fichas) -> None:
        super().__init__(nombre, fichas)
        self.__personalidad = randint(1, 100)

    def __pensar(self) -> int:
        return randint(1, 100)

    def me_planto(self, primera_vez=False) -> bool:
        respuesta = False
        suma = self.get_mano().suma_cartas(primera_vez, self.get_suma_cartas())
        self.set_suma_cartas(suma)
        print("Suma: ", suma)
        if suma >= 21:
            respuesta = True
        elif suma > 10:
            if(self.__pensar() > self.__personalidad):
                respuesta = True
                print(self.get_nombre(), "se planto")
            else:
                print(self.get_nombre(), "pide otra carta")
        else:
            print(self.get_nombre(), "pide otra carta")
        return respuesta

    def apostar(self) -> int:
        print("Fichas: ", self.get_fichas())
        cantidad = randint(1, self.get_fichas())
        print("Apuesta:", cantidad)
        return cantidad


class Humano(Cliente):

    def __init__(self, nombre, fichas) -> None:
        super().__init__(nombre, fichas)
        self.__suma_cartas = 0

    def get_suma_cartas(self):
        return self.__suma_cartas

    def set_suma_cartas(self, value):
        self.__suma_cartas = value

    def me_planto(self, primera_vez=False) -> bool:
        respuesta = False
        suma = self.get_mano().suma_cartas(primera_vez, self.get_suma_cartas())
        self.set_suma_cartas(suma)
        print("Suma: ", suma)
        if suma >= 21:
            respuesta = True
        else:
            respuesta = input("SE PLANTA [S/N]: ").upper() == 'S'

        return respuesta

    def apostar(self) -> int:
        print("Fichas: ", self.get_fichas())
        cantidad = int(input("Cuanto apuesta: "))
        return cantidad


def main():
    j = jugador_black_jack("Mengano")
    j.poner(Carta_poker(2, 2))
    j.poner(Carta_poker(1, 4))
    j.poner(Carta_poker(3, 3))
    j.poner(Carta_poker(1, 1))

    print(j)


if __name__ == "__main__":
    main()
