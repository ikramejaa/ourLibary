import os
import json
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from flask import send_from_directory
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score




app = Flask(__name__, static_url_path='/images', static_folder='images')

CORS(app)

# Replace 'your_username' and 'your_password' with your Elasticsearch username and password
es = Elasticsearch(['http://elastic:595jlbEhjbEFAdfVjDOT@localhost:9200/'])

# Create the 'library' index if it doesn't exist
index_settings = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "genre": {"type": "keyword"},
            "link": {"type": "text"},
            "image": {"type": "text"}
        }
    }
}

index_name = 'library'

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

es.indices.create(index=index_name, body=index_settings)
es.indices.refresh(index=index_name)




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

# Wait for index refresh (optional)
es.indices.refresh(index='library')



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
                "fields": ["title", "author", "genre", "link", "image"]  
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
            book_data = hit['_source']
            print(book_data)  # Check if "image" is present


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
    

@app.route('/getAllBooks', methods=['GET'])
def get_all_books():
    try:
        # Perform a search to retrieve all documents from the 'library' index
        result = es.search(index='library', body={"query": {"match_all": {}}})

        # Extract the hits from the search result
        hits = result.get('hits', {}).get('hits', [])

        # Extract book data from each hit
        books = [hit['_source'] for hit in hits]

        return jsonify({"books": books}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Add this route to serve images
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


# Function to calculate metrics based on the test examples
def calculate_metrics(results, target_genre=None, target_author=None, target_title=None):
    # Construct the lists of expected and actual results
    expected_results = [1 if is_relevant(hit, target_genre, target_author, target_title) else 0 for hit in results]
    actual_results = [1 if hit_is_retrieved(hit) else 0 for hit in results]

    # Calculate the confusion matrix
    cm = confusion_matrix(expected_results, actual_results)

    # Calculate precision, recall, and F1-score
    precision_value = precision_score(expected_results, actual_results)
    recall_value = recall_score(expected_results, actual_results)
    f1 = f1_score(expected_results, actual_results)

    return cm, precision_value, recall_value, f1

# ... (remaining functions remain unchanged)

@app.route('/evaluate_search', methods=['POST'])
def evaluate_search():
    try:
        # Assuming you receive the search results in the request
        search_results = request.json["search_results"]

        # Assuming you have a ground truth (actual relevant books)
        ground_truth = [
            {"query": "romance", "relevant_books": ["Fifty shades of grey", "Bridgerton romancing mister", "Bridgerton the viscount and I", "Bridgerton duke and I", "Seducing Mr Right", "The Kama Sutra", "REDITES-LE-MOI", "Anne of Green Gables", "Pride and Prejudice"]},
            {"query": "bridgerton", "relevant_books": ["Bridgerton duke and I", "Bridgerton the viscount and I", "Romancing Mr Right"]},
            {"query": "markus", "relevant_books": ["The book thief", "A good girl's guide to murder", "As good as dead", "Me trouver", "Kofi"]}
        ]

        metrics_results = []

        for query_data in ground_truth:
            query = query_data["query"]
            relevant_books = query_data["relevant_books"]

            # Filter search results for the current query
            query_results = [result for result in search_results if result['_source']['title'] in relevant_books]

            # Construct the lists of expected and actual results
            expected_results = [1 if result['_source']['title'] in relevant_books else 0 for result in query_results]
            actual_results = [1 if hit_is_retrieved(result) else 0 for result in query_results]

            # Calculate metrics
            cm = confusion_matrix(expected_results, actual_results)
            precision_value = precision_score(expected_results, actual_results)
            recall_value = recall_score(expected_results, actual_results)
            f1 = f1_score(expected_results, actual_results)

            metrics_results.append({
                "query": query,
                "confusion_matrix": cm.tolist(),
                "precision": precision_value,
                "recall": recall_value,
                "f1_score": f1
            })

        return jsonify({"metrics_results": metrics_results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

  
# Define a function to check if a hit is relevant based on genre, author, or title
def is_relevant(hit, target_genre=None, target_author=None, target_title=None):
    # Modify this function based on your relevance criteria
    return (
        (target_genre is None or target_genre.lower() in hit['genre']) and
        (target_author is None or target_author.lower() == hit['author'].lower()) and
        (target_title is None or target_title.lower() in hit['title'].lower())
    )

# Define a function to check if a hit is retrieved
def hit_is_retrieved(hit):
    # Modify this function based on your retrieval criteria
    return True  # Adjust the retrieval logic based on your needs

    
if __name__ == '__main__':
    app.run(debug=True)


