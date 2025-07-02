🚀 Overview
ChatBit is a simple yet powerful chatbot that demonstrates how to build a memory-enabled conversational agent using Large Language Models (LLMs). The chatbot can hold multi-turn conversations, remember past user inputs, and provide context-aware responses. It uses the Gemma2-9b-It model via Groq API for blazing fast inference and language understanding.


.

.

.

.

.

.

🎯 Features
🔁 Multi-turn conversations with memory

🧠 Remembers context using ChatMessageHistory

🔗 Powered by LangChain and Groq API

🧪 Easy-to-test Python notebook format

📜 Well-documented sample conversation flow
.

.

.

.

.

.

.

.

🛠️ Tech Stack
LangChain (langchain_core, langchain_community, langchain_groq)

Groq API for LLM inference

Python and Jupyter Notebook

.env for secure API key storage
.

.

.

.

.

.

.

.


🧠 How It Works
User inputs are wrapped in HumanMessage objects.

Model responses are generated via ChatGroq.

All messages are stored in a ChatMessageHistory.

The history is reused to make the chatbot context-aware.
.

.

.

.

.

.

.

.



📚 Educational Use
This chatbot serves as a starter project for:

Learning LLM memory handling

Understanding LangChain's message and history framework

Exploring LLM-powered assistant applications

.

.

.

.

.

.

.

.

.

 Files
chatbit.ipynb: Main notebook with complete code

.env: API key storage (not included, user must create)

README.md: Project description (this file)

