import azure.cognitiveservices.speech as speechsdk
import pyttsx3
import weather_tip
import routes

def speak_text(text, rate=130):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def trigger(prompt):
    speak_text(prompt)

    subscription_key = "bb044baee5d7476e93585c526562fc27"
    endpoint = "https://germanywestcentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, endpoint=endpoint)

    audio_input = speechsdk.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    while True:
        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text = result.text.lower()
            if any(word in recognized_text for word in ["genie", "jennie", "gini", "giny", "jeannie", "ginie", "jinie", "ginee", "ginny", "geny", "giney"]):
                speak_text("Ginie is on the way!")
                return "ginie"
            else:
                print(recognized_text)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            # Ignore unrecognized input and continue listening
            continue

def get_user_input(prompt):
    speak_text(prompt)

    # azure
    subscription_key = "bb044baee5d7476e93585c526562fc27"
    endpoint = "https://germanywestcentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, endpoint=endpoint)

    # microphone input config
    audio_input = speechsdk.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_text = result.text
        return recognized_text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("Not recognised")

def main():

    trigger_word = None
    while trigger_word != "ginie":
        trigger_word = trigger("")
    
    speak_text("Welcome to the VGI. I am ready to process your request")

    starting_point = get_user_input("What is your starting point?")
    destination = get_user_input("What is your destination?")
    hour = get_user_input("Input the desired hour")
    minutes = get_user_input("Input the minutes")

    if starting_point:
        print("Starting point:", starting_point)
    if destination:
        print("Destination:", destination)
    if hour:
        print("Hour", hour)
    if minutes:
        print("Minutes", minutes)
    
    time = hour.strip(".") + ":" + minutes.strip(".")

    route  = routes.calculate_time(starting_point, destination, time)
    speak_text(route)

    for key, value in weather_tip.weather().items():
        if key == "Advice":
            tip = value
            print(tip)

    speak_text("By the way, a quick tip for you:")
    speak_text(tip)
    
    answer = get_user_input("Would you like to see the live tracking of the bus?")
    if answer == "yes":
        pass
    elif answer == "no":
        speak_text("Okay! Genie wishes you a safe trip!")

if __name__ == "__main__":
    main()

