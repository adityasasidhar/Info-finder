from transformers import pipeline
import textwrap
from webtools import *

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def summarize_long_text(text, max_chunk_size=1000):
    chunks = textwrap.wrap(text, max_chunk_size)
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=70, min_length=15, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return " ".join(summaries)

text = input("Enter the text to summarize: ")
context = create_context(text)
text = text + context
summary = summarize_long_text(text)
print(summary)
