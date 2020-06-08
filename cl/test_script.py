from antlr4 import *
from .SkylineParser import SkylineParser
from .SkylineLexer import SkylineLexer
from .SkylineVisitor import SkylineVisitor


def get_Skyline(input):

    input_stream = InputStream(input)

    lexer = SkylineLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SkylineParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise Exception('Error de sintaxi')

    visitor = SkylineVisitor()
    return visitor.visit(tree)