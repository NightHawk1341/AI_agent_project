# AI Agent Project

## Overview

This repository contains the implementation of an AI coding agent built as part of the "Build an AI Agent in Python" course from Boot.dev. The course focuses on creating an LLM-powered command-line program using Google's Gemini API that can read, update, and execute Python code. It serves as a toy agentic code editor, demonstrating concepts like function calling, feedback loops, and working with large language models to build autonomous agents.

The agent operates within a restricted working directory (./calculator) for security, allowing it to list files, read contents, run Python scripts, and write files only in that sandbox. The repository includes a calculator folder for test purposes, where you can place sample files (e.g., simple Python scripts) to interact with the agent safely.

## Features

* **File Listing**: Lists files and directories within the working directory.
* **File Reading**: Retrieves the content of specified files.
* **Code Execution**: Runs Python files and captures output (stdout/stderr).
* **File Writing**: Writes or overwrites file contents.
* **Gemini API Integration**: Uses Google's Gemini LLM for intelligent decision-making and function calls.
* **Security Constraints**: All operations are confined to the ./calculator directory to prevent unauthorized access.

## Prerequisites

* Python 3.10 or higher.
* A free Google Gemini API key (obtain from Google AI Studio).
* Required libraries listed in requirements.txt: google-genai and python-dotenv.

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/ai-agent-project.git
cd ai-agent-project
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set up your environment variables:
   * Create a .env file in the root directory.
   * Add your Gemini API key: GEMINI_API_KEY=your-api-key-here

## Usage

Run the agent from the command line with a prompt:

```
python main.py "Your request here"
```

Example prompts:
* "List files in the directory": Calls get_files_info to list contents of ./calculator.
* "Read the content of example.py": Retrieves file content.
* "Run example.py": Executes the Python file in the working directory.
* "Write to newfile.py with content: print('Hello')": Writes the specified content.

The agent processes requests using Gemini, making function calls as needed, and outputs results. Use the --verbose flag for additional debug info.

For testing, place files in the ./calculator folder and run commands targeting them. The tests.py script demonstrates example calls to the functions.

## Project Structure

* main.py: Entry point for the command-line interface and Gemini interaction.
* get_files_info.py: Function to list files/directories.
* get_files_content.py: Function to read file contents (note: likely intended as get_file_content).
* run_python.py: Function to execute Python files.
* write_file.py: Function to write file contents.
* tests.py: Test script for function calls.
* requirements.txt: Project dependencies.
* calculator/: Sandbox working directory for tests (add your test files here).
* lorem.txt: Placeholder file (content: "wait, this isn't lorem ipsum").
