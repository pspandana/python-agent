import requests
import json
import os
import subprocess
import tempfile
from dotenv import load_dotenv

class PythonAgent:
    """
    This is the blueprint for our robot helper. It holds all the skills
    and properties of the agent.
    """

    def __init__(self, api_url, api_key, system_prompt, model="gpt-3.5-turbo"):
        """
        The 'setup' recipe that runs when we build a new robot.
        It sets the agent's personality and tools.
        """
        if not api_key:
            raise ValueError("API_KEY is not set. Please check your .env file.")
        self.api_url = api_url
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.model = model
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

    def _execute_local_script(self, file_path):
        """
        Execute a Python script from the local file system.
        """
        print(f"--- Action: Executing local script: {file_path} ---")
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' not found."
            
            # Set environment variables to force UTF-8 encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'
            
            process = subprocess.run(
                ['python', '-X', 'utf8', file_path],
                capture_output=True, 
                text=True, 
                timeout=30,
                env=env
            )
            
            if process.returncode == 0:
                return f"--- Script Result ---\n{process.stdout}"
            else:
                return f"--- Script Error ---\n{process.stderr}"
                
        except subprocess.TimeoutExpired:
            return "Error: Script execution timed out (30 seconds limit)."
        except Exception as e:
            return f"An error occurred: {e}"

    def _execute_github_script(self, github_raw_url):
        """
        The 'how to do things' recipe. It runs code from a GitHub link.
        Fixed to handle encoding issues properly.
        """
        print(f"--- Action: Executing script from: {github_raw_url} ---")
        try:
            # Check if URL is a raw GitHub URL
            if "raw.githubusercontent.com" not in github_raw_url:
                return "Error: Please use a raw GitHub URL (raw.githubusercontent.com). Regular GitHub URLs won't work."
            
            response = requests.get(github_raw_url, timeout=10)
            response.raise_for_status()
            script_code = response.text
            
            # Create temporary file with UTF-8 encoding
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_script:
                temp_script.write(script_code)
                temp_script_path = temp_script.name
                
            # Execute the script with proper encoding handling
            # Set multiple environment variables to force UTF-8 encoding on Windows
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'
            
            process = subprocess.run(
                ['python', '-X', 'utf8', temp_script_path],
                capture_output=True, 
                text=True, 
                timeout=30,
                env=env
            )
            
            # Clean up temporary file
            os.remove(temp_script_path)
            
            if process.returncode == 0:
                return f"--- Script Result ---\n{process.stdout}"
            else:
                return f"--- Script Error ---\n{process.stderr}"
                
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Check your internet connection."
        except requests.exceptions.RequestException as e:
            return f"Error fetching script: {e}"
        except subprocess.TimeoutExpired:
            return "Error: Script execution timed out (30 seconds limit)."
        except Exception as e:
            return f"An error occurred: {e}"

    def _get_agent_response(self, prompt):
        """
        The 'how to chat' recipe. This is now configured for OpenAI's API.
        """
        self.conversation_history.append({"role": "user", "content": prompt})
        payload = { 
            "model": self.model, 
            "messages": self.conversation_history,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        headers = { 
            'Authorization': f'Bearer {self.api_key}', 
            'Content-Type': 'application/json' 
        }

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload), timeout=30)
            response.raise_for_status()
            result = response.json()
            agent_text = result['choices'][0]['message']['content']
            if agent_text:
                self.conversation_history.append({"role": "assistant", "content": agent_text})
                return agent_text
            else:
                self.conversation_history.pop()
                return "Error: The AI's response was empty."
        except requests.exceptions.Timeout:
            self.conversation_history.pop()
            return "Error: Request to AI timed out. Please try again."
        except requests.exceptions.RequestException as e:
            self.conversation_history.pop()
            return f"Error talking to the AI brain: {e}"
        except Exception as e:
            self.conversation_history.pop()
            return f"Error talking to the AI brain: {e}"

    def start_chat(self):
        """
        This function starts the conversation and listens for user input.
        """
        print("--- Your Python Agent is Ready (Using ChatGPT) ---")
        print("Commands:")
        print("  run_local <file_path>     - Run a Python script from your computer")
        print("  run_github <raw_url>      - Run a Python script from GitHub")
        print("  Type 'quit' or 'exit' to end.")
        print("  Remember: Use raw.githubusercontent.com URLs for GitHub!")
        print("-" * 60)

        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit']:
                    print("Agent: Goodbye!")
                    break
                
                # Clean input and process commands
                clean_input = user_input.strip()
                
                if clean_input.lower().startswith("run_local "):
                    file_path = clean_input.split(" ", 1)[1].strip()
                    execution_result = self._execute_local_script(file_path)
                    print(f"Agent: {execution_result}")
                    
                elif clean_input.lower().startswith("run_github "):
                    url = clean_input.split(" ", 1)[1].strip()
                    execution_result = self._execute_github_script(url)
                    print(f"Agent: {execution_result}")
                    
                else:
                    agent_response = self._get_agent_response(user_input)
                    print(f"Agent: {agent_response}")
                    
            except KeyboardInterrupt:
                print("\nAgent: Goodbye!")
                break
            except Exception as e:
                print(f"Agent: An unexpected error occurred: {e}")

if __name__ == "__main__":
    load_dotenv()
    API_URL = "https://api.openai.com/v1/chat/completions"
    API_KEY = os.getenv("OPENAI_API_KEY")
    SYSTEM_PROMPT = """You are a helpful and friendly AI assistant that can execute Python code. 
    You can help with coding questions, run scripts, and assist with various tasks. 
    Explain things clearly and be concise in your responses."""
    
    try:
        my_agent = PythonAgent(api_url=API_URL, api_key=API_KEY, system_prompt=SYSTEM_PROMPT)
        my_agent.start_chat()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please make sure your .env file contains OPENAI_API_KEY=your_key_here")
    except Exception as e:
        print(f"Startup Error: {e}")