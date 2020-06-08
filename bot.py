# importa l'API de Telegram
import os
import pickle

from cl.SkylineVisitor import *
from cl.test_script import get_Skyline
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# defineix /start
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="SkylineBot!\n" + "Benvingut " +
                                  update.message.chat.first_name + " !")
    context.user_data = {}


# defineix /author
def author(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Autor: " + "Kamal El Hachmi\n" +
                                  "Correu: kamal.el.hachmi@est.fib.upc.edu")


# defineix /help
def help_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="El propòsit " +
                                  "d'aquest bot és dissenyar al teu gust un " +
                                  "skyline, una vista horitzontal d'edificis.")
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Els operadors:\n" + "skyline + skyline: " +
                                  "unió.\n" + "skyline * skyline: intersec" +
                                  "ció.\nskyline * N: replicació N vegades " +
                                  "de l'skyline.\n" + "skyline +/- N: despla" +
                                  "çament a la dreta o esquerra N posicions.\n"
                                  "- skyline: retorna l'skyline reflectit.")
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Les comandes" + " possibles són:\n/start" +
                                  "\n/help\n/author\n/lst\n/clean\n/save" +
                                  "\n/clean\n/save <id> \n/load <id>")


# defineix /lst
def showIDs(update, context):
    dic = context.user_data
    if len(dic) == 0:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="No hi ha cap identificador definit.")
    else:
        out = ""
        for x in dic:
            aux = "- Id :  %s , area: %d \n" % (x, dic[x].area)
            out += aux
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Llistat d'identificadors definits:")
        context.bot.send_message(chat_id=update.message.chat_id, text=out)


# defineix /clean
def cleanIDs(update, context):
    context.user_data.clear()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="S'ha netejat el llistat " +
                                  "d'identificadors correctament.")


# defineix /save
def guardar(update, context):
    """S'encarrega de guardar el skyline amb l'identificador passat per
    paràmetre, dins una carpeta que té com a nom l'ID de l'usuari."""

    id = update.message.text[6:]
    if len(id) == 0:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Introdueix un nom")
    else:
        if id not in context.user_data:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="No hi ha cap skyline amd ID: " + id)
        else:
            nameFolder = str(update.effective_chat.id)
            if not os.path.exists(nameFolder):
                os.makedirs(nameFolder)

            nameFolder += '/' + id + '.sky'
            pickle.dump(context.user_data[id], open(nameFolder, "wb"))
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="S'ha guardat '" + id +
                                          "' correctament")


# defineix /load
def carregar(update, context):
    """S'encarrega de carregar el skyline amb l'identificador
    passat per paràmetre. Si no es troba, retorna un missatge d'error"""

    id = update.message.text[6:]
    if len(id) == 0:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Introdueix un nom")
    else:
        nameFolder = str(update.effective_chat.id) + '/' + id + '.sky'
        if not os.path.exists(nameFolder):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="No s'ha trobat cap arxiu " + id +
                                          ".sky")
        else:
            context.user_data[id] = pickle.load(open(nameFolder, "rb"))
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="S'ha carregat '" + id +
                                          "' correctament")


# defineix com processar les gràfiques
def imprimir(update, context):
    """S'encarrega de processar els missatges
    sense '/' i contesta en funció del missatge, si hi ha hagut
    un error, retorna un missatge, si no és el cas, retorna una
    imatge del skyline"""

    SkylineVisitor.guardarDades(context.user_data)

    message = update.message.text

    try:
        skyline = get_Skyline(message)

    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))
        return

    except:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Ha passat algun error")
        return

    image = 'grafica.png'
    skyline.imprimirEdifici(image)

    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo=open(image, 'rb'))

    context.bot.send_message(chat_id=update.message.chat_id,
                             text="area: %d\nalçada: %d" %
                                  (skyline.area, skyline.yMax))

    os.remove(image)

    context.user_data.update(SkylineVisitor.listarIDs())

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objecte per treballar amb Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('lst', showIDs))
dispatcher.add_handler(CommandHandler('clean', cleanIDs))
dispatcher.add_handler(CommandHandler('save', guardar))
dispatcher.add_handler(CommandHandler('load', carregar))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command),
                                      imprimir))

# engega el bot
updater.start_polling()