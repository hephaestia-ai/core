from cowgirl_ai.error_handler import error_handler
from core.assistant.core_assistant import CoreAssistant
import logging

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(message)s")

class AssistantInterface(CoreAssistant):
    """
    Assistant Interface
    """
    def __init__(self, assistant_name=None, assistant_id=None):
        super().__init__(assistant_name)
        self.assistant_id = assistant_id
        self.content = ""

    @error_handler
    def set_prompt(self):
        """
        Take user input for passing as prompt.
        """
        self.content += input('Please provide a prompt to the assistant:')
    
    @error_handler
    def stream_data(self):
        """
        Stream data to the assistant.
        """
        self.set_prompt()
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.content}],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")

    @error_handler
    def stream_data_with_file_attachment(self, file_path):
        """
        Stream data with a file attachment to the assistant.
        """
        file = self.client.files.create(file=open(file_path, "rb"), purpose="assistants")
        thread = self.client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": self.content,
                "attachments": [{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}],
            }]
        )

        run = self.client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=self.assistant_id)
        messages = self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
        print(messages[0].content[0].text.value)

if __name__ == "__main__":
    AssistantInterface()