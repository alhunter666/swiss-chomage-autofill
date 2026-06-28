import os
import argparse
import sys
from PIL import Image

def images_to_pdf(input_dir, output_pdf_path):
    print(f"Scanning directory: {input_dir}")
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    
    image_paths = []
    files = sorted(os.listdir(input_dir))
    for file in files:
        if file.lower().endswith(valid_extensions):
            image_paths.append(os.path.join(input_dir, file))
            
    if not image_paths:
        print("Error: No images found to pack into PDF.")
        sys.exit(1)
        
    print(f"Found {len(image_paths)} images: {[os.path.basename(p) for p in image_paths]}")
    
    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            # PDF requires RGB or L (grayscale) format.
            # Convert RGBA / palette images to RGB to prevent PDF saving errors.
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
        except Exception as e:
            print(f"Error opening image {os.path.basename(path)}: {e}")
            
    if not images:
        print("Error: Failed to load any valid images.")
        sys.exit(1)
        
    print(f"Saving combined PDF to: {output_pdf_path}")
    # Save the images sequentially into a single PDF
    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
    print("PDF packing completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan folder and pack images sequentially into a single PDF.")
    parser.add_argument("--dir", default=".", help="Directory to scan for images")
    parser.add_argument("--output", default="images_combined.pdf", help="Output PDF filename")
    args = parser.parse_args()
    
    input_dir_abs = os.path.abspath(args.dir)
    output_pdf_abs = os.path.abspath(args.output)
    
    images_to_pdf(input_dir_abs, output_pdf_abs)
