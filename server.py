from flask import Flask, send_from_directory, jsonify
import os
import logging
from openslide import OpenSlide
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None

app = Flask(__name__, static_url_path='')
logging.basicConfig(level=logging.INFO)

DEEPZOOM_SLIDE = None
DEEPZOOM_FORMAT = 'jpeg'
DEEPZOOM_TILE_SIZE = 1028
DEEPZOOM_OVERLAP = 1
DEEPZOOM_LIMIT_BOUNDS = True

class PILBridge:
    def __init__(self, image_path):
        self.image = PIL.Image.open(image_path)
    
    def get_dimensions(self):
        return self.image.size
    
    def read_region(self, location, level, size):
        return self.image.crop((location[0], location[1], 
                              location[0] + size[0], 
                              location[1] + size[1]))

def get_slide(image_path):
    try:
        return OpenSlide(image_path)
    except:
        return PILBridge(image_path)

@app.route('/')
def serve_viewer():
    return send_from_directory('.', 'viewer.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/files/<path:filename>')
def serve_image(filename):
    return send_from_directory('files', filename)

@app.route('/dzi/<image_id>.dzi')
def get_dzi(image_id):
    dzi_path = os.path.join('files', f'{image_id}.dzi')
    if os.path.exists(dzi_path):
        return send_from_directory('files', f'{image_id}.dzi')
    return jsonify({'error': 'DZI file not found'}), 404

@app.route('/dzi/<image_id>_files/<int:level>/<int:col>_<int:row>.<format>')
def get_tile(image_id, level, col, row, format):
    tile_path = os.path.join('files', f'{image_id}.dzi_files', str(level), f'{col}_{row}.{format}')
    if os.path.exists(tile_path):
        return send_from_directory(os.path.join('files', f'{image_id}.dzi_files', str(level)), f'{col}_{row}.{format}')
    return jsonify({'error': 'Tile not found'}), 404

@app.route('/available-images')
def get_available_images():
    images = []
    for file in os.listdir('files'):
        if file.endswith('.dzi'):
            images.append(file.replace('.dzi', ''))
    return jsonify(images)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
