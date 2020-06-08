# Generated from Skyline.g by ANTLR 4.7.2
from antlr4 import *
from skyline import *
import copy
import random
if __name__ is not None and "." in __name__:
    from .SkylineParser import SkylineParser
else:
    from SkylineParser import SkylineParser

# This class defines a complete generic visitor
# for a parse tree produced by SkylineParser.


class SkylineVisitor(ParseTreeVisitor):

    dades = {}

    # Visit a parse tree produced by SkylineParser#root.
    def visitRoot(self, ctx: SkylineParser.RootContext):
        n = next(ctx.getChildren())
        return self.visit(n)

    # Visit a parse tree produced by SkylineParser#creacio.
    def visitCreacio(self, ctx: SkylineParser.CreacioContext):
        n = next(ctx.getChildren())
        return self.visit(n)

    # Visit a parse tree produced by SkylineParser#simple.
    def visitSimple(self, ctx: SkylineParser.SimpleContext):
        l = [n for n in ctx.getChildren()]

        ini = int(l[1].getText())
        altura = int(l[3].getText())
        fi = int(l[5].getText())
        sky = Skyline()
        sky.afegirEdifici([ini, altura, fi])
        return sky

    # Visit a parse tree produced by SkylineParser#composta.
    def visitComposta(self, ctx: SkylineParser.CompostaContext):
        l = [n for n in ctx.getChildren()]
        sky = Skyline()
        if len(l) > 2:
            for simp in l[1:len(l)-1]:
                sky.unio(self.visit(simp))

        return sky

    # Visit a parse tree produced by SkylineParser#aleatori.
    def visitAleatori(self, ctx: SkylineParser.AleatoriContext):
        l = [n for n in ctx.getChildren()]
        sky = Skyline()
        n = int(l[1].getText())
        h = int(l[3].getText())
        w = int(l[5].getText())
        xmin = int(l[7].getText())
        xmax = int(l[9].getText())
        if xmin >= xmax:
            raise Exception("Error, xmin és més gran que xmax")
        else:
            for x in range(n):
                h2 = random.randint(0, h)
                w2 = random.randint(1, w)
                ini = random.randint(xmin, (xmax-w2))
                sky.afegirEdifici([ini, h2, ini+w2])

        return sky

    # Visit a parse tree produced by SkylineParser#assig.
    def visitAssig(self, ctx: SkylineParser.AssigContext):
        l = [n for n in ctx.getChildren()]
        self.dades[l[0].getText()] = self.visit(l[2])
        return self.dades[l[0].getText()]

    # Visit a parse tree produced by SkylineParser#operador.
    def visitOperador(self, ctx: SkylineParser.OperadorContext):
        if ctx.getChildCount() == 1:
            n = next(ctx.getChildren())
            sky = self.visit(n)
            if sky is None:
                if n.getText() not in self.dades:
                    raise Exception("No s'ha trobat cap identificador '%s'"
                                    % n.getText())
                else:
                    return copy.deepcopy(self.dades[n.getText()])

            else:
                return sky

        elif ctx.getChildCount() == 2:
            sky = self.visit(ctx.operador(0))
            sky.mirall()
            return sky

        else:
            l = [n for n in ctx.getChildren()]
            if l[0].getText() == '(':
                return self.visit(l[1])

            elif l[1].getText() == '+':
                sky1 = self.visit(l[0])
                sky2 = self.visit(l[2])
                if sky2 is not None:
                    sky1.unio(sky2)
                    return sky1
                else:
                    sky1.despl(int(l[2].getText()))
                    return sky1

            elif l[1].getText() == '-':
                sky = self.visit(l[0])
                aux = int(l[2].getText())
                sky.despl(-aux)
                return sky

            elif l[1].getText() == '*':
                sky1 = self.visit(l[0])
                sky2 = self.visit(l[2])
                if sky2 is not None:
                    sky1.interseccio(sky2)
                    return sky1
                else:
                    sky1.replicacio(int(l[2].getText()))
                    return sky1

    @staticmethod
    def listarIDs():
        return SkylineVisitor.dades

    @staticmethod
    def guardarDades(context):
        SkylineVisitor.dades = copy.deepcopy(context)

    @staticmethod
    def netajarIDs():
        SkylineVisitor.dades = {}

del SkylineParser