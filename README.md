ChatBit is a conversational chatbot built using LangChain and the Groq API, leveraging the Gemma2-9b-IT language model. It can carry intelligent, stateful conversations and remember past interactions to maintain conversational context.

This project demonstrates how to implement a memory-enabled chatbot using LLMs, ideal for tasks that require continuity in dialogue (like support bots, AI assistants, etc.).

🧠 Features
🔐 Uses Groq API to access powerful LLMs

💾 Maintains conversation history with message memory

🧱 Built with LangChain abstractions

🛠️ Jupyter Notebook format for easy experimentation and customization

🛠️ Tech Stack
Python

LangChain

Groq

dotenv (.env) for secure API key management

📓 How It Works
Environment Setup: API key loaded from .env

Model Initialization: Connects to Gemma2-9b-It using ChatGroq

Human Interaction: User input is converted into HumanMessage

Response Generation: Model responds based on current and past messages

Memory: Past messages stored to preserve conversational context

