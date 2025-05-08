from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import textwrap
from webtools import create_context
app = Flask(__name__)

# Initialize the summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_long_text(text, max_chunk_size=1000):
    chunks = textwrap.wrap(text, max_chunk_size)
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=70, min_length=15, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return " ".join(summaries)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text']
    context = create_context(text)
    print(context)
    text_with_context = text + context
    summary = summarize_long_text(text_with_context)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
