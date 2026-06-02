from abc import ABC, abstractmethod

class AudioSource(ABC):

    @abstractmethod
    def get_audio(self, frames):
        pass