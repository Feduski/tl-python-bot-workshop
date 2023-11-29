import os 
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
import logging
import requests

load_dotenv() #Cargamos las variables de entorno
tl_key = os.getenv('TELEGRAM_KEY') #Obtenemos la llave del bot
chat_id = os.getenv('CHAT_ID') #Obtenemos el id del chat

logging.basicConfig( #Configuramos el logging que nos brindará información
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soy un bot de Ejemplo") #Enviamos el mensaje al usuario
    logging.info(f'El usuario: ({update.message.chat.first_name}) ejecutó: start_command.') #Dejamos asentado por consola lo que pasó

async def bitcoin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bitcoin_ars = (requests.get("https://criptoya.com/api/lemoncash/btc/ars/0.1")).json() #recibimos el valor de bitcoin en ars 
    usdt = (requests.get("https://criptoya.com/api/lemoncash/usdt/ars/0.1")).json() #recibimos el valor de usdt en ars
    btc_usd = round(bitcoin_ars['totalBid'] / usdt['totalBid']) #dividimos y redondeamos el valor para obtener el precio de btc en usd.

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'El precio actual de Bitcoin es de: {btc_usd} USD') #Enviamos el mensaje al usuario
    logging.info(f'El usuario: ({update.message.chat.first_name}) ejecutó: bitcoin_command.') #Dejamos asentado por consola lo que pasó

async def bitcoin_job(context = ContextTypes.DEFAULT_TYPE):
    bitcoin_ars = (requests.get("https://criptoya.com/api/lemoncash/btc/ars/0.1")).json() #recibimos el valor de bitcoin en ars 
    usdt = (requests.get("https://criptoya.com/api/lemoncash/usdt/ars/0.1")).json() #recibimos el valor de usdt en ars
    btc_usd = round(bitcoin_ars['totalBid'] / usdt['totalBid']) #dividimos y redondeamos el valor para obtener el precio de btc en usd.

    await context.bot.send_message(chat_id=chat_id, text=f'El precio actual de Bitcoin es de: {btc_usd} USD') #Enviamos el mensaje al usuario

application = Application.builder().token(tl_key).build() #Creamos la instancia del bot
job_queue = application.job_queue #Creamos la instancia del job_queue

application.add_handler(CommandHandler('start', start_command)) #Vinculamos el comando start
application.add_handler(CommandHandler('bitcoin', bitcoin_command)) #Vinculamos el comando bitcoin

job_minute = job_queue.run_repeating(bitcoin_job, interval=60, first=10) #Pedimos que se ejecute cada un minuto.

application.run_polling() #Corremos el bot