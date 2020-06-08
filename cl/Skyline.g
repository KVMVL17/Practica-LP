grammar Skyline;

root: (creacio | assig | operador ) EOF;

creacio: simple | composta | aleatori;

simple: '(' NUM ',' NUM ',' NUM ')' (',')?;

composta: '[' simple* ']';

aleatori: '{' NUM ',' NUM ',' NUM ',' NUM ',' NUM '}';

assig: ID ':=' (creacio | operador);

operador: '(' operador ')'
        | '-' operador
        | operador '*' (NUM | operador)
        | operador '+' operador
        | operador ('+' | '-') NUM
        | (ID | creacio)
        ;

ID : [a-zA-Z][a-zA-Z0-9]*;
NUM : [0-9]+;
WS : [\r]*[ \n]+ -> skip;
