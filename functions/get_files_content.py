import os

# Function to safely retrieve the content of a file within a constrained working directory
def get_file_content(working_directory, file_path):
    try:
        # Convert the working directory and the file path to absolute paths
        # This helps standardize paths and prevent directory traversal exploits
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # SECURITY CHECK:
        # Ensure the file path is still inside the working directory after resolution
        # This prevents the user from reading unauthorized files via relative paths like "../"
        if os.path.commonpath([working_directory, file_path]) != working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Validate that the path points to an actual regular file (not a directory, symlink, etc.)
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Safely open the file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # If the file content is very large, truncate to the first 10,000 characters
        # Prevents flooding the system with excessive output
        if len(content) > 10000:
            content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'

        # Return the (possibly truncated) file content
        return content

    # General exception handler to catch and report any errors during processing
    except Exception as e:
        return f'Error: {str(e)}'
