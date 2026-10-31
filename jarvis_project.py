
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from datetime import datetime

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


def recognize_voice(audio):
    return recognizer.recognize_sphinx(audio)


def process_command(command):
    command = command.lower().strip()

    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")

    elif "open tiktok" in command:
        webbrowser.open("https://tiktok.com")
        speak("Opening TikTok")

    elif command.startswith("play "):
        song = command[5:].strip()

        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
            speak("Playing " + song)
        else:
            speak("Sorry, song not found in my library")

    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak("The time is " + current_time)

    elif "stop listening" in command:
        speak("Goodbye")
        return False

    else:
        speak("Sorry, I don't know that command yet")

    return True


def main():
    speak("Initializing Jarvis")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:
        try:
            print("Listening for wake word...")

            with sr.Microphone() as source:
                audio = recognizer.listen(
                    source, timeout=5, phrase_time_limit=3
                )

            word = recognize_voice(audio)
            print("You said:", word)

            if "jarvis" in word.lower():
                speak("Hi sir")

                with sr.Microphone() as source:
                    print("Jarvis is active. Give a command.")
                    audio = recognizer.listen(
                        source, timeout=5, phrase_time_limit=5
                    )

                command = recognize_voice(audio)
                print("Command:", command)

                if not process_command(command):
                    break

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")

        except sr.RequestError as error:
            print("Speech recognition error:", error)

        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
