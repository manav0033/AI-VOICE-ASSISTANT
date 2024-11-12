import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import pyjokes
import PySimpleGUI as sg
import pyqrcode
import nltk  # Import NLTK
from newsapi import NewsApiClient  # Import News API Client

# Ensure NLTK resources are downloaded
nltk.download('punkt')

phone_numbers = {"rishi": "1234567890", "sakshi": "7507907497", "pranav": "9082724012"}
bank_account_numbers = {"tt": "123456789", "mm": "99999999933"}

# Initialize News API client with your API key
newsapi = NewsApiClient(api_key='8d4ca7aa1e6d4520abf4f68304807134')  # Replace 'YOUR_API_KEY' with your actual News API key

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

def execute_command(command):
    try:
        # Tokenize the command
        tokens = nltk.word_tokenize(command)
        # ask to play songni
        if 'play' in tokens:
            song = ' '.join(tokens[tokens.index('play')+1:])
            speak('playing ' + song)
            pywhatkit.playonyt(song)

        # ask date
        elif 'date' in tokens:
            today = datetime.date.today()
            speak(str(today))

        # ask time
        elif 'time' in tokens:
            timenow = datetime.datetime.now().strftime('%H:%M')
            speak(timenow)

        # ask details about a person
        elif "who is" in tokens:
            person = ' '.join(tokens[tokens.index('who')+2:])
            info = wikipedia.summary(person, 1)
            speak(info)

        # ask phone numbers
        elif "phone number" in tokens:
            names = list(phone_numbers)
            for name in names:
                if name in tokens:
                    print(name + " phone number is " + phone_numbers[name])
                    speak(name + " phone number is " + phone_numbers[name])

        # ask personal bank account numbers
        elif "account number" in tokens:
            banks = list(bank_account_numbers)
            for bank in banks:
                if bank in tokens:
                    print(bank + " bank account number is " + bank_account_numbers[bank])
                    speak(bank + " bank account number is " + bank_account_numbers[bank])

        # tell a joke
        elif "joke" in tokens:
            joke = pyjokes.get_joke()
            speak(joke)
        
        # generate QR code
        elif "generate qr" in tokens:
            data = ' '.join(tokens[tokens.index('generate')+2:])
            qr = pyqrcode.create(data)
            qr.png('qrcode.png', scale=8)
            speak("QR code generated successfully!")

        # fetch news
        elif "news" in tokens:
            fetch_news()

        # if not recognized
        else:
            speak("Please ask a valid question...")

    except Exception as e:
        speak("An error occurred: " + str(e))

# Function to fetch and display news articles
def fetch_news(category='general', language='en', country='us', num_articles=3):
    # Fetch top headlines
    top_headlines = newsapi.get_top_headlines(category=category, language=language, country=country)

    # Display top headlines
    if 'articles' in top_headlines:
        articles = top_headlines['articles'][:num_articles]
        for article in articles:
            title = article['title']
            print(title)
            speak(title)  # Speak the title of the article to the user

def main():
    layout = [[sg.Text('Voice Recognition')],
            [sg.Output(size=(60, 10), key='-OUTPUT-')],
            [sg.Button('Start'), sg.Button('Exit')]]

    window = sg.Window('Voice Recognition App', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if event == 'Start':
            r = sr.Recognizer()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print('Listening...Ask Now!...')
                audioin = r.listen(source)
                my_text = r.recognize_google(audioin)
                my_text = my_text.lower()
                print(my_text)
                window['-OUTPUT-'].update(my_text)

                execute_command(my_text)

    window.close()

if __name__ == "__main__":
    main()
