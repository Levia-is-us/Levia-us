import abc


class BaseStream(abc.ABC):
    @abc.abstractmethod
    def output(self, log: str):
        pass
