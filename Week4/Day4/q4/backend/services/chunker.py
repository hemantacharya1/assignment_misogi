from langchain.text_splitter import RecursiveCharacterTextSplitter

# You can customize chunk size and overlap here
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def chunk_text(text: str) -> list[str]:
    return splitter.split_text(text)
