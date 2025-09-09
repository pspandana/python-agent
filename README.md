# Python Agent - AI Assistant That Can Run Code

A smart Python assistant that can both chat with you AND run Python scripts from GitHub or your computer.

## What Does This Do?

This project creates an AI assistant that has two main abilities:
1. **Chat Mode**: Talk to you like ChatGPT - answer questions, help with coding, explain things
2. **Action Mode**: Actually run Python code from GitHub URLs or local files on your computer

Think of it as ChatGPT with hands - it can not only talk but also DO things!

## Features

✅ **Smart Conversations**: Uses OpenAI's ChatGPT to chat and help you  
✅ **Run GitHub Scripts**: Download and execute Python code from any GitHub repository  
✅ **Run Local Scripts**: Execute Python files from your computer  
✅ **Safe Execution**: 30-second timeout to prevent scripts from running forever  
✅ **Easy Commands**: Simple `run_github` and `run_local` commands  
✅ **Memory**: Remembers your conversation history for better context  

## Files in This Project

### `main.py` - The Main Agent
This is your AI assistant. It contains:
- **PythonAgent class**: The brain of your assistant
- **Chat functionality**: Talks to OpenAI's API
- **Script execution**: Downloads and runs code from GitHub
- **Command interface**: Simple text commands to control the agent

### `test.py` - Example Script
A simple test script that:
- Prints success messages with emojis 🚀
- Shows a random "lucky number" 
- Demonstrates that remote code execution works

### `requirements.txt` - Dependencies
Lists the Python packages you need:
- `requests`: For making web requests
- `python-dotenv`: For loading your API key safely

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Your API Key
Create a file called `.env` in your project folder:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Agent
```bash
python main.py
```

## How to Use

### Chat Mode (Default)
Just type anything and your agent will respond:
```
You: How do I create a Python list?
Agent: You can create a Python list using square brackets...
```

### Run GitHub Scripts
Use the `run_github` command with a raw GitHub URL:
```
You: run_github https://raw.githubusercontent.com/username/repo/main/script.py
Agent: --- Script Result ---
Hello from GitHub!
```

### Run Local Scripts
Use the `run_local` command with a file path:
```
You: run_local my_script.py
Agent: --- Script Result ---
Script executed successfully!
```

### Exit
Type `quit` or `exit` to stop the agent.

## Important Notes

### Security Warning ⚠️
This agent will run ANY Python code you give it! Only use trusted scripts because:
- Scripts can access your files
- Scripts can see your environment variables
- Scripts can make network requests

### GitHub URLs Must Be "Raw"
Use raw GitHub URLs that look like:
- ✅ `https://raw.githubusercontent.com/user/repo/main/file.py`
- ❌ `https://github.com/user/repo/blob/main/file.py`

## Example Session

```
--- Your Python Agent is Ready (Using ChatGPT) ---
Commands:
  run_local <file_path>     - Run a Python script from your computer
  run_github <raw_url>      - Run a Python script from GitHub
  Type 'quit' or 'exit' to end.
------------------------------------------------------------

You: What's the weather like in Python?
Agent: I think you mean how to get weather data in Python! You can use...

You: run_github https://raw.githubusercontent.com/pspandana/python-agent/main/test.py
--- Action: Executing script from: https://raw.githubusercontent.com/pspandana/python-agent/main/test.py ---
Agent: --- Script Result ---
🚀 Success! Running from GitHub!
Agent is working perfectly!
Your lucky number is: 42

You: quit
Agent: Goodbye!
```

## Troubleshooting

### "API_KEY is not set" Error
- Make sure your `.env` file exists
- Check that it contains `OPENAI_API_KEY=your_key`
- Restart the agent after creating the `.env` file

### Encoding Errors with Emojis
- This is a Windows-specific issue
- Remove emojis from your scripts, or
- Run the agent from a UTF-8 capable terminal

### "404 Not Found" for GitHub URLs
- Make sure you're using the "raw" GitHub URL
- Check that the repository and file actually exist
- Verify the URL is public (or you have access)

## What Makes This Special?

Most AI assistants can only talk. This one can:
- **Actually run code** instead of just explaining it
- **Fetch scripts from the internet** and execute them
- **Remember your conversation** for better help
- **Work with both local and remote code**

It's like having a coding assistant that can not only give you advice but also test and run the code for you!

## Future Ideas

- Add support for more programming languages
- Create a web interface instead of command line
- Add code editing and file management features
- Build in code analysis and security scanning
- Add support for private GitHub repositories

## Contributing

Want to improve this project? Here are some ways to help:
- Report bugs or issues
- Suggest new features
- Add better error handling
- Improve security features
- Write more example scripts

## License

This project is open source. Feel free to use, modify, and share it!

---

**Happy coding with your AI assistant! 🚀**