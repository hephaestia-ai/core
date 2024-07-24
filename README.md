# Cowgirl AI Core

Configures the assistant, assistant interface, vector, file management, directory and extension mechanisms for CLI useage. 

Available commands: 
```zsh 

    % cowgirl-ai-core create_assistant "Assistant Name"
    % cowgirl-ai-core create_vector "Vector Name"
    % cowgirl-ai-core update_assistant "Assistant Name" "Vector Name"
    % cowgirl-ai-core upload_files "/path/to/directory" "ext" "Vector Name" 

```


Development notes: 

+ Assistant should be created ahead of time if not already done so. 
+ If the vector already exists, it will not be created. 
+ Note: The vector only takes the 'latest' created vector.
+ Directory + ext should contain the full file path and all files you wish to upload
