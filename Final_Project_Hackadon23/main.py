import azure.cognitiveservices.speech as speechsdk
import pyttsx3
import weather_tip
import routes
import time
import subprocess


def speak_text(text, rate=130):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def trigger(prompt):
    speak_text(prompt)

    #setting up azure
    subscription_key = "bb044baee5d7476e93585c526562fc27"
    endpoint = "https://germanywestcentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, endpoint=endpoint)
    audio_input = speechsdk.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    while True:
        result = speech_recognizer.recognize_once()
        # checking if the user said the trigger word
        # if not, continue listening
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text = result.text.lower()
            if any(word in recognized_text for word in ["genie", "jennie", "gini","jeanne", "giny", "jeannie", "ginie", "jinie", "ginee", "ginny", "geny", "giney", "ginnie"]):
                speak_text("Jeenie is on the way!")
                return "ginie"
        elif result.reason == speechsdk.ResultReason.NoMatch:
            continue



def get_user_input(prompt, max_retries=2):
    #setting up azure
    subscription_key = "bb044baee5d7476e93585c526562fc27"
    endpoint = "https://germanywestcentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
    
    for retry in range(max_retries + 1):
        speak_text(prompt)

        # microphone input config
        audio_input = speechsdk.AudioConfig(use_default_microphone=True)
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, endpoint=endpoint)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text = result.text
            return recognized_text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            if retry < max_retries:
                speak_text("Sorry, I didn't catch that. Could you say it again?")
                time.sleep(1)
            else:
                print("Not recognised.")
                break


def main():
    # waiting for trigger word "ginie"
    trigger_word = None
    while trigger_word != "ginie":
        trigger_word = trigger("")
    
    # welcome message
    speak_text("Welcome to the VGI. I am ready to process your request")

    # getting user inputs
    starting_point = get_user_input("What is your starting point?")    # Central
    destination = get_user_input("What is your destination?")       # Square
    hour = get_user_input("Input the desired hour")     # 14
    minutes = get_user_input("Input the minutes")       #10
    '''
    if starting_point:
        print("Starting point:", starting_point)
    if destination:
        print("Destination:", destination)
    if hour:
        print("Hour", hour)
    if minutes:
        print("Minutes", minutes)
    '''
    if hour and minutes:
        time = hour.strip(".") + ":" + minutes.strip(".")
    
    # formatting
    starting_point = starting_point.strip(".")
    destination =  destination.strip(".")

    # bus departure
    route  = routes.calculate_time(starting_point, destination, time)
    speak_text(route)

    time.sleep(1)

    # tip based on the current weather
    for key, value in weather_tip.weather().items():
        if key == "Advice":
            tip = value
            

    speak_text("By the way, a quick tip for you:")
    speak_text(tip)
    
    #live tracking offer
    answer = get_user_input("Would you like to see the live tracking of the bus?")
    if answer.trim(".") == "yes":
        subprocess.run(['python3', 'gps_tracking_main.py'])
    elif answer.trim(".") == "no":
        speak_text("Okay! Genie wishes you a safe trip!")


if __name__ == "__main__":
    main()

