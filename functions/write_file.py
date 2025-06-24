import os

def write_file(working_directory, file_path, content):
        # Normalize the paths
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_path is within the working directory
        if not file_path.startswith(working_directory + os.sep):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        #try to create the directory if it does not exist
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            directory = os.path.dirname(file_path)
        except Exception as e:
            return f'Error: {str(e)}'
        
        #try to write the file
        try:
             with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error: {str(e)}'