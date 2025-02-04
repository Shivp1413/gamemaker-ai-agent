from langchain_community.llms import Ollama
import time
from threading import Thread
from queue import Queue
from .code_version import CodeVersion
from utils.message_formatter import clean_message, extract_version_content
from config.prompts import BASE_PROMPT

class LLMConversation:
    def __init__(self):
        self.base_prompt = BASE_PROMPT
        self.llm1 = Ollama(
            model="qwen:14b",
            temperature=0.7,
            timeout=60
        )
        self.llm2 = Ollama(
            model="qwen:14b",
            temperature=0.7,
            timeout=60
        )
        self.conversation_history = []
        self.is_running = False
        self.thread = None
        self.queue = Queue()
        self.code_versions = []
        self.version_counter = 1

    def save_code_version(self, message):
        try:
            content = extract_version_content(message)
            if not content:
                return False

            version = CodeVersion(
                code=content["code"],
                description=content["description"],
                version_number=self.version_counter,
                run_instructions=content["instructions"]
            )
            
            self.code_versions.append(version)
            self.version_counter += 1
            
            self.add_to_history("System", f"""✨ Version {self.version_counter-1} is complete!

{content['description']}

How to run:
{content['instructions']}""")
            
            return True
            
        except Exception as e:
            self.add_to_history("Error", f"Failed to create version: {str(e)}")
            return False

    def add_to_history(self, speaker, message):
        if "===VERSION_START===" in message:
            self.save_code_version(message)
        else:
            cleaned_message = clean_message(message)
            self.conversation_history.append({
                "speaker": speaker,
                "message": cleaned_message,
                "timestamp": time.strftime("%H:%M:%S")
            })

    def format_prompt(self, message, is_llm1):
        role = "AI 1" if is_llm1 else "AI 2"
        other_role = "AI 2" if is_llm1 else "AI 1"
        
        return f"""{self.base_prompt}

You are {role} working with {other_role}.

Previous message: {message}

Remember:
1. Format all code in ```python ``` blocks
2. Discuss implementation clearly
3. Only submit versions when both agree
4. Keep improving the game"""

    def run_conversation(self, initial_question):
        current_prompt = f"Create this game: {initial_question}"
        while self.is_running:
            try:
                formatted_prompt1 = self.format_prompt(current_prompt, is_llm1=True)
                response1 = self.llm1(formatted_prompt1)
                self.queue.put(("AI 1", response1))
                
                formatted_prompt2 = self.format_prompt(response1, is_llm1=False)
                response2 = self.llm2(formatted_prompt2)
                self.queue.put(("AI 2", response2))
                
                current_prompt = response2
                
            except Exception as e:
                self.queue.put(("Error", str(e)))
                self.is_running = False
                break
            
            time.sleep(0.1)

    def start_conversation(self, initial_question):
        if not self.is_running:
            self.is_running = True
            self.thread = Thread(target=self.run_conversation, args=(initial_question,))
            self.thread.start()

    def stop_conversation(self):
        if self.is_running:
            self.is_running = False
            if self.thread and self.thread.is_alive():
                self.thread.join()
                self.thread = None