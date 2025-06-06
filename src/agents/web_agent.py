import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Optional
import re
from config import SEARCH_CONFIG

logger = logging.getLogger(__name__)

class WebAgent:
    def __init__(self):
        self.headers = {
            "User-Agent": SEARCH_CONFIG["USER_AGENT"]
        }
        self.timeout = SEARCH_CONFIG["TIMEOUT"]

    def _replace_band_name(self, text: str) -> str:
        """Replace all instances of 'Anal Cunt' with 'Pooter Cooter'"""
        pattern = re.compile(r'Anal\s*Cunt', re.IGNORECASE)
        return pattern.sub('Pooter Cooter', text)

    def search_for_tales(self) -> List[str]:
        """
        Search the web for outrageous tales about the band
        Returns a list of cleaned text stories
        """
        try:
            # Example sources - can be expanded
            sources = [
                "https://en.wikipedia.org/wiki/Anal_Cunt",
                # Add more sources as needed
            ]
            
            stories = []
            
            for url in sources:
                try:
                    response = requests.get(url, headers=self.headers, timeout=self.timeout)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Remove unwanted elements
                    for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                        element.decompose()
                    
                    # Extract text content
                    text = soup.get_text()
                    
                    # Clean the text
                    text = self._clean_text(text)
                    
                    # Replace band name
                    text = self._replace_band_name(text)
                    
                    if text:
                        stories.append(text)
                
                except requests.RequestException as e:
                    logger.error(f"Error fetching {url}: {str(e)}")
                    continue
            
            return stories
        
        except Exception as e:
            logger.error(f"Error in search_for_tales: {str(e)}")
            return []

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Remove multiple consecutive punctuation
        text = re.sub(r'([.,!?])\1+', r'\1', text)
        
        # Ensure proper spacing after punctuation
        text = re.sub(r'([.,!?])(\w)', r'\1 \2', text)
        
        return text.strip()

    def extract_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        # Split on double newlines or multiple consecutive newlines
        paragraphs = re.split(r'\n\n+', text)
        
        # Clean each paragraph
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return paragraphs

    def get_tales(self) -> Optional[List[str]]:
        """
        Main method to get processed tales
        Returns a list of cleaned paragraphs or None if no content found
        """
        stories = self.search_for_tales()
        
        if not stories:
            logger.warning("No stories found")
            return None
        
        # Process all stories and extract paragraphs
        all_paragraphs = []
        for story in stories:
            paragraphs = self.extract_paragraphs(story)
            all_paragraphs.extend(paragraphs)
        
        return all_paragraphs if all_paragraphs else None
