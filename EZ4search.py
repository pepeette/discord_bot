import os
import csv
import docx
from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.qparser import QueryParser

def construct_index(directory_path):
    schema = Schema(
        path=ID(stored=True),
        content=TEXT(analyzer=None, stored=True),
        tags=KEYWORD(lowercase=True, commas=True, scorable=True, stored=True)
    )

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = index.create_in("indexdir", schema)

    writer = ix.writer()

    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith(".txt"):
                with open(file_path) as f:
                    content = f.read()
                    writer.add_document(path=file_path, content=content)
            elif file_path.endswith(".csv"):
                with open(file_path, newline='') as f:
                    reader = csv.reader(f)
                    content = '\n'.join([','.join(row) for row in reader])
                    writer.add_document(path=file_path, content=content)
            elif file_path.endswith(".docx"):
                doc = docx.Document(file_path)
                content = '\n'.join([para.text for para in doc.paragraphs])
                writer.add_document(path=file_path, content=content)

    writer.commit()

def search_index(query):
    ix = index.open_dir("indexdir")
    parser = QueryParser("content", schema=ix.schema)
    q = parser.parse(query)

    with ix.searcher() as searcher:
        results = searcher.search(q, limit=None)

    return [r['path'] for r in results]

def chatbot(input_text):
    results = search_index(input_text)
    return "Found documents:\n" + '\n'.join(results)

construct_index("docs")

# Run the chatbot with Gradio
import gradio as gr

iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")
iface.launch(share=True)
