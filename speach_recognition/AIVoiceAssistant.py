import openai
import pyttsx3
import speech_recognition as sr
from api_secrets import API_KEY


openai.api_key = API_KEY

engine = pyttsx3.init()

rec = sr.Recognizer()
mic = sr.Microphone(device_index=1)
print(sr.Microphone.list_microphone_names())

conversation = ""
user_name = "You"
bot_name = "Hamada"

while True:
    with mic as source:
        print("\nlistening...")
        rec.adjust_for_ambient_noise(source, duration=0.2)
        audio = rec.listen(source)
    print("no longer listening.\n")

    try:
        user_input = rec.recognize_google(audio)

        prompt = user_name + ": " + user_input + "\n" + bot_name + ": "
        conversation += prompt
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")

    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt=conversation, max_tokens=100)
        response_str = response["choices"][0]["text"].replace("\n", "")
        response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]

        conversation += response_str + "\n"
        print(response_str)

        engine.say(response_str)
        engine.runAndWait()
    except openai.error.OpenAIError as e:
        # Handle OpenAI API-specific errors
        print("OpenAI API Error: {0}".format(e))
    except Exception as e:
        # Handle other general exceptions
        print("An error occurred: {0}".format(e))





