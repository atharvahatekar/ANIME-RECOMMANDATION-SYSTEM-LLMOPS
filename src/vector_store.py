from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings


from dotenv import load_dotenv
load_dotenv()

class AnimeVectorStore:
    def __init__(self, csv_path: str, persist_directory: str = "chroma_db"):
        self.csv_path = csv_path
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_vectorstore(self):
        # Load the CSV file
        loader = CSVLoader(file_path=self.csv_path,
                           encoding='utf-8',
                           metadata_columns=[]
                           )
        
        data = loader.load()

        # Split the text into manageable chunks
        text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
        splitted_text = text_splitter.split_documents(data)


        # Create and persist the vector store
        db = Chroma.from_documents(
            splitted_text,
            self.embeddings,
            persist_directory=self.persist_directory
        )
        
        db.persist()

    def load_vectorstore(self):
        # Load the persisted vector store
        return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
