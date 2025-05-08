# Info Aggregator Web Application

This is a web-based text summarization and question-answering tool that can process both plain text and web content. It uses the BART model from Facebook for summarization and provides additional context through web searches or content extraction from URLs.

## Features

- Obtain info and summarize plain text input with concise, brief summaries
- Summarize content from a URL
- Enrich text with context from web searches
- Clean, responsive web interface
- 100% private and secure - all processing happens locally on your machine

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

3. Enter text or a URL in the input field and click "Ask" and 
   wait for the processing to complete (this may take a moment, especially for longer texts or when processing URLs)

   <img src="images/asking%20a%20question.png" alt="Asking a Question" width="500">


4. View the generated answer

   <img src="images/response%20to%20question.png" alt="Response to Question" width="500">

## How It Works

1. When you enter text, the application checks if it's a URL:
   - If it's a URL, it extracts the content from the webpage using the Newspaper3k library
   - If it's plain text, it searches for related information using DuckDuckGo to provide context

   <img src="images/url%20based%20query.png" alt="URL Based Query" width="500">

2. The application processes the input:
   - Checks URL safety using pattern matching
   - Filters out potentially harmful or irrelevant domains
   - Extracts and cleans text content from web pages
   - Combines information from multiple sources for context

3. The text (with added context) is then processed by the BART summarization model:
   - For longer texts, the content is split into manageable chunks
   - Each chunk is summarized separately
   - The summaries are combined into a coherent response

4. The summary is displayed on the web page

   <img src="images/answer%20to%20url%20based%20query.png" alt="Answer to URL Based Query" width="500">

## Privacy and Security

This application prioritizes your privacy and security:

- **100% Local Processing**: All text processing and summarization happens on your local machine
- **No Data Storage**: Your queries and results are not stored or sent to external servers
- **URL Safety Checking**: The application checks URLs against known suspicious patterns
- **Domain Filtering**: A comprehensive list of potentially harmful or irrelevant domains is blocked
- **No Tracking**: The application doesn't use cookies or tracking mechanisms

<img src="images/bart%20model%20page.png" alt="BART Model" width="700">

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
