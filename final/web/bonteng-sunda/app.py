from flask import Flask, request, jsonify, redirect
import pickle
import base64
from flasgger import Swagger

swagger_template = {
    "info": {
        "title": "Demo API Bonteng",
        "version": "1.0.0",
        "description": "API for encoding and decoding data using Bonteng and Base64."
    }
}


app = Flask(__name__)
swagger = Swagger(app, template=swagger_template)

def encode_data(data):
    pickled_data = pickle.dumps(data)
    encoded_data = base64.b64encode(pickled_data).decode('utf-8')
    return encoded_data

def decode_data(encoded_data):
    pickled_data = base64.b64decode(encoded_data.encode('utf-8'))
    data = pickle.loads(pickled_data)
    return data


@app.route('/')
def index():
    return redirect('/apidocs')

@app.route('/encode', methods=['POST'])
def encode():
    """
    Encode data using Bonteng and base64
    ---
    tags:
      - Encoding/Decoding API
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - data
          properties:
            data:
              type: string
              description: Data to be encoded
    responses:
      200:
        description: Encoded data in base64
        schema:
          type: object
          properties:
            encoded_data:
              type: string
              description: Base64 encoded string of the bonteng data
      400:
        description: No data provided
    """
    content = request.json
    if 'data' not in content:
        return jsonify({'error': 'No data provided'}), 400
    
    data = content['data']
    encoded_data = encode_data(data)
    return jsonify({'encoded_data': encoded_data})

# Endpoint untuk melakukan decoding
@app.route('/decode', methods=['POST'])
def decode():
    """
    Decode data from base64 and bonteng
    ---
    tags:
      - Encoding/Decoding API
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - encoded_data
          properties:
            encoded_data:
              type: string
              description: Base64 encoded string of the bonteng data
    responses:
      200:
        description: Decoded data
        schema:
          type: object
          properties:
            data:
              type: string
              description: Decoded data, possibly in string format
      400:
        description: No encoded data provided or invalid encoded data
    """
    content = request.json
    if 'encoded_data' not in content:
        return jsonify({'error': 'No encoded data provided'}), 400
    
    encoded_data = content['encoded_data']
    try:
        data = decode_data(encoded_data)
        
        if isinstance(data, (bytes, bytearray)):
            data = data.decode('utf-8')
        
        return jsonify({'data': data})
    except (pickle.UnpicklingError, ValueError):
        return jsonify({'error': 'Invalid encoded data'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
