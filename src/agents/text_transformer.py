import logging
from typing import List, Dict, Optional
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import random

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except Exception as e:
    logging.error(f"Error downloading NLTK data: {str(e)}")

class TextTransformer:
    def __init__(self):
        # Gender word mappings
        self.gender_mappings = {
            'he': 'she',
            'him': 'her',
            'his': 'her',
            'himself': 'herself',
            'man': 'woman',
            'men': 'women',
            'boy': 'girl',
            'boys': 'girls',
            'male': 'female',
            'father': 'mother',
            'brother': 'sister',
            'son': 'daughter',
            'uncle': 'aunt',
            'gentleman': 'lady',
            'gentlemen': 'ladies',
            'sir': 'madam',
            'mr': 'ms',
            'king': 'queen',
            # Add reverse mappings
            'she': 'he',
            'her': 'him',
            'herself': 'himself',
            'woman': 'man',
            'women': 'men',
            'girl': 'boy',
            'girls': 'boys',
            'female': 'male',
            'mother': 'father',
            'sister': 'brother',
            'daughter': 'son',
            'aunt': 'uncle',
            'lady': 'gentleman',
            'ladies': 'gentlemen',
            'madam': 'sir',
            'ms': 'mr',
            'queen': 'king'
        }

        # Embellishment additions
        self.intensifiers = [
            'incredibly', 'absolutely', 'outrageously', 'shockingly',
            'unbelievably', 'astoundingly', 'mind-blowingly'
        ]
        
        self.dramatic_adjectives = [
            'wild', 'insane', 'legendary', 'notorious', 'scandalous',
            'controversial', 'unprecedented', 'jaw-dropping'
        ]

    def invert_gender(self, text: str) -> str:
        """Invert gender-specific words in the text"""
        try:
            words = word_tokenize(text)
            new_words = []
            
            for word in words:
                word_lower = word.lower()
                if word_lower in self.gender_mappings:
                    # Preserve original capitalization
                    if word.isupper():
                        new_words.append(self.gender_mappings[word_lower].upper())
                    elif word.istitle():
                        new_words.append(self.gender_mappings[word_lower].title())
                    else:
                        new_words.append(self.gender_mappings[word_lower])
                else:
                    new_words.append(word)
            
            return ' '.join(new_words)
        
        except Exception as e:
            logging.error(f"Error in gender inversion: {str(e)}")
            return text

    def embellish_text(self, text: str) -> str:
        """Add dramatic flair to the text"""
        try:
            sentences = sent_tokenize(text)
            embellished_sentences = []
            
            for sentence in sentences:
                # Randomly decide whether to embellish this sentence
                if random.random() < 0.7:  # 70% chance of embellishment
                    words = word_tokenize(sentence)
                    
                    # Add intensifier at random position
                    if random.random() < 0.5:
                        insert_pos = random.randint(0, len(words))
                        words.insert(insert_pos, random.choice(self.intensifiers))
                    
                    # Add dramatic adjective at random position
                    if random.random() < 0.5:
                        insert_pos = random.randint(0, len(words))
                        words.insert(insert_pos, random.choice(self.dramatic_adjectives))
                    
                    embellished_sentences.append(' '.join(words))
                else:
                    embellished_sentences.append(sentence)
            
            return ' '.join(embellished_sentences)
        
        except Exception as e:
            logging.error(f"Error in text embellishment: {str(e)}")
            return text

    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """
        Summarize text to specified number of sentences
        Uses a simple frequency-based approach
        """
        try:
            # Split into sentences
            sentences = sent_tokenize(text)
            
            if len(sentences) <= num_sentences:
                return text
            
            # Calculate word frequencies
            words = word_tokenize(text.lower())
            word_freq = {}
            for word in words:
                if word.isalnum():
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Score sentences based on word frequencies
            sentence_scores = {}
            for sentence in sentences:
                score = 0
                for word in word_tokenize(sentence.lower()):
                    if word.isalnum():
                        score += word_freq.get(word, 0)
                sentence_scores[sentence] = score
            
            # Get top sentences while maintaining order
            sorted_sentences = sorted(sentence_scores.items(), 
                                   key=lambda x: x[1], 
                                   reverse=True)[:num_sentences]
            
            # Sort sentences by their original order
            summary_sentences = [s[0] for s in sorted_sentences]
            summary_sentences.sort(key=sentences.index)
            
            return ' '.join(summary_sentences)
        
        except Exception as e:
            logging.error(f"Error in summarization: {str(e)}")
            return text[:500] + '...'  # Fallback to simple truncation

    def select_spicy_paragraph(self, paragraphs: List[str]) -> Optional[str]:
        """
        Select the spiciest paragraph based on presence of dramatic words
        and overall length
        """
        try:
            if not paragraphs:
                return None
            
            # Words that might indicate an interesting story
            spicy_indicators = set([
                'controversy', 'scandal', 'shocking', 'outrage', 'wild',
                'crazy', 'infamous', 'notorious', 'bizarre', 'unexpected',
                'dramatic', 'unbelievable', 'incredible', 'intense'
            ])
            
            # Score paragraphs
            paragraph_scores = []
            for para in paragraphs:
                score = 0
                words = word_tokenize(para.lower())
                
                # Score based on spicy words
                score += sum(2 for word in words if word in spicy_indicators)
                
                # Score based on optimal length (prefer paragraphs between 100-300 chars)
                length = len(para)
                if 100 <= length <= 300:
                    score += 3
                elif length < 50 or length > 500:
                    score -= 2
                
                paragraph_scores.append((para, score))
            
            # Return paragraph with highest score
            return max(paragraph_scores, key=lambda x: x[1])[0]
        
        except Exception as e:
            logging.error(f"Error in paragraph selection: {str(e)}")
            return paragraphs[0] if paragraphs else None

    def process_tale(self, text: str) -> Optional[str]:
        """
        Process a single tale through all transformation steps
        """
        try:
            # First invert gender
            gender_inverted = self.invert_gender(text)
            
            # Then embellish
            embellished = self.embellish_text(gender_inverted)
            
            # Summarize
            summarized = self.summarize(embellished)
            
            # Split into paragraphs and select the spiciest one
            paragraphs = summarized.split('\n\n')
            selected = self.select_spicy_paragraph(paragraphs)
            
            return selected
        
        except Exception as e:
            logging.error(f"Error in tale processing: {str(e)}")
            return None
