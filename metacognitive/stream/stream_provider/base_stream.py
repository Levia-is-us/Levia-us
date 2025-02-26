import abc


class BaseStream(abc.ABC):
    @abc.abstractmethod
    def output(self, log: str, user_id: str, type: str, child_id: str = ""):
        pass
