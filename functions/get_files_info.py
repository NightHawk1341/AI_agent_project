import os

# Function to list file and directory information within a specified (safe) working directory
def get_files_info(working_directory, directory=None):
    try:
        # If no subdirectory is specified, default to the working directory itself
        if directory is None:
            directory = working_directory

        # Convert the working directory and target directory to absolute paths
        # This avoids relative path issues and is important for security checks
        working_directory = os.path.abspath(working_directory)
        directory = os.path.abspath(os.path.join(working_directory, directory))

        # SECURITY CHECK:
        # Ensure the target directory is inside the permitted working directory
        # This prevents directory traversal attacks (e.g., using '../' to escape)
        if os.path.commonpath([working_directory, directory]) != working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Validate that the resolved path is an actual directory
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        # Initialize the result list
        output_lines = []

        # Iterate through all items (files and directories) in the target directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)  # Full path of the item
            file_size = os.path.getsize(item_path)     # Get file size in bytes
            is_dir = os.path.isdir(item_path)          # Check if the item is a directory
            # Append information string to output list
            output_lines.append(f'{item}: file_size={file_size} bytes, is_dir={is_dir}')

        # Return all collected lines as a single string separated by newlines
        return '\n'.join(output_lines)

    # Catch any unexpected error (e.g., permission issues, I/O errors)
    except Exception as e:
        return f'Error: {str(e)}'
