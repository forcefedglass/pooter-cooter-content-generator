import logging
import ffmpeg
import os
from typing import List, Optional
from datetime import datetime
import glob
from config import PATHS

logger = logging.getLogger(__name__)

class VideoCompiler:
    def __init__(self):
        self.output_path = PATHS["DAILY_VIDEO"]
        self.temp_path = PATHS["TEMP_IMAGES"]
        
        # Video settings
        self.duration_per_image = 5  # seconds
        self.transition_duration = 1  # seconds
        self.video_size = (1080, 1920)  # Instagram Reels/TikTok format
        self.fps = 30
        
        # Ensure output directory exists
        os.makedirs(self.output_path, exist_ok=True)

    def _create_transition(self, duration: int) -> ffmpeg.Stream:
        """
        Create a transition effect between images
        """
        try:
            # Create a black frame for transition
            transition = ffmpeg.input('color=c=black:s=1080x1920:d=1', f='lavfi')
            return transition
            
        except Exception as e:
            logger.error(f"Error creating transition: {str(e)}")
            return None

    def _prepare_image(self, image_path: str) -> ffmpeg.Stream:
        """
        Prepare an image for video inclusion
        """
        try:
            # Load image and scale it to video size
            stream = (
                ffmpeg
                .input(image_path, loop=1, t=self.duration_per_image)
                .filter('scale', self.video_size[0], self.video_size[1])
                .filter('setsar', '1/1')  # Set aspect ratio
                .filter('fps', fps=self.fps)
            )
            
            return stream
            
        except Exception as e:
            logger.error(f"Error preparing image: {str(e)}")
            return None

    def _add_fade_effects(self, stream: ffmpeg.Stream) -> ffmpeg.Stream:
        """
        Add fade in/out effects to a stream
        """
        try:
            return (
                stream
                .filter('fade', type='in', start_time=0, duration=0.5)
                .filter('fade', type='out', start_time=self.duration_per_image-0.5, duration=0.5)
            )
        except Exception as e:
            logger.error(f"Error adding fade effects: {str(e)}")
            return stream

    def compile_daily_video(self, image_paths: List[str]) -> Optional[str]:
        """
        Compile daily video from Instagram posts
        """
        try:
            if not image_paths:
                logger.error("No images provided for video compilation")
                return None
            
            # Create output filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            output_file = os.path.join(self.output_path, f"daily_compilation_{timestamp}.mp4")
            
            # Prepare streams for each image
            streams = []
            for img_path in image_paths:
                # Prepare image stream
                img_stream = self._prepare_image(img_path)
                if img_stream:
                    img_stream = self._add_fade_effects(img_stream)
                    streams.append(img_stream)
                    
                    # Add transition after image (except for last image)
                    if img_path != image_paths[-1]:
                        transition = self._create_transition(self.transition_duration)
                        if transition:
                            streams.append(transition)
            
            if not streams:
                logger.error("No valid streams created")
                return None
            
            # Concatenate all streams
            joined = ffmpeg.concat(*streams, v=1, a=0)
            
            # Add background music if available
            try:
                audio = ffmpeg.input('background_music.mp3')  # Replace with actual music file
                joined = ffmpeg.output(joined, audio, output_file,
                                    acodec='aac',
                                    vcodec='libx264',
                                    preset='medium',
                                    movflags='faststart',
                                    pix_fmt='yuv420p')
            except:
                # If no music or error, continue without audio
                joined = ffmpeg.output(joined, output_file,
                                    vcodec='libx264',
                                    preset='medium',
                                    movflags='faststart',
                                    pix_fmt='yuv420p')
            
            # Run the ffmpeg command
            joined.overwrite_output().run(capture_stdout=True, capture_stderr=True)
            
            return output_file
            
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
            return None
            
        except Exception as e:
            logger.error(f"Error compiling video: {str(e)}")
            return None

    def get_daily_images(self) -> List[str]:
        """
        Get all images created today for compilation
        """
        try:
            today = datetime.now().strftime("%Y%m%d")
            pattern = os.path.join(self.temp_path, f"instagram_{today}*.png")
            
            # Get all matching files and sort by creation time
            files = glob.glob(pattern)
            files.sort(key=os.path.getctime)
            
            return files
            
        except Exception as e:
            logger.error(f"Error getting daily images: {str(e)}")
            return []

    def cleanup_old_files(self, days_to_keep: int = 7):
        """
        Clean up old temporary files and videos
        """
        try:
            current_time = datetime.now().timestamp()
            
            # Clean up temp images
            for file in glob.glob(os.path.join(self.temp_path, "*.png")):
                if (current_time - os.path.getctime(file)) > (days_to_keep * 86400):
                    try:
                        os.remove(file)
                    except Exception as e:
                        logger.warning(f"Could not remove file {file}: {str(e)}")
            
            # Clean up old videos
            for file in glob.glob(os.path.join(self.output_path, "*.mp4")):
                if (current_time - os.path.getctime(file)) > (days_to_keep * 86400):
                    try:
                        os.remove(file)
                    except Exception as e:
                        logger.warning(f"Could not remove file {file}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def process_daily_compilation(self) -> Optional[str]:
        """
        Main method to handle daily video compilation
        """
        try:
            # Get today's images
            images = self.get_daily_images()
            
            if not images:
                logger.warning("No images found for today's compilation")
                return None
            
            # Compile video
            video_path = self.compile_daily_video(images)
            
            if video_path:
                # Clean up old files
                self.cleanup_old_files()
                
            return video_path
            
        except Exception as e:
            logger.error(f"Error processing daily compilation: {str(e)}")
            return None
