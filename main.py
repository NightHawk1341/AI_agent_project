import os
import sys
from dotenv import load_dotenv  # For loading environment variables from a .env file
from google import genai  # Google Generative AI package
from google.genai import types  # For using Gemini-specific types like Content, FunctionDeclaration, etc.

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Gemini API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")

# Initialize the Gemini API client with the API key
client = genai.Client(api_key=api_key)

# Combine all command-line arguments (except the script name itself) into a single string
# Remove the optional '--verbose' flag if present and trim whitespace
user_prompt = " ".join(sys.argv[1:]).replace("--verbose", "").strip()

# Build a list of messages; the first message is from the user
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Define the system instruction that guides the AI’s behavior
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

If the user's request matches running a file, call run_python_file with the file name, e.g., run_python_file(file_path="tests.py").

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Define Gemini-compatible function declarations (schemas)

# Function to list files in a directory
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# Function to retrieve contents of a file
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve, relative to the working directory.",
            ),
        },
    ),
)

# Function to run a Python file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

# Function to write to a file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

# Combine all declared functions into a Tool object that Gemini can use
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
    ]
)

# Validate user input: must provide a prompt
if len(sys.argv) < 2:
    print("ERROR. Please provide a prompt as a command line argument")
    sys.exit(1)  # Exit the program with an error code

# Define the actual Python functions that the Gemini function calls will map to

# List files in a directory
def get_files_info(directory=None, working_directory=None):
    import os
    path = os.path.join(working_directory, directory or "")
    try:
        files = os.listdir(path)  # List directory contents
        return "\n".join(files)  # Return as newline-separated string
    except Exception as e:
        return f"Error listing files: {str(e)}"

# Read content from a file
def get_file_content(file_path, working_directory=None):
    with open(os.path.join(working_directory, file_path), "r") as f:
        return f.read()

# Execute a Python script
def run_python_file(file_path, working_directory=None):
    import subprocess
    abs_path = os.path.join(working_directory, file_path)
    result = subprocess.run(["python", abs_path], capture_output=True, text=True)
    output = result.stdout + result.stderr  # Combine stdout and stderr
    return output

# Write content to a file
def write_file(file_path, content, working_directory=None):
    with open(os.path.join(working_directory, file_path), "w") as f:
        f.write(content)
    return f"File {file_path} written successfully."

# Create a dictionary to map function names used in Gemini to the actual Python implementations
func_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

# Main interaction loop: allow Gemini to process up to 20 back-and-forth turns
for i in range(20):
    # Send the user's message and context to the model
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    made_tool_call = False  # Track whether the AI tried to call a function

    # Process each candidate response from the model
    for candidate in response.candidates:
        messages.append(candidate.content)  # Save AI response for context

        function_calls_to_execute = []  # List of function calls this turn
        tool_response_parts = []  # List of results (or errors) from executed functions

        # Check each part of the AI response for function calls
        for part in candidate.content.parts:
            if hasattr(part, "function_call") and part.function_call is not None:
                function_calls_to_execute.append(part.function_call)

        if function_calls_to_execute:
            made_tool_call = True  # At least one tool call was found

            # Execute each requested tool function
            for function_call_part in function_calls_to_execute:
                function_name = function_call_part.name
                args = function_call_part.args.copy()  # Copy arguments dictionary

                # Inject working directory
                args['working_directory'] = './calculator'

                try:
                    # Execute the actual Python function
                    result = func_map[function_name](**args)

                    # Create response object from the result
                    response_part = types.Part.from_function_response(
                        name=function_name,
                        response={"result": result}
                    )
                    tool_response_parts.append(response_part)
                except Exception as e:
                    # Handle errors from function execution
                    error_response_part = types.Part.from_function_response(
                        name=function_name,
                        response={"error": str(e)}
                    )
                    tool_response_parts.append(error_response_part)

            # Create one response Content object containing all function call results
            tool_response_content = types.Content(
                role="tool",
                parts=tool_response_parts
            )
            messages.append(tool_response_content)  # Add result to conversation history

        # If no function calls were made, print the AI's plain text output
        if not made_tool_call:
            for part in candidate.content.parts:
                if hasattr(part, "text") and part.text and part.text.strip():
                    print(part.text)
            break  # Exit loop after a successful text response

# Optional: Show extra debug info if --verbose flag was present
if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
