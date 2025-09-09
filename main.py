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

    def _execute_github_script(self, github_raw_url):
        """
        The 'how to do things' recipe. It runs code from a GitHub link.
        """
        print(f"--- Action: Executing script from: {github_raw_url} ---")
        try:
            response = requests.get(github_raw_url)
            response.raise_for_status()
            script_code = response.text
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_script:
                temp_script.write(script_code)
                temp_script_path = temp_script.name
            process = subprocess.run(
                ['python', temp_script_path],
                capture_output=True, text=True, timeout=30
            )
            os.remove(temp_script_path)
            if process.returncode == 0:
                return f"--- Script Result ---\n{process.stdout}"
            else:
                return f"--- Script Error ---\n{process.stderr}"
        except Exception as e:
            return f"An error occurred: {e}"

    def _get_agent_response(self, prompt):
        """
        The 'how to chat' recipe. This is now configured for OpenAI's API.
        """
        self.conversation_history.append({"role": "user", "content": prompt})
        payload = { "model": self.model, "messages": self.conversation_history }
        headers = { 'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json' }

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            agent_text = result['choices'][0]['message']['content']
            if agent_text:
                self.conversation_history.append({"role": "assistant", "content": agent_text})
                return agent_text
            else:
                self.conversation_history.pop()
                return "Error: The AI's response was empty."
        except Exception as e:
            self.conversation_history.pop()
            return f"Error talking to the AI brain: {e}"

    def start_chat(self):
        """
        This function starts the conversation and listens for user input.
        """
        print("--- Your Python Agent is Ready (Using ChatGPT) ---")
        print("Command: run_github <raw_github_url>")
        print("Type 'quit' or 'exit' to end.")
        print("-" * 50)

        while True:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Agent: Goodbye!")
                break
            
            # --- THE FIX IS HERE! ---
            # We use .strip() to remove any accidental spaces at the start or end
            clean_input = user_input.strip()
            
            if clean_input.lower().startswith("run_github "):
                url = clean_input.split(" ", 1)[1]
                execution_result = self._execute_github_script(url)
                print(f"Agent: {execution_result}")
            else:
                agent_response = self._get_agent_response(user_input)
                print(f"Agent: {agent_response}")

if __name__ == "__main__":
    load_dotenv()
    API_URL = "https://api.openai.com/v1/chat/completions"
    API_KEY = os.getenv("OPENAI_API_KEY")
    SYSTEM_PROMPT = """You are a helpful and friendly AI assistant. Explain things simply."""
    my_agent = PythonAgent(api_url=API_URL, api_key=API_KEY, system_prompt=SYSTEM_PROMPT)
    my_agent.start_chat()

