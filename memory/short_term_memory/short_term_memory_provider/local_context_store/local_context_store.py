class ContextStore:
    def __init__(self, max_length=5):
        """
        Initialize the context store.
        :param max_length: Maximum length of context history to maintain
        """
        self.max_length = max_length
        self.history = []

    def add(self, user_input, model_output):
        """
        Add new conversation to history.
        :param user_input: User input
        :param model_output: Model output
        """
        self.history.append({"user": user_input, "model": model_output})
        # If history exceeds max length, remove oldest entry
        if len(self.history) > self.max_length:
            self.history.pop(0)

    def get_context(self):
        """
        Get current conversation context formatted as string.
        :return: Current conversation context
        """
        context = ""
        for exchange in self.history:
            context += f"User: {exchange['user']}\n"
            context += f"Model: {exchange['model']}\n"
        return context

    def clear(self):
        """
        Clear all history.
        """
        self.history = []

# Example: How to use this ContextStore class
if __name__ == "__main__":
    context_store = ContextStore(max_length=3)

    # Add conversations
    context_store.add("Hello", "Hello! How can I help you?")
    context_store.add("How's the weather today?", "The weather is nice today, sunny and bright.")
    context_store.add("I want to learn about artificial intelligence", "Artificial intelligence is a branch of computer science that enables machines to perform human-like tasks.")

    # Get current context
    print("Current context:")
    print(context_store.get_context())

    # Add another conversation, oldest will be removed if exceeds max length
    context_store.add("What is machine learning?", "Machine learning is an important branch of artificial intelligence that involves machines learning from data and making predictions.")
    
    print("\nUpdated context:")
    print(context_store.get_context())
