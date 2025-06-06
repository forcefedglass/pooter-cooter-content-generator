import logging
import requests
import os
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import io
from config import API_KEYS, PATHS

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self):
        self.api_key = API_KEYS["IMAGE_GEN"]
        self.image_size = (1080, 1080)  # Instagram square format
        self.font_size = 48
        self.font_color = (255, 255, 255)  # White text
        self.background_color = (0, 0, 0)  # Black background
        
        # Ensure temp directory exists
        os.makedirs(PATHS["TEMP_IMAGES"], exist_ok=True)

    def _create_prompt(self, text: str) -> str:
        """
        Convert text into an image generation prompt
        """
        # Remove any explicit references to avoid API rejections
        cleaned_text = text.replace("Pooter Cooter", "rock band")
        
        # Create an artistic prompt
        prompt = f"A surreal, artistic interpretation of: {cleaned_text}. "
        prompt += "Style: dark, dramatic, high contrast, professional photography"
        
        return prompt

    def generate_image(self, text: str) -> Optional[str]:
        """
        Generate an image using the image generation API
        Returns the path to the generated image
        """
        try:
            prompt = self._create_prompt(text)
            
            # API endpoint (replace with actual endpoint)
            url = "https://api.imagegeneration.com/v1/generate"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
                "response_format": "url"
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Get image URL from response
            image_url = response.json()["data"][0]["url"]
            
            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Save the image
            timestamp = int(time.time())
            image_path = os.path.join(PATHS["TEMP_IMAGES"], f"generated_{timestamp}.png")
            
            with open(image_path, "wb") as f:
                f.write(image_response.content)
            
            return image_path
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return self._create_fallback_image(text)

    def _create_fallback_image(self, text: str) -> Optional[str]:
        """
        Create a simple text-based image as fallback
        """
        try:
            # Create new image with black background
            image = Image.new('RGB', self.image_size, self.background_color)
            draw = ImageDraw.Draw(image)
            
            # Load a font (fallback to default if custom font fails)
            try:
                font = ImageFont.truetype("Arial.ttf", self.font_size)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            wrapped_text = self._wrap_text(text, font, self.image_size[0] - 100)
            
            # Calculate text position (center)
            text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (self.image_size[0] - text_width) / 2
            y = (self.image_size[1] - text_height) / 2
            
            # Add text
            draw.multiline_text(
                (x, y),
                wrapped_text,
                font=font,
                fill=self.font_color,
                align="center"
            )
            
            # Save image
            timestamp = int(time.time())
            image_path = os.path.join(PATHS["TEMP_IMAGES"], f"fallback_{timestamp}.png")
            image.save(image_path)
            
            return image_path
            
        except Exception as e:
            logger.error(f"Error creating fallback image: {str(e)}")
            return None

    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> str:
        """
        Wrap text to fit within specified width
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line = ' '.join(current_line)
            bbox = font.getbbox(line)
            width = bbox[2] - bbox[0]
            
            if width > max_width:
                if len(current_line) == 1:
                    lines.append(current_line[0])
                    current_line = []
                else:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)

    def create_instagram_post(self, text: str, image_path: str) -> Optional[str]:
        """
        Create final Instagram post image with "Did You Know..." format
        """
        try:
            # Open generated image
            with Image.open(image_path) as img:
                # Resize if needed
                if img.size != self.image_size:
                    img = img.resize(self.image_size)
                
                # Create drawing object
                draw = ImageDraw.Draw(img)
                
                # Add "Did You Know..." header
                try:
                    header_font = ImageFont.truetype("Arial-Bold.ttf", 60)
                except:
                    header_font = ImageFont.load_default()
                
                header_text = "Did You Know..."
                header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
                header_width = header_bbox[2] - header_bbox[0]
                
                # Draw header with background
                x = (self.image_size[0] - header_width) / 2
                y = 50
                
                # Draw semi-transparent background for header
                padding = 20
                draw.rectangle(
                    [x - padding, y - padding,
                     x + header_width + padding, y + header_bbox[3] - header_bbox[1] + padding],
                    fill=(0, 0, 0, 128)
                )
                
                # Draw header text
                draw.text((x, y), header_text, font=header_font, fill=self.font_color)
                
                # Save final image
                timestamp = int(time.time())
                final_path = os.path.join(PATHS["TEMP_IMAGES"], f"instagram_{timestamp}.png")
                img.save(final_path)
                
                return final_path
                
        except Exception as e:
            logger.error(f"Error creating Instagram post: {str(e)}")
            return None

    def process_post(self, text: str) -> Optional[str]:
        """
        Main method to generate a complete Instagram post
        """
        try:
            # Generate base image
            base_image_path = self.generate_image(text)
            if not base_image_path:
                return None
            
            # Create Instagram post format
            final_path = self.create_instagram_post(text, base_image_path)
            
            # Clean up base image
            try:
                os.remove(base_image_path)
            except:
                pass
            
            return final_path
            
        except Exception as e:
            logger.error(f"Error processing post: {str(e)}")
            return None
