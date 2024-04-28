

import telebot
from pytube import YouTube
import os  # Importa os para eliminar archivos después de usarlos

# Reemplaza con tu token de bot de Telegram
bot_token = ""

# Crea el objeto del bot
bot = telebot.TeleBot(bot_token)  # Sin el parámetro http

@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.reply_to(message, "Bienvenido al bot de descarga de audio de YouTube. Envía la URL del video que deseas descargar para obtener el audio en formato MP3.")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    video_url = message.text

    # Comprueba si la URL es válida
    try:
        video = YouTube(video_url)
    except Exception as e:
        bot.reply_to(message, "La URL proporcionada no es válida. Asegúrate de que sea una URL de YouTube.")
        return

    # Obtén información del video
    try:
        video_title = video.title
    except Exception as e:
        bot.reply_to(message, "No se pudo obtener información del video. Inténtalo de nuevo más tarde.")
        return

    # Descarga el audio del video
    try:
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_filename = f"{video_title}.mp3"
        audio_stream.download(filename=audio_filename)

        # Envía el archivo de audio al usuario
        with open(audio_filename, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file, caption=video_title)

        # Elimina el archivo de audio temporal
        os.remove(audio_filename)

    except Exception as e:
        bot.reply_to(message, "No se pudo descargar el video o extraer el audio. Inténtalo de nuevo más tarde.")

# Inicia el bot
bot.polling()

