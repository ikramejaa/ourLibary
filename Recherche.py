import os
import json
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file


app = Flask(__name__)
CORS(app)

# Replace 'your_username' and 'your_password' with your Elasticsearch username and password
es = Elasticsearch(['http://elastic:595jlbEhjbEFAdfVjDOT@localhost:9200/'])

# Create the 'library' index if it doesn't exist
index_settings = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "genre": {"type": "text", "analyzer": "standard"},
            "link": {"type": "text"}
        }
    }
}


if not es.indices.exists(index='library'):
    es.indices.create(index='library', body=index_settings)

# Read data from the JSON file
with open('data.json', 'r', encoding='utf-8') as file:
    books_data = json.load(file)

# Preprocess each book before indexing
for i, book in enumerate(books_data, start=1):
    book['title'] = book['title'].lower()
    book['author'] = book['author'].lower()
    book['genre'] = [genre.lower() for genre in book['genre']]

    # Index each preprocessed book in the 'library' index
    es.index(index='library', body=book)

@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        data['title'] = data['title'].lower()
        data['author'] = data['author'].lower()
        data['genre'] = [genre.lower() for genre in data['genre']]
        
        es.index(index='library', doc_type='_doc', body=data)
        return jsonify({"message": "Book added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search function
def search(query):
    search_body = {
        "query": {
            "multi_match": {
                "query": query.lower(),
                "fields": ["title", "author", "genre"]
            }
        }
    }

    result = es.search(index='library', body=search_body)
    return result

@app.route('/search_books', methods=['POST'])
def search_books():
    try:
        query = request.json["query"].lower()
        result = search(query)

        # Filter out duplicate results based on title and author
        unique_results = []
        seen_titles_and_authors = set()

        for hit in result['hits']['hits']:
            title = hit['_source']['title']
            author = hit['_source']['author']
            identifier = f"{title}_{author}"

            if identifier not in seen_titles_and_authors:
                seen_titles_and_authors.add(identifier)
                unique_results.append(hit)

        return jsonify(unique_results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/download_book/<book_id>', methods=['GET'])
def download_book(book_id):
    try:
        # Get the document by ID from Elasticsearch
        document = es.get(index='library', id=book_id)
        if document is not None and '_source' in document:
            book_data = document['_source']
            pdf_path = book_data.get('link', '')

            if os.path.exists(pdf_path):
                return send_file(pdf_path, as_attachment=True)
            else:
                return jsonify({"error": "PDF file not found"}), 404
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)
