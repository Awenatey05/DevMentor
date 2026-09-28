import requests

from config import OLLAMA_URL, MODEL_NAME
from prompts import SYSTEM_PROMPT



# Check if Ollama is available 
def check_ollama():
    """Check whether Ollama is available."""
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
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
        f"{OLLAMA_URL}/api/tags",
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
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=120
    )
    
    response.raise_for_status()
    
    return response.json()["response"]

def chat_llm(messages):

    model = MODEL_NAME
    base_url = OLLAMA_URL

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

# def prompt_assistant(user_prompt, system_prompt):
#     messages = [
#         {"role": "system",
#          "content": system_prompt},
#         {"role": "user",
#          "content": user_prompt}
#     ]
#     return chat_llm(messages)

# Part 3 version — uses conversation memory
def prompt_assistant(user_prompt):
    messages.append(
        {"role": "user", "content": user_prompt}
    )

    reply = chat_llm(messages)

    messages.append(
        {"role": "assistant", "content": reply}
    )

    return reply

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]
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
    print("Type /exit to stop.")
    print("Type /reset to clear the conversation.")
    print("Type /history to view the conversation.\n")

    while True:
        prompt = input("You: ").strip()

        if not prompt:
            print("Please enter a message.")
            continue

        command = prompt.lower()

        if command == "/exit":

            print("Goodbye!")
            break

        if command == "/reset":
            messages.clear()
            messages.append(
                {"role": "system", "content": SYSTEM_PROMPT}
            )
            print("\nConversation reset.\n")
            continue

        if command == "/history":
            messages_to_show = messages[1:]

            for message in messages_to_show:
                print(f"{message['role']}: {message['content']}")

            print()
            continue


        try:
            answer = prompt_assistant(prompt)

        except requests.exceptions.ConnectionError:
            print("\nERROR: Could not connect to Ollama.")
            messages.pop()
            continue

        except requests.exceptions.RequestException as error:
            print(f"\nAPI ERROR: {error}")
            messages.pop()
            continue

        print("\nDevMentor:")
        print(answer)
        print()

    
       
