import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy

matplotlib.use('agg')


class Skyline:
    yMax = 0
    xMax = 0
    area = 0

    def __init__(self):
        self.edificis = []

    def afegirEdifici(self, edifici):
        """S'afegeix l'edifici passat per paràmetre a la instància"""

        if self.yMax < edifici[1]:
            self.yMax = edifici[1]
        if self.xMax < edifici[2]:
            self.xMax = edifici[2]
        self.edificis.append(edifici)
        self.area += (edifici[2]-edifici[0])*edifici[1]

    def replicacio(self, num):
        """Es replica el numero passat per paràmentre
        els edificis de la instància self"""

        aux = []
        a = self.xMax-1
        for i in range(1, num):
            for x in self.edificis:
                ini = x[0] + (a*i)
                fin = x[2] + (a*i)
                aux.append([ini, x[1], fin])

        self.edificis += aux
        self.xMax = a*num + 1
        self.area *= num

    def mirall(self):
        """Retorna el mirall de la instància"""

        reversed(self.edificis)
        aux = self.xMax
        for x in self.edificis:
            amplada = x[2] - x[0]
            x[0] = (2*aux - x[2]) - (aux-1)
            x[2] = x[0] + amplada

    def unio(self, skyline):
        """Uneix els edificis de la pròpia instància amb la
        instància  skyline passada per paràmetre. L'àrea és la visible"""

        s = copy.deepcopy(self)
        s.interseccio(skyline)
        self.edificis += skyline.edificis
        if self.xMax < skyline.xMax:
            self.xMax = skyline.xMax
        if self.yMax < skyline.yMax:
            self.yMax = skyline.yMax

        self.area += skyline.area - s.area

    def interseccio(self, skyline):
        """Es fa intersecció dels edificis de la pròpia instància amb la
        instància skyline passada per paràmetre i es guarda en self.
        L'àrea és la intersecció"""

        edif = []
        amplada = 0
        altura = 0
        areaNew = 0
        for x in self.edificis:
            for y in skyline.edificis:
                if y[0] <= x[0] < y[2]:
                    aux = [max(x[0], y[0]), min(x[1], y[1]), min(x[2], y[2])]
                    edif.append(aux)
                    areaNew += (aux[2] - aux[0]) * aux[1]
                    if aux[2] > amplada:
                        amplada = aux[2]
                    if aux[1] > altura:
                        altura = aux[1]

                elif x[0] < y[0] < x[2]:
                    aux = [y[0], min(x[1], y[1]), min(x[2], y[2])]
                    edif.append(aux)
                    areaNew += (aux[2] - aux[0]) * aux[1]
                    if aux[2] > amplada:
                        amplada = aux[2]
                    if aux[1] > altura:
                        altura = aux[1]

        self.edificis = edif
        self.xMax = amplada
        self.yMax = altura
        self.area = areaNew

    def despl(self, num):
        """Desplaça horitzontalment els edificis de la pròpia instància
        el número de vegades passat per paràmetre (pot ser negatiu)"""

        for x in self.edificis:
            x[0] += num
            x[2] += num

        self.xMax += num

    def imprimirEdifici(self, path):
        """Crea una imatge gràfica del skyline de la
        pròpia instància en el path indicat al paràmetre"""

        fig = plt.figure()
        skyline = fig.add_subplot(111)

        for edifici in self.edificis:
            inici = edifici[0]
            final = edifici[2]
            altura = edifici[1]

            amplada = final - inici

            skyline.add_patch(patches.Rectangle((inici, 0), amplada, altura,
                                                color='red'))

        if self.yMax <= 20 and self.xMax >= self.yMax:
            plt.yticks(range(0, self.yMax + 1, 1))

        if self.xMax <= 20:
            plt.xticks(range(1, self.xMax + 1, 1))

        plt.margins(0.05, 0)

        x0, x1, y0, y1 = plt.axis()
        plt.axis((x0, x1, y0, y1 + y1 * 0.05))
        plt.savefig(path)