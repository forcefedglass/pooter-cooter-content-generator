# Pooter Cooter Content Generator

An automated content generation system that creates engaging social media content by transforming band-related stories into unique posts and video compilations.

## Features

- Web scraping for source content
- Gender inversion and text embellishment
- Automated image generation with "Did You Know..." format
- Daily video compilation for TikTok and Instagram Reels
- Scheduled posting (3 times per day)
- Automated cleanup of temporary files

## Project Structure

```
pooter-cooter-bot/
├── src/
│   ├── agents/
│   │   ├── web_agent.py         # Web scraping and content gathering
│   │   ├── text_transformer.py  # Text processing and transformation
│   │   ├── image_generator.py   # Image generation and post creation
│   │   └── video_compiler.py    # Daily video compilation
│   └── utilities/
│       └── logger.py            # Centralized logging system
├── config.py                    # Configuration settings
├── main.py                      # Main application entry point
└── requirements.txt            # Project dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with the following:
```
IMAGE_GEN_API_KEY=your_image_generation_api_key
INSTAGRAM_API_KEY=your_instagram_api_key
```

3. Run the application:
```bash
python main.py
```

## Configuration

The application can be configured through `config.py`:

- Post scheduling times
- Image generation settings
- File paths for temporary storage
- Cleanup settings

## Logging

Logs are stored in the `logs` directory with the following features:
- Daily log rotation
- Colored console output
- Detailed error tracking
- Automatic cleanup of old logs

## Components

### Web Agent
- Searches and scrapes content about the band
- Cleans and processes raw text
- Handles content filtering

### Text Transformer
- Inverts gender references in text
- Embellishes stories with dramatic flair
- Summarizes content for social media
- Selects the most engaging paragraphs

### Image Generator
- Creates images based on processed text
- Formats posts with "Did You Know..." template
- Handles image storage and cleanup

### Video Compiler
- Compiles daily posts into video format
- Adds transitions and effects
- Manages temporary file cleanup

## Error Handling

The application includes comprehensive error handling:
- Graceful degradation when services fail
- Detailed error logging
- Automatic retry mechanisms
- Fallback content generation

## Maintenance

- Temporary files are automatically cleaned up after 7 days
- Log files are rotated daily
- Failed posts are logged for manual review

## Requirements

- Python 3.8+
- FFmpeg for video compilation
- Internet connection for web scraping and API access
- Sufficient storage for temporary files

## License

This project is licensed under the MIT License - see the LICENSE file for details.
