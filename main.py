import streamlit as st  #server
import faiss #local vector store
import numpy as np
from sentence_transformers import SentenceTransformer #embedding
import openai
import tempfile
import os
import google.generativeai as genai
import pandas as pd #reading csv files
import os
from openai import OpenAI

# Set up OpenAI API key


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])



# Initialize SentenceTransformer model
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Streamlit UI
st.set_page_config(page_title="ICT Cell AI Assistant ", page_icon=":speech_balloon:", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .chat-box {
        border: 2px solid #cccccc;
        border-radius: 10px;
        padding: 10px;
        background-color: #000000;
    }
    .chat-bubble {
        border-radius: 15px;
        padding: 10px;
        margin: 5px;
        max-width: 70%;
    }
    .user-bubble {
        background-color: #0b6122;
        align-self: flex-end;
    }
    .bot-bubble {
        background-color: #1b0765;
        align-self: flex-start;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("ICT Cell AI Assistant")
st.write("Upload a CSV file containing questions and answers, and start interacting with it!")

# CSV Upload
uploaded_file = st.file_uploader("Upload your CSV document", type=["csv"])

# Initialize variables
questions = []
answers = []
question_embeddings = None
index = None

if uploaded_file:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Ensure that the CSV has 'Question' and 'Answer' columns
    if 'Question' in df.columns and 'Answer' in df.columns:
        st.write("CSV uploaded successfully.")
        st.write("You can now start asking questions based on the content.")

        questions = df['Question'].tolist()
        answers = df['Answer'].tolist()

        # Embed the questions
        question_embeddings = embedder.encode(questions, show_progress_bar=True)

        # Build FAISS index
        dimension = question_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(question_embeddings))

        # Chatbox UI
        chat_history = []

        query = st.text_input("You:", "")

        if query:
            # Add user query to chat history
            chat_history.append(f'<div class="chat-bubble user-bubble">{query}</div>')

            # Embed the query
            query_embedding = embedder.encode([query])

            # Search the FAISS index
            distances, indices = index.search(query_embedding, k=3)

            # Retrieve the most relevant question-answer pair
            relevant_indices = indices[0]
            relevant_qas = [f"Question: {questions[i]}\n\n Answer: {answers[i]}" for i in relevant_indices]
            context = "\n\n".join(relevant_qas)
           # st.write("Relevant FAQs :"+ context)

            # Generate response using openai

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=200,
                messages=[
                    {"role": "system", "content": f"You are a helpful IT support assistant named Jarvis working for KIIT Deemed To Be University. Your role is to answer user queries about the problem faced by users. Refer to this knowledgebase in form of Question and Answer = {context} to frame your answer. Be funny and friendly in your tone. Introduce yourself with your name and organization name. Don't ask for clarifying questions. Answer if you know. Keep your answer crisp, bit more elaborative and close to the reference provided. "},
                    {
                        "role": "user",
                        "content": "Are you clear about your role?"
                    },
                    {
                        "role": "assistant",
                        "content": "Yes I am clear. Fire your queries"
                    },
                    {
                        "role": "user",
                        "content" : query
                    }

                ]
            )

            answer = completion.choices[0].message.content






            # Add bot response to chat history
            chat_history.append(f'<div class="chat-bubble bot-bubble">{answer}</div>')

            # Display chat history
            for message in chat_history:
                st.markdown(message, unsafe_allow_html=True)
    else:
        st.write("Please ensure your CSV contains 'Question' and 'Answer' columns.")
