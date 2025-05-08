# Text Summarizer Web Application

This is a web-based text summarization tool that can summarize both plain text and web content. It uses the BART model from Facebook for summarization and provides additional context through web searches or content extraction from URLs.

## Features

- Summarize plain text input with concise, brief summaries
- Summarize content from a URL
- Enrich text with context from web searches
- Clean, responsive web interface

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the web application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Enter text or a URL in the input field and click "Summarize"

4. Wait for the summary to be generated (this may take a moment, especially for longer texts or when processing URLs)

5. View the generated summary

## How It Works

1. When you enter text, the application checks if it's a URL:
   - If it's a URL, it extracts the content from the webpage
   - If it's plain text, it searches for related information to provide context

2. The text (with added context) is then processed by the BART summarization model

3. The summary is displayed on the web page

## Command Line Version

You can also use the command line version of the tool:

```
python main.py
```

This will prompt you to enter text to summarize and will display the summary in the terminal.

## Dependencies

- Flask: Web framework
- Transformers: For the BART summarization model
- Newspaper3k: For extracting content from URLs
- BeautifulSoup4: For parsing HTML
- Requests: For making HTTP requests

## License

[Include license information here]
