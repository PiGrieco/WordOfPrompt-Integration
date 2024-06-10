class PromptFactory:
    """
    Class for generating prompt messages.
    """

    def __init__(self, assistant=None, question=None, user=None, system=None):
        """
        Initializes the PromptFactory instance with specified components of the prompt messages.

        Args:
            assistant (str, optional): The content for the assistant role. Defaults to None.
            question (str, optional): The content for the user's question. Defaults to None.
            user (str, optional): The content for the user role. Defaults to None.
            system (str, optional): The content for the system role. Defaults to None.
        """
        self.assistant = assistant
        self.question = question
        self.user = user
        self.system = system

    def generate_prompt(self):
        """
        Generates a prompt template based on the specified components.

        Returns:
            list: A list of prompt messages.
        """
        messages = []

        if self.assistant is not None:
            messages.append({"role": "assistant", "content": self.assistant})
        else:
            messages.append(None)

        if self.question is not None:
            messages.append({"role": "user", "content": self.question})
        else:
            messages.append(None)

        if self.user is not None:
            messages.append({"role": "user", "content": self.user})
        else:
            messages.append(None)

        if self.system is not None:
            messages.append({"role": "system", "content": self.system})
        else:
            messages.append(None)

        return messages
