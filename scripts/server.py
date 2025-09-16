'''
=====================================================================================
Main server.py file
=====================================================================================
This file contains the reference to the util.py file 
This file contains the reference to the front-end HTML, CSS, JS 
Checks if the RESTFUL API are working fine or not 
-------------------------------------------------------------------------------------
'''

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import util

app = Flask(__name__, template_folder='UI', static_folder='UI', static_url_path='')
CORS(app) 

# HTML from UI/index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/classify_endpoint', methods=['POST'])
def classify_endpoint():
    # Main classification end point 
    try:
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")

        if request.is_json:
            data = request.get_json()
            print("Receieved JSON data")
        else:
            # Handle form data
            data = request.form.to_dict()
            print("Received form data")

        print(f"Data keys: {list(data.keys()) if data else 'No data'}")

        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        image_b64 = data['image']

        if not image_b64:
            return jsonify({'error': 'Empty image data'}), 400
        
        print("Received image for classification")
        print(f"Image data length: {len(image_b64)} characters")

        # Call classification function
        result = util.classify_image(image_b64)
        print(f"Classified Result: {result}")
        return jsonify(result)
    
    except Exception as e:
        print(f"Error during classification: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def initialize_app():
    """Initialize the application"""
    try:
        print("Initializing Celebrity Classifier App...")
        util.load_saved_artifacts()
        print("* Model and artifacts loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize app: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Celebrity Classifier Server...")
    
    # Initialize the app
    if initialize_app():
        print("** Server ready!")
        print("** Open your browser and go to: http://localhost:5000")
        print("** Press Ctrl+C to stop the server")
        
        # Run Flask app
        app.run(
            host='0.0.0.0',  # Allow connections from any IP
            port=5000,
            debug=True,      # Enable debug mode for development
            threaded=True    # Handle multiple requests simultaneously
        )
    else:
        print("❌ Failed to start server. Please check your model files.")
