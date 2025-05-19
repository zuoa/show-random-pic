import os

from flask import Flask, request, send_file, jsonify
import requests
import random
from io import BytesIO
from PIL import Image

app = Flask(__name__)

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')


@app.route('/<width>/<height>/', methods=['GET'])
def get_resized_image(width: int, height: int):
    orientation = 'square'
    keyword = request.args.get('k')
    width = int(width)
    height = int(height)
    if width > height:
        orientation = 'landscape'
    elif width < height:
        orientation = 'portrait'

    if not keyword:
        return jsonify({'error': 'Please provide a keyword parameter'}), 400

    headers = {
        'Authorization': PEXELS_API_KEY
    }

    params = {
        'query': keyword,
        'per_page': 15,
        'orientation': orientation,
        'page': 1
    }

    response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch image from Pexels'}), 500

    data = response.json()
    photos = data.get('photos', [])
    if not photos:
        return jsonify({'error': 'No images found'}), 404

    photo = random.choice(photos)
    image_url = photo['src']['original']

    # 下载原始图片
    img_response = requests.get(image_url)
    if img_response.status_code != 200:
        return jsonify({'error': 'Failed to download image'}), 500

    # 处理图像缩放
    image = Image.open(BytesIO(img_response.content))
    if width and height:
        image = image.resize((width, height), Image.LANCZOS)

    img_io = BytesIO()
    image.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')
