# Importações para Assistente
import warnings
import os
import pygame
import speech_recognition as sr
import pyttsx3
import random
from random import choice
import datetime
import webbrowser as wb
import requests
from modules import comandos_respostas
from modules.yt_music import YTMusicPlayer

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

# Função de voz com velocidade aumentada
def speak(audio):
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

# Função de Pesquisa
def search(frase):
    wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)

# Previsão do Tempo 
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

# Inicialização
print('\n' + '👑' * 60)
print('[INFO] Inicializando o Sistema...'.center(60))
play_audio('n1.mp3')  # Agora busca na pasta Isa automaticamente

mensagem = f"{saudacao()}, sou a {meu_nome}. {choice(entradas)}"
print('═' * 60)
print(f"🔊 {meu_nome.upper()}: {mensagem}")
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

        if result in comandos[1]:
            play_audio('n2.mp3')
            speak('Pode falar!')
            result = listen_microphone()
            with open('anotacao.txt', mode='a+', encoding='utf-8') as anotacao:
                anotacao.write(result + '\n')
            speak(choice(respostas[1]))
            speak('Deseja que eu leia os lembretes?')
            if listen_microphone() in ['sim', 'pode ler']:
                with open('anotacao.txt') as file_source:
                    for line in file_source.readlines():
                        speak(line)

        if result in comandos[2]:
            play_audio('n2.mp3')
            speak(choice(respostas[2]))
            search(listen_microphone())

        if result in comandos[3]:
            play_audio('n2.mp3')
            speak('Agora são ' + datetime.datetime.now().strftime('%H:%M'))

        if result in comandos[4]:
            play_audio('n2.mp3')
            date = datetime.date.today().strftime('%d/%B/%Y').split('/')
            speak(f"Hoje é dia {date[0]} de {date[1]}")

        if result in comandos[5]:
            play_audio('n2.mp3')
            speak('Para qual cidade você quer saber a previsão?')
            cidade = listen_microphone()
            clima(cidade)  

        if result in comandos[6]:  # Comando para música
            play_audio('n2.mp3')
            speak("Qual música você quer ouvir?")
            musica = listen_microphone() 
            
        if musica:  
            try:
                if not music_player.driver:
                    music_player._initialize_browser()
                
                if music_player.search_and_play(musica):
                    speak(f"Tocando {musica}. Diga 'pausar', 'continuar' ou 'próxima'.")
                    
                    while True:
                        try:
                            comando = listen_microphone().lower()
                            
                            if "pausar" in comando:
                                if music_player.pause_resume():
                                    speak("Música pausada")
                                else:
                                    speak("Não consegui pausar a música")
                                    
                            elif "continuar" in comando or "despausar" in comando:
                                if music_player.pause_resume():
                                    speak("Continuando a música")
                                else:
                                    speak("Não consegui retomar a música")
                                    
                            elif "próxima" in comando or "próximo" in comando:
                                if music_player.next_track():
                                    speak("Próxima música tocando")
                                else:
                                    speak("Não consegui avançar para a próxima música. Tentando novamente...")
                                    time.sleep(1)
                                    if music_player.next_track():  # Segunda tentativa
                                        speak("Próxima música tocando")
                                    else:
                                        speak("Ainda não consegui. Por favor, tente manualmente.")
                                        
                            elif any(cmd in comando for cmd in ["parar", "encerrar"]):
                                speak("Encerrando player de música")
                                music_player.close()
                                break
                                
                        except Exception as e:
                            print(f"Erro no controle de música: {e}")
                            speak("Desculpe, houve um problema ao processar seu comando")
                            break 
                            
            except Exception as e:
                print(f"Erro: {e}")
                speak("Ocorreu um erro ao controlar a música")
    else:
        play_audio('n3.mp3')