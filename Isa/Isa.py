# Importacoes para Assistente
import warnings
with warnings.catch_warnings():
   warnings.simplefilter("ignore")  # Ignora todos os avisos

from playsound import playsound
import speech_recognition as sr
import pyttsx3
#import tensorflow as ts
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
import pyaudio
import webbrowser as wb
import speech_recognition as sr
from playsound import playsound
import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
sns.set()

import datetime

# Exibixao de Data e Hora
hora = datetime.datetime.now().strftime('%H:%M')
date = datetime.date.today().strftime('%d/%B/%Y')
date = date.split('/')

#Importacao de Comandos e Respostas
from modules import comandos_respostas
comandos = comandos_respostas.comandos
respostas = comandos_respostas.respostas

# Definicao do Nome da Assistente
meu_nome = 'Isa'

# Definicao do Navegador
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

# Funcao de Pesquisa
def search(frase):
   wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)

# Funcao de Previsao do Tempo

import requests

def clima(cidade):
    token = "3449a9d876cc22887f531bb84654b9e5"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + token + "&q=" + cidade + "&lang=pt_br"
    response = requests.get(complete_url)
    retorno = response.json()

    if retorno["cod"] == 200:
        valor = retorno["main"]
        current_temperature = valor["temp"]
        current_humidity = valor["humidity"]
        tempo = retorno["weather"]
        weather_description = tempo[0]["description"]

        temperatura_celsius = int(current_temperature - 273.15)

        frase = f"Em {cidade}, a temperatura é de {temperatura_celsius} graus Celsius, com umidade de {current_humidity}% e o clima está {weather_description}."
        speak(frase)
    else:
        speak('Desculpe, não consegui encontrar a previsão para essa cidade.')


# Funcao de Voz da Assistente
def speak(audio):
   engine = pyttsx3.init()
   engine.setProperty('rate', 170)
   engine.setProperty('volume', 1)
   engine.say(audio)
   engine.runAndWait()

# Funcao de Ativacao do Microfone
def listen_microphone():
   microfone = sr.Recognizer()
   with sr.Microphone() as source:
       microfone.adjust_for_ambient_noise(source, duration=0.8)
       print('Ouvindo:')
       audio = microfone.listen(source)
       with open('recordings/speech.wav', 'wb') as f:
           f.write(audio.get_wav_data())
   try:
       frase = microfone.recognize_google(audio, language='pt-BR')
       print('Você disse: ' + frase)
   except sr.UnknownValueError:
       frase = ''
       print('Não entendi')
   return frase

playing = False
mode_control = False
print('[INFO] Pronto para começar!')
playsound('n1.mp3')
while (1):
   result = listen_microphone()
   if meu_nome in result:
       result = str(result.split(meu_nome + ' ')[1])
       result = result.lower()
       print('Acionou a assistente!')
       # print('Após o processamento: ', result)
       if result in comandos[0]:
           playsound('n2.mp3')
           speak('Eu posso te ajudar a : ' + respostas[0])

       if result in comandos[1]:
           playsound('n2.mp3')
           speak('Pode falar!')
           result = listen_microphone()
           anotacao = open('anotacao.txt', mode='a+', encoding='utf-8')
           anotacao.write(result + '\n')
           anotacao.close()
           speak(''.join(random.sample(respostas[1], k=1)))
           speak('Deseja que eu leia os lembretes?')
           result = listen_microphone()
           if result == 'sim' or result == 'pode ler':
               with open('anotacao.txt') as file_source:
                   lines = file_source.readlines()
                   for line in lines:
                       speak(line)
           else:
               speak('Ok!')
       if result in comandos[2]:
           playsound('n2.mp3')
           speak(''.join(random.sample(respostas[2], k=1)))
           result = listen_microphone()
           search(result)
       if result in comandos[3]:
           playsound('n2.mp3')
           speak('Agora são ' + datetime.datetime.now().strftime('%H:%M'))
       if result in comandos[4]:
           playsound('n2.mp3')
           speak('Hoje é dia ' + date[0] + ' de ' + date[1])
       if result in comandos[5]:
           playsound('n2.mp3')
           speak('Para qual cidade você quer saber a previsão?')
           cidade = listen_microphone()
           clima(cidade)

       if result == 'encerrar':
           playsound('n2.mp3')
           speak(''.join(random.sample(respostas[4], k=1)))
           break
   else:
       playsound('n3.mp3')