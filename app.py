import easyocr
from PIL import Image
from flask import Flask, request, Response
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the EasyOCR tool API'

@app.route('/ocr', methods=['POST'])
def perform_ocr():
    if 'image' not in request.files:
        return Response(
            'status: error\n\nNo image provided',
            status=400,
            mimetype='text/plain'
        )

    image_file = request.files['image']

    if image_file.filename == '':
        return Response(
            'status: error\n\nNo file selected',
            status=400,
            mimetype='text/plain'
        )

    try:
        # Open image with Pillow
        image = Image.open(image_file)

        # Convert Pillow image to a NumPy array
        image_np = np.array(image)

        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Perform OCR
        results = reader.readtext(image_np)

        # Extract just the text from OCR results
        extracted_text = [res[1] for res in results]

        # Format the response as plain text
        response_text = f"\n(Status): success\n\n(Extracted text):\n\n" + "\n".join(extracted_text) + "\n"

        return Response(response_text, mimetype='text/plain')

    except Exception as e:
        return Response(
            f"status: error\n\n{str(e)}",
            status=500,
            mimetype='text/plain'
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

