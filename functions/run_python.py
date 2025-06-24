import os
import subprocess

def run_python_file(working_directory, file_path):
            # Normalize the paths
        working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_path is within the working directory
        if not abs_file_path.startswith(working_directory + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_file_path):
              return f'Error: File "{file_path}" not found.'
        
        if not abs_file_path.endswith('.py'):
            return f'Error: File "{file_path}" is not a Python file.'
        try:
            result = subprocess.run(['python3', abs_file_path], capture_output=True,  cwd=working_directory, timeout=30, text = True)
            result_stdout = 'STDOUT:' + result.stdout
            result_stderr = 'STDERR:' + result.stderr
        except Exception as e:
            return f"Error: executing Python file: {e}"
        
        if not result.stdout.strip() and not result.stderr.strip():
            return "No output produced."

        # Always build the output with STDOUT and STDERR
        output = result_stdout + "\n" + result_stderr

        # Add exit code message if non-zero
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"

        return output