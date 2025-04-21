import os
import time
from openslide import OpenSlide
from openslide.deepzoom import DeepZoomGenerator
import PIL.Image
from PIL import ImageFile
import xml.etree.ElementTree as ET

ImageFile.LOAD_TRUNCATED_IMAGES = True
PIL.Image.MAX_IMAGE_PIXELS = None

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

def generate_dzi(image_path, output_dir):
    start_time = time.time()
    
    # Get image ID from filename
    image_id = os.path.splitext(os.path.basename(image_path))[0]
    dzi_dir = os.path.join(output_dir, f"{image_id}.dzi_files")
    dzi_file = os.path.join(output_dir, f"{image_id}.dzi")
    
    # Skip if already exists
    if os.path.exists(dzi_file):
        print(f"DZI already exists for {image_id}")
        return
    
    print(f"Generating DZI for {image_id}...")
    
    # Create output directory
    os.makedirs(dzi_dir, exist_ok=True)
    
    # Generate DZI
    slide = get_slide(image_path)
    if isinstance(slide, OpenSlide):
        width, height = slide.dimensions
    else:
        width, height = slide.get_dimensions()
    
    print(f"Original image dimensions: {width}x{height}")
    
    dzg = DeepZoomGenerator(slide, 
                          tile_size=1028,
                          overlap=1,
                          limit_bounds=False)  # Changed to False
    
    # Get image properties and validate pyramid structure
    levels = dzg.level_count
    print(f"\nPyramid structure:")
    for level in range(levels):
        dims = dzg.level_dimensions[level]
        tiles = dzg.level_tiles[level]
        print(f"Level {level}:")
        print(f"  Dimensions: {dims[0]}x{dims[1]}")
        print(f"  Tiles: {tiles[0]}x{tiles[1]} ({tiles[0] * tiles[1]} total)")
    
    # Generate DZI XML with fixed attributes
    dzi_xml = ET.Element("Image", {
        "xmlns": "http://schemas.microsoft.com/deepzoom/2008",
        "Format": "jpeg",
        "Overlap": "1",  # Use the value we passed to constructor
        "TileSize": "1028"  # Use the value we passed to constructor
    })
    size_elem = ET.SubElement(dzi_xml, "Size", {
        "Width": str(width),
        "Height": str(height)
    })
    
    # Save DZI file
    with open(dzi_file, 'wb') as f:
        f.write(ET.tostring(dzi_xml, encoding='utf-8', xml_declaration=True))
    
    # Generate and save tiles for each level
    total_tiles = sum(cols * rows for cols, rows in dzg.level_tiles)
    tiles_processed = 0
    
    for level in range(levels):
        level_dir = os.path.join(dzi_dir, str(level))
        os.makedirs(level_dir, exist_ok=True)
        
        cols, rows = dzg.level_tiles[level]
        print(f"Generating level {level} ({cols}x{rows} tiles)...")
        
        for row in range(rows):
            for col in range(cols):
                tile = dzg.get_tile(level, (col, row))
                tile_path = os.path.join(level_dir, f"{col}_{row}.jpeg")
                tile.save(tile_path, 'JPEG', quality=90)
                
                tiles_processed += 1
                if tiles_processed % 100 == 0:
                    progress = (tiles_processed / total_tiles) * 100
                    print(f"Progress: {progress:.1f}% ({tiles_processed}/{total_tiles} tiles)")
    
    end_time = time.time()
    print(f"DZI generation completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    files_dir = "files"
    for file in os.listdir(files_dir):
        if file.endswith(('.tif', '.tiff')):
            generate_dzi(os.path.join(files_dir, file), files_dir)
