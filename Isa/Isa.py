# Importações para Assistente
import warnings
import os
import pygame
import speech_recognition as sr
import pyttsx3
import random
from random import choice
import datetime
import locale
import webbrowser as wb
import requests
from modules import comandos_respostas
from modules.yt_music import YTMusicPlayer
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

# player de música (yt_music.py)
music_player = YTMusicPlayer()
pygame.mixer.init()

# Importação de Comandos e Respostas
comandos = comandos_respostas.comandos
respostas = comandos_respostas.respostas
saudacoes = comandos_respostas.saudacoes
entradas = comandos_respostas.entradas

# Configurações da Assistente
meu_nome = 'Isa'
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

# Cria pasta para gravações
os.makedirs(os.path.join(BASE_DIR, 'recordings'), exist_ok=True)

# Define localização para datas
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Função para obter saudação baseada na hora
def saudacao():
    hora = datetime.datetime.now().hour
    if 5 <= hora < 12:
        return random.choice(saudacoes["manha"])
    elif 12 <= hora < 18:
        return random.choice(saudacoes["tarde"])
    return random.choice(saudacoes["noite"])

# Função para reproduzir áudio (arquivos na pasta Isa)
def play_audio(file_name):
    audio_path = os.path.join(BASE_DIR, file_name)
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Erro ao reproduzir {file_name}: {e}")

# Função de voz com velocidade aumentada e console
def speak(audio):
    print(f"🔊 ISA: {audio}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 250)
    engine.setProperty('volume', 1)
    engine.say(audio)
    engine.runAndWait()

def listen_microphone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print('═' * 60)
        print('🎧 OUVINDO:')
        microfone.adjust_for_ambient_noise(source, duration=0.8)
        audio = microfone.listen(source)
        recording_path = os.path.join(BASE_DIR, 'recordings', 'speech.wav')
        with open(recording_path, 'wb') as f:
            f.write(audio.get_wav_data())
    try:
        frase = microfone.recognize_google(audio, language='pt-BR')
        print('═' * 60)
        print('🙎 Você disse:', frase)
        return frase
    except sr.UnknownValueError:
        print('═' * 60)
        print('Não entendi')
        return ''

def search(frase):
    wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)

def clima(cidade):
    token = "3449a9d876cc22887f531bb84654b9e5"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + token + "&q=" + cidade + "&lang=pt_br"
    response = requests.get(complete_url)
    retorno = response.json()

    if retorno["cod"] == 200:
        valor = retorno["main"]
        temperatura_celsius = int(valor["temp"] - 273.15)
        descricao = retorno["weather"][0]["description"]
        umidade = valor["humidity"]

        frase = f"Em {cidade}, a temperatura é de {temperatura_celsius} graus Celsius, com umidade de {umidade}% e o clima está {descricao}."
        speak(frase)
    else:
        speak('Desculpe, não consegui encontrar a previsão para essa cidade.')

# Inicialização
print('\n' + '👑' * 60)
print('[INFO] Inicializando o Sistema...'.center(60))
play_audio('n1.mp3')
mensagem = f"{saudacao()}, sou a {meu_nome}. {choice(entradas)}"
print('═' * 60)
speak(mensagem)

# Loop principal
while True:
    result = listen_microphone()

    if meu_nome in result:
        result = str(result.split(meu_nome + ' ')[1]).lower()
        print('Acionou a assistente!')

        if result in comandos[0]:
            play_audio('n2.mp3')
            speak('Até agora minhas funções são: ' + respostas[0])

        elif result in comandos[1]:
            play_audio('n2.mp3')
            speak('Pode falar!')
            result = listen_microphone()
            with open('anotacao.txt', 'a+', encoding='utf-8') as anotacao:
                anotacao.write(result + '\n')
            speak(choice(respostas[1]))
            speak('Deseja que eu leia os lembretes?')
            if listen_microphone().lower() in ['sim', 'pode ler']:
                with open('anotacao.txt') as file_source:
                    for line in file_source:
                        speak(line.strip())

        elif result in comandos[2]:
            play_audio('n2.mp3')
            speak(choice(respostas[2]))
            search(listen_microphone())

        elif result in comandos[3]:
            play_audio('n2.mp3')
            speak('Agora são ' + datetime.datetime.now().strftime('%H:%M'))

        elif result in comandos[4]:
            play_audio('n2.mp3')
            data_formatada = datetime.datetime.now().strftime('%d de %B')
            speak(f"Hoje é {data_formatada}")

        elif result in comandos[5]:
            play_audio('n2.mp3')
            speak('Para qual cidade você quer saber a previsão?')
            cidade = listen_microphone()
            clima(cidade)

        elif result in ['sair', 'encerrar', 'finalizar', 'desligar']:
            speak("Encerrando o sistema. Até mais!")
            break

        elif result in comandos[6] or 'outra música' in result:
            play_audio('n2.mp3')
            speak("Qual música você quer ouvir?")
            musica = listen_microphone()

            try:
                if not music_player.driver:
                    music_player._initialize_browser()

                if music_player.search_and_play(musica):
                    speak(f"Tocando {musica}. Diga 'pausar', 'continuar', 'próxima' ou 'outra música'.")

                    while True:
                        comando = listen_microphone().lower()

                        if 'outra música' in comando:
                            speak("Qual música você quer ouvir?")
                            musica = listen_microphone()
                            if music_player.search_and_play(musica):
                                speak(f"Tocando {musica}.")

                        elif 'pausar' in comando:
                            if music_player.pause_resume():
                                speak("Música pausada")
                            else:
                                speak("Não consegui pausar a música")

                        elif 'continuar' in comando or 'despausar' in comando:
                            if music_player.pause_resume():
                                speak("Continuando a música")
                            else:
                                speak("Não consegui retomar a música")

                        elif 'próxima' in comando:
                            if music_player.next_track():
                                speak("Próxima música tocando")
                            else:
                                speak("Não consegui avançar para a próxima música")

                        elif any(cmd in comando for cmd in ['parar', 'encerrar']):
                            speak("Encerrando player de música")
                            music_player.close()
                            break

            except Exception as e:
                print(f"Erro: {e}")
                speak("Ocorreu um erro ao controlar a música")

    else:
        play_audio('n3.mp3')
