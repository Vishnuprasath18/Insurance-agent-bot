import streamlit as st
import os
import nltk
from thirdai import licensing, neural_db as ndb
from openai import OpenAI

# Download NLTK data
nltk.download("punkt")

# Licensing and setup
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the keys
openai_api_key = os.getenv("OPENAI_API_KEY")
thirdai_license_key = os.getenv("THIRDAI_LICENSE_KEY")

# Now you can use these variables in your code
if thirdai_license_key:
    licensing.activate(thirdai_license_key)

openai_client = OpenAI(api_key=openai_api_key)

db = ndb.NeuralDB()
insertable_docs = []
doc_files = ["E:\lang and llama\insurance bot\data.pdf"]

for file in doc_files:
    doc = ndb.PDF(file)
    insertable_docs.append(doc)
db.insert(insertable_docs, train=False)


openai_client = OpenAI()

def generate_answers(query, references):
    context = "\n\n".join(references[:3])
    prompt = (
    f"You are an insurance chatbot designed to provide information about insurance plans. "
    f"Respond to the following question by providing clear, accurate, and relevant information about insurance plans. "
    f"Make sure to address the specifics of the plan and any important details that might help the user make an informed decision.\n"
    f"Question: {query}\n"
    f"Context: {context}\n"
    "Provide a short answer that helps the user understand their options.\n"
    "give specific answer withing 3-4 lines"
)

    messages = [{"role": "user", "content": prompt}]
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0
    )
    return response.choices[0].message.content

def generate_queries_chatgpt(original_query):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates multiple search queries based on a single input query."},
            {"role": "user", "content": f"Generate multiple search queries related to: {original_query}"},
            {"role": "user", "content": "OUTPUT (5 queries):"}
        ]
    )
    generated_queries = response.choices[0].message.content.strip().split("\n")
    return generated_queries

def get_references(query):
    search_results = db.search(query, top_k=1)
    references = [result.text for result in search_results]
    return references

def reciprocal_rank_fusion(reference_list, k=60):
    fused_scores = {}
    for i in reference_list:
        for rank, j in enumerate(i):
            if j not in fused_scores:
                fused_scores[j] = 0
            fused_scores[j] += 1 / ((rank+1) + k)
    reranked_results = {j: score for j, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)}
    return reranked_results

def get_answer(query, r):
    return generate_answers(query=query, references=r)

# Streamlit app
st.set_page_config(page_title="AI Insurance Agent Bot", page_icon=":hugging_face:", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #FFFFFF;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #FFFF00;
    }
    .text-input {
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #007BFF;
        background-color: #007BFF;
        color: #FFFFFF; 
    }
    .answer {
        font-size: 20px;
        color: #FFFF00; 
        background-color: #007BFF;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #DDD;
    }
    </style>
    <div class="title">AI Insurance Agent Bot</div>
    """,
    unsafe_allow_html=True
)

query = st.text_input("Do you have any question?", key="query_input", placeholder="Type your question here...", help="Enter your query related to insurance.")

if query:
    query_list = generate_queries_chatgpt(query)
    reference_list = [get_references(q) for q in query_list]
    r = reciprocal_rank_fusion(reference_list)
    ranked_reference_list = [i for i in r.keys()]
    ans = get_answer(query, ranked_reference_list)
    st.markdown(f"<div class='answer'>Answer: {ans}</div>", unsafe_allow_html=True)
