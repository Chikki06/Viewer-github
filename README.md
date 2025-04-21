# Slide Image Viewer

A web-based viewer for digital microscopy slides and large format images using OpenSeadragon and Flask. The viewer supports Deep Zoom Image (DZI) format and can display very large images efficiently through tile-based streaming.

## Features

- Support for Deep Zoom Image (DZI) format
- Tile-based image streaming for efficient viewing of large images
- OpenSlide integration for reading various whole slide image formats
- Fallback to PIL for standard image formats
- Browse available images through API endpoint
- Simple web interface with zoom and pan controls

## Requirements

- Python 3.7+
- See requirements.txt for Python package dependencies

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd slide-viewer
```

2. Install Python dependencies using pip:
```bash
pip install -r requirements.txt
```

3. Create a `files` directory and place your images or DZI files in it:
```bash
mkdir files
```

## Usage

1. Place your source images in the `files` directory:
```bash
mkdir files
cp your-images/*.tif files/
```

2. Generate DZI files for your images:
```bash
python generate_dzi.py
```
This will create .dzi files and associated tile directories for each image in the `files` directory.

3. Start the Flask server:
```bash
python server.py
```

4. Open a web browser and navigate to:
```
http://localhost:8000
```

5. The viewer will display available images that have corresponding .dzi files in the `files` directory.

## API Endpoints

- `GET /` - Serves the main viewer interface
- `GET /static/<path>` - Serves static files (CSS, JavaScript, etc.)
- `GET /files/<filename>` - Serves image files directly
- `GET /dzi/<image_id>.dzi` - Serves DZI descriptor file
- `GET /dzi/<image_id>_files/<level>/<col>_<row>.<format>` - Serves image tiles
- `GET /available-images` - Returns list of available images

## Directory Structure

```
slide-viewer/
├── server.py           # Flask server implementation
├── generate_dzi.py     # Script to generate Deep Zoom Image from tif format
├── viewer.html         # Main viewer interface
│   └── ...
└── files/            # Image and DZI files
    ├── image1.dzi
    ├── image1.dzi_files/
    ├── image2.dzi
    └── image2.dzi_files/
```

## License

[MIT License](LICENSE)
