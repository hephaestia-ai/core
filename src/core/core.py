from cowgirl_ai.error_handler import error_handler
from cowgirl_ai.vectors.vector_interactions import VectorInteractions
from cowgirl_ai.search.search import Search

from core.assistant.core_assistant import CoreAssistant
from config import ConfigOpenAI

import logging
import time


logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

class Core(ConfigOpenAI): 
    """
    Core
    ----

    Core API behavior methods, includes searching and uploading files to a vector store 
    and assigning a vector store to a provided assistant.
    """

    def __init__(self, assistant_name=None, vector_name=None, directory=None, extension=None):
        super().__init__()
        self.assistant_name = assistant_name
        self.vector_name = vector_name
        self.directory = directory
        self.extension = extension


    @error_handler
    def create_new_assistant(self):
        """
        Create New Assistant 
        --------------------

        Creates a new assistant by calling the CoreAssistant class
        """

        ai = CoreAssistant(self.assistant_name)
        ai.create_new_assistant()
        logging.info(f"Created new assistant: {self.assistant_name}")

    @error_handler 
    def delete_assistant(self):
        """
        Delete Assistant 
        ----------------

        Deletes assistant from Open AI
        """

        ai = CoreAssistant(self.assistant_name)
        ai.delete_assistant()

    @error_handler
    def create_new_vector(self):
        """
        Create New Vector
        -----------------

        Creates a new vector by calling the VectorInteractions class
        """

        vector_interactions = VectorInteractions(self.vector_name)
        vector_interactions.create_vector()

    def update_assistant_to_use_vector(self):
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
        self.create_new_vector(self.vector_name) # Creates new vector if not exists already

        vector_interactions = VectorInteractions(self.vector_name)
        latest_vector_dict = vector_interactions.get_latest_vector_id()
        vector_id = latest_vector_dict.get(f'{self.vector_name}')

        time.sleep(5) # Delay execution so assistant has time to see vector

        assistant_interactions = CoreAssistant(self.assistant_name)  
        assistant_interactions.get_assistant_attributes(limit=1)
        attributes = assistant_interactions.assistant_attributes
        assistant_id = attributes[f'{self.assistant_name}'].get('id')
        success = False
        try:
            self.client.beta.assistants.update(
                assistant_id=assistant_id,
                tool_resources={"file_search": {"vector_store_ids": [vector_id]}},
            )
            logging.info(f"Assistant {self.assistant_name} updated to use vector store {self.vector_name}")
            success = True
        except Exception as error:
            logging.info(f"Issue making API request {error}")
        return success

    def __process_files(self, directory, extension):
        """
        Note: the file has to contain information. Doesn't take empty files
        TODO: Add check for no data.
        """ 
            
        file_search = Search() # TBD: replace with args? CLI entry point
        try:
            file_search.search(directory=directory, file_ext=extension)
            file_paths = file_search.data # Stack obj
            logging.debug(f"Found {file_search.data}")
            return file_paths
        except Exception as err:
            logging.error(f"Issue loading files, see {err}")
       
    
    @error_handler
    def upload_files_to_vector(self):
        """
        Upload Files to Vector
        ----------------------

        Uploads specified files to our vector store. This can 
        happen before or after an assistant is referencing a specific vector. 
        This is because many assistants may reference the same vector object.
        """

        file_paths = self.__process_files(self.directory, self.extension)
        vector_interactions = VectorInteractions(self.vector_name)
        vector_interactions.upload_files(file_paths=file_paths)

if __name__=="__main__":
    
    """   
    Configure your vector, assistant, directory and extension.
    + Assistant should be created ahead of time if not already done so. 
    + If the vector already exists, it will not be created. 
    + Note: The vector only takes the 'latest' created vector.
    + Directory + ext should contain the full file path and all files you wish to upload
    """

    Core()

    # EXAMPLE USAGE:

    # vector_name='Data Generation Assistant Vector Store'
    # assistant_name='Data Generation Assistant v2'
    # directory = "/Users/teraearlywine/Cowgirl-AI/core/src/data_generation"
    # extension = "py"
    
    # core = Core(assistant_name, vector_name, directory, extension)
