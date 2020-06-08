# Pràctica d'LP
Pràctica Python per GEI-LP de la FIB - SkylineBot - Edició primavera 2020

Aquest és el projecte per l'assignatura LP edició primavera 2020 (en plena Era del Confinament). Com se sap, un _Skyline_ d'una ciutat és una vista horitzontal dels seus edificis, doncs el projecte consisteix en un chatbot en Telegram que permet la creació i manipulació de _Skylines_ mitjançant un intèrpret i també permet consultar, guardar i carregar _Skylines_ en arxius `.sky`.

## Getting Started

Aquestes instruccions us proporcionaran una còpia del projecte en funcionament a la vostra màquina local amb finalitats de desenvolupament i proves. Consulteu les notes per saber com obrir el projecte al vostre sistema.

### Prerequisites

Abans de posar en funcionament el projecte es requereix:

 - Instalar **Python 3**:
   * [Python 3](https://www.python.org/)
   
 - Altres requirements:
```
pip3 install -r requirements.txt
```
_Si no us funciona, utilitzeu `pip` en comptes de `pip3`_


Un cop instal·lat els requeriments anteriors, només faltaria instal·lar el **ANTLR4** per ser utilitzat en la part del compilador.
 - Descarregar el ANTLR4.jar file:
 
   * [jar file](https://www.antlr.org/download/antlr-4.8-complete.jar)
   * [Getting started](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md)

 - Install Python runtime:
 
   - `pip3 install antlr4-python3-runtime` or
   - `pip install antlr4-python3-runtime`

### Running

Dins de la carpeta principal es troban els seguents fitxers:

 - **_bot.py_** (Per gestionar el bot Telegram)
 - **_skyline.py_** (Per gestionar els skylines)
 - **_token.txt_** (fitxer text on es guarda el token del bot, en aquest cas el meu, **@CheaMs_bot**)
 - **_requirements.txt_** (fitxer text on es guarda les llibreries utiltizades)
 - **_`cl`_** (carpeta amb el contingut de la part de compiladors)
    - **_Skyline.g_** (Gramàtica)
    - **_test_script.py_** (Script per interectuar amb el Visitor)
    - **_test_visitor.py_** (**Copia correcte del SkylineVisitor**)

A la primera part del projecte s'havia de realitzar la part de compiladors que interpretés el llenguatge definit a l'[enunciat](https://github.com/gebakx/SkylineBot). S'ha fet una certa gramatica per aquest llenguatge per tal que es passes un _Skyline_ en format AST a una instancia de la classe **_skyline_**. 
Per poder compilar i executar aixo s'ha de fer el seguent:


1. Primer de tot s'ha de compilar la gramàtica Skyline.g amb ANTLR4 dins la carpeta **cl**.

```
antlr4 -Dlanguage=Python3 -no-listener -visitor Skyline.g
```

El visitor (_SkylineVisitor.py_) que ens crea aquesta comanda no és el que volem, ja que es troba buit, llavors que s'ha de canviar pel visitor **_test_visitor.py_**.

Per solucionar-ho:

- Copiem tot el contingut de test_visitor.py i el substituïm pel que es troba al fitxer SkylineVisitor.py 

  o sinó

- Utilitzar aquesta comanda:

```
cp test_visitor.py SkylineVisitor.py
```

Un cop fet, com es veurà en el visitor, hi ha un diccionari amb nom `dades` de tipus estàtic que s'encarrega de guardar les assignacions ID - Skyline. I sobre l'arxiu `test_script.py` conté la funció `get_Skyline()` que passat el text per paràmetre retorna una instància de la classe `skyline`.


A la segona part del projecte s'havia d'implementar un bot per Telegram (l'arxiu `bot.py`) per gestionar la comunicació entre BOT i l'usuari i complir el que demanava l'enunciat. També s'havia d'implementar la classe Skyline (l'arxiu `skyline.py`) per gestionar els edificis, hi ha una petita descripció en les funcions que conté.

Per probar el bot s'ha de executar la següent comanda desde la carpeta principal:

```
python3 bot.py
```

Un cop executat el bot estarà actiu. Si es va a l'aplicació Telegram i es busca `@CheaMs_bot` el trobarà, es diu Skyline (nom original), i ja pot interactuar amb ell.

### Functioning

El funcionament del bot és bastant senzill i es poden utilitzar totes les comandes descrites a l'[enunciat](https://github.com/gebakx/SkylineBot) de la pràctica. Tot i així té algunes excepcions com la tardança en la creació del _skyline_ random `{100000,20,3,1,10000}` en menys de 30 segons, difícil arreglar-lo. També el BOT `@CheaMs_bot` permet crear edificis un darrer l'altre, ja que no queda clar en l'enunciat.

Quan es posa en marxa el bot i l'usuari imprimeix un edifici, aquesta foto es guarda per un moment a la carpeta actual (principal) però s'esborra quasi instantàniament. 

El bot permet interactuar amb diferents usuaris a la vegada, cada usuari amb els seus skylines gràcies al `context.user_data`. A més a més, quan l'usuari fa un `/save`, es crea una carpeta com a nom l'id de l'usuari que és única en comptes de creació amb nom d'usuari, i allà es guarda el skyline o skylines que vulgui, d'aquesta manera, cada usuari interactuarà amb els seus `.sky`.

Si es voleu canviar el color del skyline per color més realista o el quin vulgueu, dirigiu-vos a la funció `imprimirEdifici` de la classe de `skyline.py` i canvieu-ho en l'apartat `color = `.
## Built With

* [Python](https://docs.python.org/3/) - Llenguatge utilitzat
* [Telegram](https://core.telegram.org/bots) - Aplicació del bot utilitzat
* [Matplotlib](https://matplotlib.org/) - Llibraria utilitzada per generar i mostrar els gràfics (_Skylines_)
* [Pickle](https://docs.python.org/3.6/library/pickle.html) - Utilitzada per guardar estructures de dades
* [PyCharm](https://www.jetbrains.com/es-es/pycharm/) - IDE utilitzada

## Authors

* **Kamal El Hachmi**

## Acknowledgments

* A tots aquells que m'han respost i ajudat a resoldre els dubtes que m'han anat sorgint durant la realització d'aquest projecte. Moltes gràcies.