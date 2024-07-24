import argparse
from core.core import Core

def main():
    parser = argparse.ArgumentParser(description="Core API behavior methods")
    subparsers = parser.add_subparsers(dest='command')

    # Create new assistant
    parser_create_assistant = subparsers.add_parser('create_assistant', help='Create a new assistant')
    parser_create_assistant.add_argument('assistant_name', type=str, help='Name of the new assistant')

    # Create new vector
    parser_create_vector = subparsers.add_parser('create_vector', help='Create a new vector')
    parser_create_vector.add_argument('vector_name', type=str, help='Name of the new vector')

    # Update assistant to use vector
    parser_update_assistant = subparsers.add_parser('update_assistant', help='Update assistant to use vector store')
    parser_update_assistant.add_argument('assistant_name', type=str, help='Name of the assistant')
    parser_update_assistant.add_argument('vector_name', type=str, help='Name of the vector')

    # Upload files to vector
    parser_upload_files = subparsers.add_parser('upload_files', help='Upload files to vector store')
    parser_upload_files.add_argument('directory', type=str, help='Directory containing files')
    parser_upload_files.add_argument('extension', type=str, help='File extension to filter by')
    parser_upload_files.add_argument('vector_name', type=str, help='Name of the vector')

    args = parser.parse_args()

    core = Core()

    if args.command == 'create_assistant':
        core.create_new_assistant(args.assistant_name)
    elif args.command == 'create_vector':
        core.create_new_vector(args.vector_name)
    elif args.command == 'update_assistant':
        core.update_assistant_to_use_vector(args.assistant_name, args.vector_name)
    elif args.command == 'upload_files':
        core.upload_files_to_vector(args.directory, args.extension, args.vector_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


    """
    
    python script.py create_assistant "Assistant Name"
    python script.py create_vector "Vector Name"
    python script.py update_assistant "Assistant Name" "Vector Name"
    python script.py upload_files "/path/to/directory" "txt" "Vector Name"
    """