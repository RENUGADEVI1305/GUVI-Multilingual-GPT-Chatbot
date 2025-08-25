# GUVI-Multilingual-GPT-Chatbot

# Project Title - 🌍 GUVI Multilingual GPT Chatbot using Streamlit – Integrated Translation and Domain-Specific Model Deployment
This project is a multilingual AI chatbot for GUVI, built using RAG (Retrieval-Augmented Generation) with HuggingFace models, LangChain, FAISS, and Streamlit.
It supports English, Tamil, Hindi, Telugu, Kannada with auto-detection of language.

## Overview
Build a multilingual chatbot that uses a pre-trained or fine-tuned GPT model to answer user queries. If the user’s input is in a non-English language, the chatbot should translate the input to English using some translator model, get a response from the GPT model, and then translate the response back to the original language.

## 🚀 Features

Multilingual Support: Auto-detect and translate between English, Tamil, Hindi, Telugu, and Kannada.

RAG-based Answering: Uses FAISS vector search + FLAN-T5 for concise, factual answers.

Fallback Knowledge Base: Preloaded answers for common GUVI FAQs.

Clean Responses: Strips out extra text, limits answers to 2–4 sentences.

Interactive UI: Built with Streamlit, with clear chat and language options.

Ngrok Integration: Run on Colab or local machine with a public link.

## 📂 Project Structure

├── app.py # Streamlit app (UI + chatbot) 

├── multilingual_utils.py # Language detection + translation

├── retriever.py # RAG retriever (FAISS + HuggingFace + LangChain) 

├── GUVIinfo.txt # Knowledge base document 

├── requirements.txt # Dependencies 

└── README.md # Documentation

## 🧠 How it Works 

User Input → Language detected (langdetect). 

Translate to English → Using Deep Translator. 

RAG Pipeline → FAISS retrieves relevant chunks, HuggingFace FLAN-T5 generates answer. 

Clean Answer → Shortened to 2–4 sentences. 

Translate Back → Response shown in user’s input language. 

Display in Streamlit → Chat history maintained.

## 🛠️ Tech Stack 

Streamlit → UI & chatbot interface 

LangChain → RAG pipeline orchestration 

FAISS → Vector similarity search 

HuggingFace (FLAN-T5) → Language model 

Deep Translator → Translation 

LangDetect → Auto language detection 

Pyngrok → Public hosting
