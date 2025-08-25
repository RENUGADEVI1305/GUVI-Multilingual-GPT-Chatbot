
import os
import re
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS as LangFAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# ---------------------------
# 1. Load documents
# ---------------------------
def load_documents(path="/content/GUVIinfo.txt"):
    loader = TextLoader(path, encoding="utf-8")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

# ---------------------------
# 2. Build FAISS Index
# ---------------------------
def build_faiss_index(docs):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = LangFAISS.from_documents(docs, embeddings)
    return vectorstore

# ---------------------------
# 3. Load instruction-tuned LLM (FLAN-T5)
# ---------------------------
def load_llm(model_name="google/flan-t5-base"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    generator = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=150,
        temperature=0.3,  # lower = more factual
    )

    return HuggingFacePipeline(pipeline=generator)

# ---------------------------
# 4. Strict concise QA prompt
# ---------------------------
QA_PROMPT = PromptTemplate(
    template='''You are a helpful assistant for GUVI.
Use only the following context to answer the user's question.
Do NOT add unrelated text, links, or jokes.

Context:
{context}

Question: {question}
Answer in 2-4 sentences only:
''',
    input_variables=["context", "question"],
)

# ---------------------------
# 5. Build RAG Chain
# ---------------------------
def build_rag_chain():
    docs = load_documents("/content/GUVIinfo.txt")
    vectorstore = build_faiss_index(docs)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = load_llm()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
    )
    return qa_chain

qa_chain = build_rag_chain()

# ---------------------------
# 6. Cleanup answer
# ---------------------------
def clean_answer(ans: str) -> str:
    import re
    ans = re.sub(r"http\S+|www\S+", "", ans)              # remove URLs
    ans = ans.replace("Helpful Answer:", "").strip()      # remove prefix
    sentences = re.split(r'(?<=[.!?]) +', ans)            # split into sentences
    return " ".join(sentences[:4]).strip()                # keep max 4 sentences


# ---------------------------
# 7. Main function
# ---------------------------
def generate_answer(query: str) -> str:
    result = qa_chain.invoke({"query": query})
    raw_answer = result["result"]
    return clean_answer(raw_answer)


