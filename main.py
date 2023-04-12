from senha import API_KEY
from senha import API_KEY_TEMP
import datetime
import requests
import json
import speech_recognition as sr
import pyttsx3
import webbrowser

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Ouvindo: ")
        microfone.pause_threshold = 1
        audio = microfone.listen(source)

    try:
        print("reconhecendo...")
        query = microfone.recognize_google(audio, language="pt-BR")
        print(f"usuário disse: {query}")

    except Exception as e:
        print("Poderia dizer novamente")
        return "none"

    return query

def search_web():
    speak("o que você gostaria de procurar?")
    query = recognize_speech()
    url = f"https://google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"aqui está os resultados para {query}")

def set_reminder():
    speak("O que devo lembrá-lo?")
    task = recognize_speech()
    speak("em quantos minutos?")
    mins = recognize_speech()
    mins = int(mins)
    reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=mins)
    with open('reminder.txt', 'a') as f:
        f.write(f"{reminder_time} - {task}")
    speak(f"Lembrete definido para {mins} minutos a partir de agora.")

def chat_gpt():
    speak("o que você gostaria de pesquisar?")
    frase = recognize_speech()
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-type": "application/json"}
    link = "https://api.openai.com/v1/chat/completions"
    id_modelo = "gpt-3.5-turbo"

    body_message = {
            "model": id_modelo,
            "messages": [{"role": "user", "content": f"{frase}"}]
        }
    body_message = json.dumps(body_message)
    requisicao = requests.post(link, headers=headers, data=body_message)
    print(requisicao)
    resposta = requisicao.json()
    mensagem = resposta["choices"][0]["message"]["content"]
    print("sua solicitação: " + frase)
    print("sua resposta é: " + mensagem)
    speak(mensagem)
    with open('mensagem.txt', 'a') as f:
        f.write(f"{mensagem}")

def weather():
    speak("Qual cidade você gostaria de saber o tempo?")
    query = recognize_speech()
    cidade = query
    chave_api = API_KEY_TEMP
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        temperatura = dados["main"]["temp"]
        descricao = dados["weather"][0]["description"]
        speak(f"Em {cidade}, a temperatura atual é de {temperatura} graus Celsius e o tempo está {descricao}.")
    else:
        speak("Não foi possível obter os dados de tempo.")

def main():
    speak("Olá, Eu sou o UIQUI, seu assistente pessoal. Em que posso ajudar?")
    while True:
        query = recognize_speech().lower()

        if "buscar conhecimento" in query:
            chat_gpt()

        elif "pesquisar na web" in query:
            search_web()

        elif "criar um lembrete" in query:
            set_reminder()
            break
        elif "previsão do tempo" in query:
            weather()

        elif "pare" in query or "sair" or "cancelar" in query:
            speak("Até logo.")
            break
        else:
            speak("Desculpe, não entendi. Poderia repetir?")

main()
