from src.core.interface.assistant_interface import AssistantInterface
from src.core.core import Core 
import os 
import logging 

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

def upload_files(directory, extension, assistant_name, vector_name):
    """
    Call core for backend file uploads/processing
    """

    core = Core()
    core.update_assistant_to_use_vector(assistant_name=assistant_name, vector_name=vector_name)
    core.upload_files_to_vector(directory=directory, extension=extension, vector_name=vector_name)


def generate(assistant_name, assistant_id, has_attachement=False, file_path=None):
    """
    Pass what you want the assistant to do as your input (i.e. read jd file, create a cover letter for x company)
    """
    interface = AssistantInterface(assistant_name=assistant_name, assistant_id=assistant_id)

    interface.set_prompt()
    prompt = interface.content
    logging.info(f"Prompt rendered and passed to assistant, starting stream....")
    # Default
    if has_attachement==False:
        interface.stream_data()
    elif has_attachement==True: 
        interface.stream_data_with_file_attachment(file_path=file_path)


if __name__=="__main__":
        
    # CONFIG
    VECTOR_NAME = 'CI - Cover Letter Generation Vector Store'
    ASSISTANT_NAME = 'Cover Letter Generation Assistant' # Pre-existing

    FILE_SEARCH_DIRECTORY = os.path.join(os.getcwd(), 'src/cover_letter_generation/file_search')
    EXTENSION = ".py"

    upload_files(directory=FILE_SEARCH_DIRECTORY, extension=EXTENSION, assistant_name=ASSISTANT_NAME, vector_name=VECTOR_NAME)

    generate(
        assistant_name=ASSISTANT_NAME, 
        assistant_id=None, 
        has_attachement=True, 
        file_path=os.path.join(FILE_SEARCH_DIRECTORY, 'assistant_constants.py')
    )

