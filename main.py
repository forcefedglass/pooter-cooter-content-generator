import logging
import schedule
import time
from datetime import datetime
import os
from src.agents.web_agent import WebAgent
from src.agents.text_transformer import TextTransformer
from src.agents.image_generator import ImageGenerator
from src.agents.video_compiler import VideoCompiler
from config import SCHEDULE_CONFIG, PATHS

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(PATHS["LOGS"], 'app.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ContentOrchestrator:
    def __init__(self):
        self.web_agent = WebAgent()
        self.text_transformer = TextTransformer()
        self.image_generator = ImageGenerator()
        self.video_compiler = VideoCompiler()
        
        # Store daily posts
        self.daily_posts = []

    def create_post(self) -> bool:
        """
        Create a single post by orchestrating all agents
        """
        try:
            logger.info("Starting post creation process")
            
            # Get tales from web
            tales = self.web_agent.get_tales()
            if not tales:
                logger.error("No tales found")
                return False
            
            # Process random tale
            selected_tale = random.choice(tales)
            
            # Transform text
            processed_text = self.text_transformer.process_tale(selected_tale)
            if not processed_text:
                logger.error("Text processing failed")
                return False
            
            # Generate image
            image_path = self.image_generator.process_post(processed_text)
            if not image_path:
                logger.error("Image generation failed")
                return False
            
            # Store post details
            self.daily_posts.append({
                'text': processed_text,
                'image': image_path,
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info("Successfully created new post")
            return True
            
        except Exception as e:
            logger.error(f"Error in post creation: {str(e)}")
            return False

    def compile_daily_video(self) -> bool:
        """
        Create daily video compilation
        """
        try:
            logger.info("Starting daily video compilation")
            
            # Get all image paths from today's posts
            image_paths = [post['image'] for post in self.daily_posts]
            
            if not image_paths:
                logger.error("No images found for video compilation")
                return False
            
            # Compile video
            video_path = self.video_compiler.process_daily_compilation()
            
            if not video_path:
                logger.error("Video compilation failed")
                return False
            
            # Clear daily posts after successful compilation
            self.daily_posts = []
            
            logger.info(f"Successfully created daily video: {video_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error in video compilation: {str(e)}")
            return False

def setup_schedules(orchestrator: ContentOrchestrator):
    """
    Set up scheduled tasks
    """
    # Schedule posts throughout the day
    for post_time in SCHEDULE_CONFIG["POST_TIMES"]:
        schedule.every().day.at(post_time).do(orchestrator.create_post)
    
    # Schedule video compilation
    schedule.every().day.at(SCHEDULE_CONFIG["VIDEO_COMPILATION_TIME"]).do(
        orchestrator.compile_daily_video
    )

def main():
    """
    Main application entry point
    """
    try:
        logger.info("Starting Pooter Cooter Content Generator")
        
        # Create orchestrator
        orchestrator = ContentOrchestrator()
        
        # Set up schedules
        setup_schedules(orchestrator)
        
        # Run continuously
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
