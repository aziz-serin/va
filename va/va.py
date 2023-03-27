import logging
from openai_tools.config.config_manager import Config
from openai_tools.ai_chat import OpenAIChat
from openai_tools.error import InvalidMessageError, TokenLimitError, NullResponseError, FileSizeError, VAError
from text_to_speech.talk import Talkie
from text_to_speech.error import UnsupportedLanguageError
from gtts import gTTSError
from configparser import NoSectionError

logging.basicConfig(level = logging.DEBUG)

"""
This script is provided to play around with the current implemented features of the application. It will be deleted/made
absolute once the app is completed
"""

def main():
    config = get_config("resources/config.ini", "personal_information")
    text_to_speech("Speak this text in english, do a good job", "resources/tts.mp3")

def get_config(path:str, section:str) -> Config:
    try:
        return Config(path, section)
    except NoSectionError:
        quit(1)

def chat(message:str, config:Config):
    ai = OpenAIChat(config=config)
    try:
        return ai.send_message(message=message, conversation=False)
    except (InvalidMessageError, TokenLimitError, NullResponseError) as err:
        logging.error(err.message)
        quit(1)
    except VAError:
        quit(1)

def conversation(config: Config):
    ai = OpenAIChat(config=config)
    while True:
        prompt = str(input(": "))
        if prompt in ["quit", "q", "end"]:
            break
        try:
            reply = ai.send_message(message=prompt, conversation=True)
            print(f"\t{reply}")
        except (InvalidMessageError, TokenLimitError, NullResponseError) as err:
            logging.error(err.message)
            break
        except VAError:
            break
    print("\n\n\n")
    print(ai.messages)

def text_to_speech(text:str, path:str):
    talkie = Talkie()
    try:
        talkie.save_sound(text, path)
    except gTTSError as err:
        logging.error(err.msg)
        quit(1)
    except UnsupportedLanguageError as err:
        logging.error(err.message)
        quit(1)


def speech_to_text(file_path:str, function):
    try:
        return function(file=file_path)
    except FileSizeError as err:
        logging.error(err.message)
        quit(1)
    except VAError:
        quit(1)


if __name__ == "__main__":
    main()
