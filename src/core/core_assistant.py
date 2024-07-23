from src.config import ConfigOpenAI
import logging 

class CoreAssistant(ConfigOpenAI):
    """
    Core Assistant
    --------------

    Define core assistant properties for easy replication. 
    "Create Assistant" -> tbd
    """

    def __init__(self, assistant_name=None):
        super().__init__()
        self.model = "gpt-4o"            # Required (try gpt-4o-mini)
        self.name = assistant_name       # Name of the assistant
        self.response_format = { "type": "json_object" } 
        self.description = None   
        self.instructions = None
        self.temperature = 0.1   
        self.tools=[{"type": "code_interpreter"}] # pylint disable=trailing-comma-tuple
        # self.tool_resources={"file_search": {"vector_store_ids": [f'{None}']}} #TODO 
        self.assistant_attributes = {}

    def get_assistant_attributes(self, limit=None):
        """
        Makes an API call to assistants feature
        and returns attributes assigned to each assistant using the name as the key.

        """
        assistants = self.client.beta.assistants.list(limit=limit, order="desc")
        for assistant in assistants.data:
            assistant_name = assistant.name 
            self.assistant_attributes[assistant_name] = assistant.__dict__

    def set_base_description(self):
        description = 'You are a data generation assistant'
        return description 
    
    def set_base_instructions(self):
        instructions = ''' 
            Your duties are to generate data and output the data itself as a JSON object. Please keep 
            as structured as possible for easy data cleaning. o extra chat or text needed, keep it just the results.
        '''
        return instructions

    def create_new_assistant(self):
        try:
            self.client.beta.assistants.create(
                model=self.model, 
                name=self.name,
                description=self.set_base_description(),
                instructions=self.set_base_instructions(), 
                temperature=self.temperature,
                response_format=self.response_format,
                tools=self.tools,
                # tool_resources=self.tool_resources
            )
        except Exception as err: 
            logging.info(f"Issue creating assistant, see error: {err}")

    def delete(self, assistant_id):
        """
        TODO: buff this out
        """

        response = self.client.beta.assistants.delete(assistant_id=assistant_id)
        return response

if __name__=="__main__":
    CoreAssistant()

    # EXAMPLE USAGE
    # core_assistant = CoreAssistant(assistant_name="Data Generation Assistant v2")
    
    # CREATING:
    # core_assistant.create_new_assistant()
    # core_assistant.get_assistant_attributes(limit=1)
    # print(core_assistant.assistant_attributes)

    # DELETING:
    # core_assistant.delete("asst_TT7W3hhIhs53naQRUR2paKuI")
    # core_assistant.get_assistant_attributes(limit=1)
    # print(core_assistant.assistant_attributes)
