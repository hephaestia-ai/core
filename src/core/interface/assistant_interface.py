from src.core.assistant.core_assistant import CoreAssistant
import logging 

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

class AssistantInterface(CoreAssistant):
    """
    Assistant Interface
    """
    def __init__(self, assistant_name=None, assistant_id=None):
        super().__init__(assistant_name=None)
        self.assistant_id = assistant_id
        self.assistant_name = assistant_name
        self.content = ""

    def set_prompt(self):
        """
        Take user input for passing as prompt. 
        Combine with json-object so GPT knows to output a jsonl file 
        """

        user_input = input('Please provide a prompt to the assistant:')
        full = user_input # + "output as json object"
        self.content += full

    def stream_data(self):
        """
        Usage::
            >>> interface = AssistantInterface(assistant_name='Data Generation Assistant v2')
            >>> interface.stream_data()

        """

        self.set_prompt()
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": self.content}
            ],

            # Potentially make the following conditional
            stream=True, 
            # response_format=self.response_format
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # Add clause to write to file or database
                print(chunk.choices[0].delta.content, end="")

    def stream_data_with_file_attachment(self, file_path):

        file = self.client.files.create(file=open(file_path, "rb"), purpose="assistants")
        thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": self.content, 
                    "attachments": [            
                        {
                            "file_id": file.id, 
                            "tools": [{"type": "code_interpreter"}] 
                        }
                    ],
                }
            ]
        )
        # Get attributes for the assistant we're currently working with
        # self.get_assistant_attributes(limit=1)
        # attributes = self.assistant_attributes
        # assistant_id = attributes[f'{self.assistant_name}'].get('id')

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=self.assistant_id
        )

        messages = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        message_content = messages[0].content[0].text
        print(message_content.value)

if __name__=="__main__":
    AssistantInterface()
