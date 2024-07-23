from cowgirl_ai.error_handler import error_handler
from cowgirl_ai.vectors.vector_interactions import VectorInteractions
from cowgirl_ai.search.search import Search

from src.core.assistant.core_assistant import CoreAssistant
from src.config import ConfigOpenAI

import logging
import time


logging.basicConfig(level=logging.INFO, dtfmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

class Core(ConfigOpenAI): 
    """
    Core
    ----

    Core API behavior methods, includes searching and uploading files to a vector store 
    and assigning a vector store to a provided assistant.
    """

    def __init__(self):
        super().__init__()


    @error_handler
    def create_new_assistant(self, assistant_name):
        """
        Create New Assistant 
        --------------------

        Creates a new assistant by calling the CoreAssistant class
        """

        ai = CoreAssistant(assistant_name)
        ai.create_new_assistant()
        logging.info(f"Created new assistant: {assistant_name}")

    @error_handler
    def create_new_vector(self, vector_name):
        """
        Create New Vector
        -----------------

        Creates a new vector by calling the VectorInteractions class
        """

        vector_interactions = VectorInteractions(vector_name)
        vector_interactions.create_vector()

    def update_assistant_to_use_vector(self, assistant_name, vector_name):
        """
        Update Assistant to Use Vector Store 
        ------------------------------------

        Key method used for maintaining a assistant <> vector relationship. 
        Vectors contain files that are uploaded and used as references by the assistant
        for various processes, frameworks etc.

        Assumes assistant already exists.

        Usage::

            >>> core = Core()
            >>> core.update_assistant_to_use_vector(assistant_name='Cover Letter Generation Assistant', 
                    vector_name='Cover Letter Generation Vector Store')
        """
        self.create_new_vector(vector_name) # Creates new vector if not exists already

        vector_interactions = VectorInteractions(vector_name)
        latest_vector_dict = vector_interactions.get_latest_vector_id()
        vector_id = latest_vector_dict.get(f'{vector_name}')

        time.sleep(5) # Delay execution so assistant has time to see vector

        assistant_interactions = CoreAssistant(assistant_name)  
        assistant_interactions.get_assistant_attributes(limit=1)
        attributes = assistant_interactions.assistant_attributes
        assistant_id = attributes[f'{assistant_name}'].get('id')
        success = False
        try:
            self.client.beta.assistants.update(
                assistant_id=assistant_id,
                tool_resources={"file_search": {"vector_store_ids": [vector_id]}},
            )
            logging.info(f"Assistant {assistant_name} updated to use vector store {vector_name}")
            success = True
        except Exception as error:
            logging.info(f"Issue making API request {error}")
        return success

    @error_handler
    def __process_files(self, directory, extension):
        file_search = Search() # TBD: replace with args? CLI entry point
        file_search.search(directory=directory, file_ext=extension)
        file_paths = file_search.data # Stack obj
        return file_paths
    
    @error_handler
    def upload_files_to_vector(self, directory, extension, vector_name):
        """
        Upload Files to Vector
        ----------------------

        Uploads specified files to our vector store. This can 
        happen before or after an assistant is referencing a specific vector. 
        This is because many assistants may reference the same vector object.
        """

        file_paths = self.__process_files(directory, extension)
        vector_interactions = VectorInteractions(vector_name)
        vector_interactions.upload_files(file_paths=file_paths)

if __name__=="__main__":

    """   
    Configure your vector, assistant, directory and extension.
    + Assistant should be created ahead of time if not already done so. 
    + If the vector already exists, it will not be created. 
    + Note: The vector only takes the 'latest' created vector.
    + Directory + ext should contain the full file path and all files you wish to upload
    """
    # EXAMPLE USAGE:

    vector_name='Cover Letter Generation Vector Store'
    assistant_name='Cover Letter Generation Assistant'
    directory = "/Users/teraearlywine/Desktop/Resumes/cover_letters/"
    extension = ".docx"
    
    core = Core()
    core.upload_files_to_vector(directory, extension, vector_name)
    core.update_assistant_to_use_vector(assistant_name, vector_name)
