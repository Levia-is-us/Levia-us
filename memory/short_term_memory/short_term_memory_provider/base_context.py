import abc


class BaseContextStore(abc.ABC):
    @abc.abstractmethod
    def get_context(self, user_key: str = "local"):
        """
        Get context for a specific user key.
        :param user_key: Key to identify user's context
        :return: Context for the specified user
        """
        pass

    @abc.abstractmethod
    def add_context(self, context: str, user_key: str = "local"):
        """
        Add context for a specific user key.
        :param context: Context to add
        :param user_key: Key to identify user's context
        """
        pass

    @abc.abstractmethod
    def delete_context(self, context: str, user_key: str = "local"):
        """
        Delete context for a specific user key.
        :param context: Context to delete
        :param user_key: Key to identify user's context
        """

        pass
