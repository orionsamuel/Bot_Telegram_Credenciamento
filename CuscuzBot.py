import re
import telegram


from telegram import User, InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram.utils.helpers import escape_markdown

botToken = "919748657:AAE95fqJ9pppzMFMqgZ3bHUj_tL1PmdVfkk"

cuscuzbot = telegram.Bot(botToken)

def buscar(update, context):
    arquivoInscritos = open("/home/samuel/cuscuzhq.csv", "r+")
    inscritos = arquivoInscritos.readlines()
    for linha in inscritos:
        if(re.search(str(context.args[0]), linha, re.IGNORECASE)):
           update.message.reply_text(linha)
    arquivo.close()


def checkin(update, context):
    arquivoInscritos = open("/home/samuel/cuscuzhq.csv", "r+")
    arquivoPresentesLeitura = open("/home/samuel/checkin.txt", "r+")
    
    presentes = arquivoPresentesLeitura.readlines()
    numLinhas = sum(1 for linha in presentes)
    
    arquivoPresentesLeitura.close()
    
    arquivoPresentes = open("/home/samuel/checkin.txt", "a+")
    inscritos = arquivoInscritos.readlines()    
    escolhido = inscritos[int(context.args[0]) - 1]
    escolhidoSeparado = escolhido.split(',')

    arquivoInscritos.close()

    arquivoPresentes.write(str((numLinhas + 1 )) + " " + str(escolhidoSeparado[1]) + " " + str(escolhidoSeparado[2]))

    arquivoPresentes.close()

    update.message.reply_text("Check-in realizado com sucesso!")

def cadastro(update, context):
    arquivoPresentesLeitura = open("/home/samuel/checkin.txt", "r+")
    
    presentes = arquivoPresentesLeitura.readlines()
    numLinhas = sum(1 for linha in presentes)
    
    arquivoPresentesLeitura.close()
    
    arquivoPresentes = open("/home/samuel/checkin.txt", "a+")

    arquivoPresentes.write(str((numLinhas + 1 )))
    for i in range(len(context.args)):
        arquivoPresentes.write(" " + str(context.args[i]))

    arquivoPresentes.write("\n")

    arquivoPresentes.close()

    update.message.reply_text("Cadastro realizado com sucesso!")


def presentes(update, context):
    arquivoPresentesLeitura = open("/home/samuel/checkin.txt", "r+")
    
    for linha in arquivoPresentesLeitura:
        update.message.reply_text(linha)

    arquivoPresentesLeitua.close()

def sorteado(update, context):
    arquivoPresentesLeitura = open("/home/samuel/checkin.txt", "r+")
    linha = ""
    for linha in arquivoPresentesLeitura:
        pessoaSorteada = linha.split(' ')
        if(pessoaSorteada[0] == context.args[0]):
            update.message.reply_text(linha)

    arquivoPresentesLeitua.close()


def ajuda(update, context):
    update.message.reply_text("Esse bot foi criado para ajudar com o credenciamento do evento Cuscuz HQ. \n" +
                              "Abaixo se encontram os comandos disponíveis e suas formas de utilização. \n" + "\n" +
                              "/buscar - Busca um participante na lista de inscritos. ao usar o comando deve-se passar o nome do comando + nome do participante. Ex: /buscar Antônio \n" + "\n" +
                              "/checkin - Realiza o check-in de um participante já cadastrado. Depois de buscado um participante, a pesquisa trará um número de inscrição, o comando checkin utiliza ele número para registrar a presença do participante. Ex: /checkin 22 \n" + "\n" +
                              "/cadastro - Realiza o cadastro de um participante ainda não inscrito e já faz o check-in imediatamente, dispensando o outro comando. Deve-se usar passando o comando, o nome do participante e telefone. Ex: /cadastro José Pereira de Souza 998903344 \n" + "\n" +
                              "/presentes - Mostra todos os participantes presentes ordenados pela chegada do participante no evento. O comando deve ser usado sozinho sem nenhum parâmetro. Ex: /presentes \n" + "\n" +
                              "/sorteado - Mostra uma pessoa que foi sorteada. O comando deve receber como parâmetro o número sorteado que equivale ao número da ordem de chegada do participante. O comando tem como retorno o nome e telefone do participante sorteado. Ex: /sorteado 3 \n" + "\n" +
                              "/help - Lista todos os comandos e suas descrições")



def main():
    updater = Updater(botToken, use_context=True)

    dp = updater.dispatcher
    
    #Comandos
    dp.add_handler(CommandHandler("buscar", buscar, pass_args=True))
    dp.add_handler(CommandHandler("checkin", checkin, pass_args=True))
    dp.add_handler(CommandHandler("cadastro", cadastro, pass_args=True))
    dp.add_handler(CommandHandler("presentes", presentes, pass_args=True))
    dp.add_handler(CommandHandler("sorteado", sorteado, pass_args=True))
    dp.add_handler(CommandHandler("help", ajuda, pass_args=True))

    
    # Start the Bot
    updater.start_polling()
    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
