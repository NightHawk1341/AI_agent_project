from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
if __name__ == "__main__":

# Test cases
    print(run_python_file("calculator", "main.py"))               # Should succeed
    print(run_python_file("calculator", "tests.py"))              # Should succeed
    print(run_python_file("calculator", "../main.py"))            # Should return error (outside working directory)
    print(run_python_file("calculator", "nonexistent.py"))  