from math import fabs
from jugadores import Humano, Computadora, Croupier, Cliente
from mazos import Mazo_black_jack


class Black_jack(object):
    def __init__(self) -> None:
        super().__init__()
        self.__el_mazo = Mazo_black_jack()
        self.__los_jugadores = []
        self.__el_croupier = Croupier("Sr Croupier")
        self.__las_apuestas = []

    def agregar_jugador(self, cliente) -> None:
        if not isinstance(cliente, (Humano, Computadora)):
            raise TypeError("SOLO SE PUEDEN AGREGAR CLIENTES")
        self.__los_jugadores.append(cliente)

    def eliminar_jugador(self, cliente) -> None:
        if not isinstance(cliente, (Humano, Computadora)):
            raise TypeError("SOLO SE PUEDEN ELIMINAR CLIENTES")
        self.__los_jugadores.remove(cliente)

    def jugar(self):
        self.__el_mazo.llenar()
        print("----- JUGADORES EN MESA -----")
        for x in self.__los_jugadores:
            print(str(x))
        while(self.__hay_jugadores_en_la_mesa()):
            self.__el_mazo.mezclar()
            self.__se_reparten_dos_cartas_a_los_jugadores()
            self.__se_reparten_dos_cartas_al_croupier()
            self.__los_jugadores_apuestan()
            self.__los_jugadores_juegan()
            self.__el_croupier_juega()
            self.__se_reparten_los_premios()
            self.__se_descartan_los_jugadores()
            self.__se_descarta_el_croupier()
            self.__se_retiran_los_jugadores_sin_fichas()
        self.__fin_del_juego()

    def __se_reparten_dos_cartas_a_los_jugadores(self) -> None:
        print("-----SE REPARTEN 2 CARTAS A LOS JUGADORES-----")
        for jug in self.__los_jugadores:
            jug.poner(self.__el_mazo.sacar())
            jug.poner(self.__el_mazo.sacar())

    def __se_reparten_dos_cartas_al_croupier(self) -> None:
        self.__el_croupier.poner(self.__el_mazo.sacar())
        carta = self.__el_mazo.sacar()
        carta.tapar()
        self.__el_croupier.poner(carta)

    def __los_jugadores_apuestan(self) -> None:
        self.__las_apuestas.clear()
        print("-----LOS JUGADORES APUESTAN-----")
        for jug in self.__los_jugadores:
            print("Apuesta: ", str(jug))
            self.__las_apuestas.append(jug.apostar())
            print("")

    def __los_jugadores_juegan(self) -> None:
        print("-----LOS JUGADORES JUEGAN-----")
        for jug in self.__los_jugadores:
            print("Juega: ", str(jug))
            primera_vez = True
            # suma_realizada = jug.get_mano().suma_cartas() #Here is the problem
            while not jug.me_planto(primera_vez):
                primera_vez = False
                jug.poner(self.__el_mazo.sacar())
                print(str(jug.get_mano()))
            print()

    def __el_croupier_juega(self) -> None:
        self.__el_croupier.get_mano().destapar()
        print("Juega:", str(self.__el_croupier))
        primera_vez = True
        while not self.__el_croupier.me_planto(primera_vez):
            print("pide otra carta")
            primera_vez = False
            self.__el_croupier.poner(self.__el_mazo.sacar())
            print(str(self.__el_croupier.get_mano()))

    def __se_reparten_los_premios(self) -> None:
        print("-----SE REPARTEN LOS PREMIOS-----")
        suma_croupier = self.__el_croupier.get_suma_cartas()
        suma_jugador = 0

        if suma_croupier > 21:
            print("SE PASO EL CROUPIER!!")
            for jug in self.__los_jugadores:
                print(str(jug), end='')
                suma_jugador = jug.get_suma_cartas()
                index_apuesta = self.__los_jugadores.index(jug)
                fichas_apostadas = self.__las_apuestas[index_apuesta]
                if suma_jugador > 21:
                    print(" PIERDE ==> SE PASO")
                    jug.perder(fichas_apostadas)
                else:
                    print(" GANA ==> SE PASO EL CROUPIER")
                    jug.ganar(2*fichas_apostadas)
        else:
            print("-----SE COMPARAN LAS JUGADAS-----")
            for jug in self.__los_jugadores:
                print(str(jug), end='')
                suma_jugador = jug.get_suma_cartas()
                index_apuesta = self.__los_jugadores.index(jug)
                fichas_apostadas = self.__las_apuestas[index_apuesta]
                if suma_jugador > 21:
                    print(" PIERDE ==> SE PASO")
                    jug.perder(fichas_apostadas)
                elif suma_croupier > suma_jugador:
                    print(" PIERDE ==> LE GANA EL CROUPIER")
                    jug.perder(fichas_apostadas)
                elif suma_croupier < suma_jugador:
                    print(" GANA ==> LE GANA AL CROUPIER")
                    jug.ganar(2*fichas_apostadas)
                else:  # EMPATE
                    bj_jug = jug.get_mano().tiene_black_jack()
                    bj_cro = self.__el_croupier.get_mano().tiene_black_jack()
                    if suma_croupier != 21:
                        print(" EMPATE!!")
                    elif bj_jug and not bj_cro:
                        print(" GANA ==> TIENE BLACK JACK")
                        jug.ganar(2*fichas_apostadas)
                    elif not bj_jug and bj_cro:
                        print(" PIERDE ==> EL CROUPIER TIENE BLACK JACK")
                        jug.perder(fichas_apostadas)
                    else:
                        print(" EMPATE!!")

    def __se_descartan_los_jugadores(self) -> None:
        print("")
        print("Se descartan los jugadores")
        for jug in self.__los_jugadores:
            while jug.get_mano().hay_cartas():
                self.__el_mazo.poner(jug.sacar())

    def __se_descarta_el_croupier(self):
        print("Se descarta el croupier")
        while self.__el_croupier.get_mano().hay_cartas():
            self.__el_mazo.poner(self.__el_croupier.sacar())

    def __se_retiran_los_jugadores_sin_fichas(self):
        print("Se retiran los jugadores sin fichas")
        print("")
        index = 0
        while index < len(self.__los_jugadores):
            jug = self.__los_jugadores[index]
            if not jug.tiene_fichas():
                print("SE RETIRA: ", jug.get_nombre())
                print("")
                self.eliminar_jugador(jug)
            else:
                index += 1

    def __hay_jugadores_en_la_mesa(self) -> bool:
        hay = False
        if len(self.__los_jugadores) > 0:
            hay = True
        return hay

    def __fin_del_juego(self):
        print("----- NO HAY MAS JUGADORES EN MESA, EL JUEGO HA FINALIZADO -----")


def main():
    juego = Black_jack()
    juego.agregar_jugador(Humano("Matias", 100))
    juego.agregar_jugador(Humano("Pirulo",100))
    juego.agregar_jugador(Computadora("Compu Uno", 100))
    # juego.agregar_jugador(Computadora("Compu Dos",100))
    juego.jugar()


main()
