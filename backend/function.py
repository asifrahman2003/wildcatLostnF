import json
import logging
import nltk
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define lost-and-found spots with areas
spots = {
    "Student Union Info Desk": {
        "tags": ["bags", "phones", "keys", "electronics", "backpack"],
        "link": "https://studentunion.arizona.edu",
        "area": "Central Campus"
    },
    "UAPD Lost & Found": {
        "tags": ["wallets", "tech", "catcard", "id", "valuable", "phone", "laptop"],
        "link": "https://uapd.arizona.edu/lost-and-found",
        "area": "Central Campus"
    },
    "Main Library Ask Us": {
        "tags": ["books", "notebooks", "laptop", "study", "materials"],
        "link": "https://library.arizona.edu",
        "area": "Library Area"
    },
    "Likins Hall Desk": {
        "tags": ["clothes", "personal", "keys", "dorm", "residential"],
        "link": "https://housing.arizona.edu",
        "area": "South Campus"
    },
    "Parking Office": {
        "tags": ["bikes", "gear", "helmet", "skateboard", "transportation"],
        "link": "https://parking.arizona.edu",
        "area": "East Campus"
    }
}

def extract_item(text):
    """Extract lost item from natural language input using NLTK."""
    try:
        # Tokenize the input text
        tokens = word_tokenize(text.lower())
        
        # Look for patterns like "lost my X" or "lost X"
        item = None
        for i, token in enumerate(tokens):
            if token in ["lost", "my"] and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token not in ["my", "near", "at", "in", "the"]:
                    item = next_token
                    break
        
        # If no item found, take first noun-like token
        if not item:
            stopwords = ["i", "lost", "my", "near", "at", "in", "the"]
            for token in tokens:
                if token.isalnum() and token not in stopwords:
                    item = token
                    break
        
        logger.info(f"Extracted item '{item}' from text: '{text}'")
        return item if item else "unknown"
    
    except Exception as e:
        logger.error(f"Error in extract_item: {str(e)}")
        return "unknown"

def match_spots(item, user_area):
    """Match extracted item to lost-and-found spots, prioritizing by area."""
    try:
        item = item.lower()
        matches = []
        
        # Find spots with matching tags
        for spot, data in spots.items():
            # Check if any tag is contained within the item or vice versa
            if any(tag in item or item in tag for tag in data["tags"]):
                matches.append({
                    "name": spot,
                    "link": data["link"],
                    "area": data["area"]
                })
        
        # Sort matches: prioritize spots in user's area
        sorted_matches = sorted(matches, key=lambda x: x["area"] != user_area)
        
        # If no matches, suggest UAPD as fallback
        if not sorted_matches:
            return [{
                "name": "Check UAPD Lost & Found",
                "link": "https://uapd.arizona.edu/lost-and-found",
                "area": "Central Campus",
                "note": "No exact matches found, but UAPD handles all types of lost items."
            }]
            
        return sorted_matches
        
    except Exception as e:
        logger.error(f"Error in match_spots: {str(e)}")
        return [{
            "name": "Error processing request",
            "link": "https://uapd.arizona.edu/lost-and-found",
            "area": "Central Campus"
        }]

app = Flask(__name__)
CORS(app, resources={
    r"/lost-found": {
        "origins": "*",
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/lost-found', methods=['GET', 'OPTIONS'])
def lost_found():
    """Main endpoint for lost item processing."""
    try:
        # Handle preflight request
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'ok'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
            return response

        # Get query parameters
        item_text = request.args.get('item')
        user_area = request.args.get('area')
        
        logger.info(f"Received request - Item: {item_text}, Area: {user_area}")
        
        if not item_text or not user_area:
            logger.warning("Missing required parameters")
            return jsonify({
                'error': 'Missing required parameters. Please provide both "item" and "area".'
            }), 400
            
        # Extract item using NLP
        extracted_item = extract_item(item_text)
        logger.info(f"Processing request for item: {extracted_item}, area: {user_area}")
        
        # Match to spots
        matches = match_spots(extracted_item, user_area)
        logger.info(f"Found {len(matches)} matches")
        
        # Return results with CORS headers
        response = jsonify(matches)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error occurred. Please try again later.'
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)