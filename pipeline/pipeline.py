from src.vector_store import AnimeVectorStore
from src.recommander import AnimeRecommender
from config.config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException


logger = get_logger(__name__)

class AnimeRecommendationPipeline:
    def __init__(self, persist_directory: str = "chroma_db"):
        try:
            logger.info("Initializing AnimeRecommendationPipeline")
            
            self.vector_store_builder = AnimeVectorStore(csv_path="", persist_directory=persist_directory)

            retriever = self.vector_store_builder.load_vectorstore().as_retriever()

            self.recommender = AnimeRecommender(
                retriever = retriever,
                api_key = GROQ_API_KEY,
                model_name = MODEL_NAME
            )
            logger.info("AnimeRecommendationPipeline initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing AnimeRecommendationPipeline: {e}")
            raise CustomException("Failed to initialize AnimeRecommendationPipeline")

    def run(self, query: str) -> str:
        try:
            logger.info(f"Received a query: {query}")
            recommendations = self.recommender.get_recommendations(query)
            logger.info(f"Recommendations found: {recommendations}")
            return recommendations
        except Exception as e:
            logger.error(f"Error occurred while getting recommendations: {e}")
            raise CustomException("Failed to get recommendations")