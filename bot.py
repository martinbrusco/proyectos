import telebot
from pytube import YouTube
import os 


bot_token = ""

bot = telebot.TeleBot(bot_token)  

@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.reply_to(message, "Bienvenido al bot de descarga de audio de YouTube. Envía la URL del video que deseas descargar para obtener el audio en formato MP3.")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    video_url = message.text

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

 
    try:
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_filename = f"{video_title}.mp3"
        audio_stream.download(filename=audio_filename)

  
        with open(audio_filename, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file, caption=video_title)

     
        os.remove(audio_filename)

    except Exception as e:
        bot.reply_to(message, "No se pudo descargar el video o extraer el audio. Inténtalo de nuevo más tarde.")

bot.polling()

