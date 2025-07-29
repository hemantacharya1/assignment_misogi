from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_unstructured import UnstructuredLoader

load_dotenv()
#create llm object
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")
embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
db_save_path = "db/faiss_index_gemini"

def load_file_and_store():
    print("process started----------")
    loader = UnstructuredLoader("sample_unstructured_test.pdf")
    documents = loader.load()
    print(documents)
    #split the text using recursive approch
    text_splitter=RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=20 )
    chunks = text_splitter.split_documents(documents)
    print(chunks)
     #create database from chunks and embedding model  
    db=FAISS.from_documents(chunks,embedding) 
    db.save_local(db_save_path)
    print("process ended-----------")
    return db


def query_function(question,loaded_db):
    similler_data=loaded_db.similarity_search(question,k=2)
    # prompt template and generation                                                                
    prompt_template = """
        Use the following context to answer the question:
        
        {context}
        
        Question: {question}
        
        Answer:
    """
    prompt=PromptTemplate.from_template(prompt_template)
    formatted_prompt=prompt.invoke({
        "context":"\n\n".join([doc.page_content for doc in similler_data]),
        "question":question
    })
    # print(formatted_prompt)
    final_response=llm.invoke(formatted_prompt)
    print(final_response.content)


def main():
    loaded_db = None
    try:
        # allow_dangerous_deserialization is needed for FAISS with custom embeddings
        loaded_db = FAISS.load_local(db_save_path, embedding, allow_dangerous_deserialization=True)
        print("Loaded DB from local")
    except Exception as e:
        print("Failed to load DB from local, creating a new one.")
    
    if not loaded_db:
        # Now we capture the returned database object
        loaded_db = load_file_and_store()
    
    if loaded_db:
        question = "What is this document about?"
        query_function(question, loaded_db)
    else:
        print("Database could not be loaded or created.")


if __name__=="__main__":
    main()

