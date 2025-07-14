from src.data_loader import AnimeDataLoader
from src.vector_store import AnimeVectorStore
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting to build Anime Recommendation Pipeline")
        # Initialize the data loader
        data_loader = AnimeDataLoader(original_csv="data/anime_with_synopsis.csv", processed_csv="data/processed_anime_data.csv")
        
        processed_csv = data_loader.load_and_process()

        logger.info("Data loaded and processed successfully")

        # Initialize the vector store
        vector_builder = AnimeVectorStore(processed_csv)
        vector_builder.build_and_save_vectorstore()

        logger.info("Vector store built and saved successfully")

        logger.info("Anime Recommendation Pipeline built successfully")
    except Exception as e:
        logger.error(f"An error occurred while building the pipeline: {e}")
        raise CustomException("Pipeline build failed") from e

if __name__ == "__main__":
    main()