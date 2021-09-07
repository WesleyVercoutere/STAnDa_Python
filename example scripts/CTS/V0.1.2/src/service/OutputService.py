from abc import ABC, abstractmethod

from src.domain.Settings import Settings


class OutputService(ABC):

    def __init__(self, settings: Settings):
        self._settings = settings

    @abstractmethod
    def output(self, data):
        raise NotImplementedError("Method from abstract class not implemented")
