from src.config import ConfigOpenAI
import logging

class CoreAssistant(ConfigOpenAI):
    """
    Core Assistant
    --------------
    Define core assistant properties for easy replication.
    """

    def __init__(self, assistant_name=None):
        super().__init__()
        self.name = assistant_name
        self.model = "gpt-4o-mini"
        self.response_format = 'auto'
        self.description = 'You are a cover letter writing assistant'
        self.instructions = (
            "Your duties are to process provided job description from the user "
            "and write a targeted cover letter to bypass ATS that is also tailored to their skill set."
        )
        self.temperature = 0.1
        self.tools = [{"type": "code_interpreter"}]
        self.assistant_attributes = {}

    def get_assistant_attributes(self, limit=None):
        """
        Retrieve attributes assigned to each assistant.
        """
        assistants = self.client.beta.assistants.list(limit=limit, order="desc")
        self.assistant_attributes = {assistant.name: assistant.__dict__ for assistant in assistants.data}

    def create_new_assistant(self):
        """
        Create a new assistant with core attributes.
        """
        try:
            self.client.beta.assistants.create(
                model=self.model,
                name=self.name,
                description=self.description,
                instructions=self.instructions,
                temperature=self.temperature,
                response_format=self.response_format,
                tools=self.tools
            )
        except Exception as err:
            logging.info(f"Issue creating assistant, see error: {err}")

    def delete_assistant(self):
        """
        Delete an assistant based on the provided assistant name.
        """
        self.get_assistant_attributes()
        assistant_data = self.assistant_attributes.get(self.name)
        if assistant_data:
            command = input(f'Are you sure you would like to delete {self.name}? (y/N) ')
            if command.lower() == 'y':
                self.client.beta.assistants.delete(assistant_id=assistant_data.get('id'))
                logging.debug(f"{self.name} deleted.")
                return True
        else:
            logging.debug(f"{self.name} doesn't exist")
        return False

if __name__ == "__main__":
    core_assistant = CoreAssistant("Cover Letter Writing Assistant")
