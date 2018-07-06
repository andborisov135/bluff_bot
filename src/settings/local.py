from telegram.ext import Updater, Dispatcher

TOKEN = "592575295:AAF0SPnb_az379TNk5oXQ8OxvyuwSlmHslY"

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

URL = "https://ece90700.ngrok.io/" #Ngrok URL, mind "/" in the end