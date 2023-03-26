import openai
import logging
import os
from .ai import OpenAI
from .error import FileSizeError, VAError

logging.basicConfig(level = logging.DEBUG)

class OpenAIAudio(OpenAI):
    """
    Given byte limit for audio files for openai at the time of writing this code (25Mb)
    Supported audio file formats at the time of writing this code: ['m4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg']
    """
    byte_limit:int = 26_214_400

    def __init__(self, model:str="whisper-1"):
        super().__init__(model)

    def speech_to_text(self, file:str) -> str:
        file = self.__open_file(file)
        response = self.__send_transcribe_request(file)
        return response["text"]

    def __send_transcribe_request(self, file):
        try:
            return openai.Audio.transcribe(model=self.model, file=file)
        except openai.OpenAIError as err:
            logging.error(err.json_body)
            raise VAError(err.json_body)

    def __open_file(self, file:str):
        try:
            self.__validate_size(file)
            return open(file, "rb")
        except FileSizeError as err:
            logging.error(err.message)
            raise VAError(err.message)

    def __validate_size(self, file:str):
        try:
            size = os.path.getsize(file)
            if size >= self.byte_limit:
                raise FileSizeError(f"Given file size {size} is larger than the limit {self.byte_limit}")
        except OSError as err:
            logging.error(err)
            raise VAError(err)