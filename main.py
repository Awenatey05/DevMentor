import requests 
from prompts import SYSTEM_PROMPT

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "llama3.2:latest"


# Check if Ollama is available 
def check_ollama():
    """Check whether Ollama is available."""
    try:
        response = requests.get(
            f"{OLLAMA_HOST}/api/tags",
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False


# List available models
def list_models():
    """Return locally available Ollama models."""
    
    response = requests.get(
        f"{OLLAMA_HOST}/api/tags",
        timeout=10
    )
    
    response.raise_for_status()
    
    data = response.json()
    
    return [
        model["name"]
        for model in data["models"]
    ]


def ask_llm(prompt, model=MODEL_NAME):
    """Send a prompt to the local LLM."""
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json=payload,
        timeout=120
    )
    
    response.raise_for_status()
    
    return response.json()["response"]

def chat_llm(messages):

    model = MODEL_NAME
    base_url = OLLAMA_HOST

    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    response = requests.post(
        f"{base_url}/api/chat",
        json=payload,
        timeout=120
    )
    response.raise_for_status()

    return response.json()["message"]["content"]

def prompt_assistant(user_prompt, system_prompt):
    messages = [
        {"role": "system",
         "content": system_prompt},
        {"role": "user",
         "content": user_prompt}
    ]
    return chat_llm(messages)

# ------------------------------------------------
# Application
# ------------------------------------------------

if not check_ollama():
    print("\nOllama is not running.")
else:
    
    print("\nOllama is running.")
    
    print("\nAvailable models:")
    
    for model in list_models():
        print("-", model)
    
    print("\nDevMentor:")
    print("Type 'exit' to stop.\n")
    
    while True:
        prompt = input("You: ")
        
        if prompt.lower() == "exit":
            break
        
        answer = prompt_assistant(prompt, SYSTEM_PROMPT)
        
        print("\nDevMentor:")
        print(answer)
        print()
