"""
Image Sharpening Tool
Sharpens pixelated ship sprites using advanced filtering
"""
from PIL import Image, ImageFilter, ImageEnhance
import os


def sharpen_image(input_path, output_path=None, sharpness_factor=2.0):
    """
    Sharpen a pixelated image
    
    Args:
        input_path: Path to input image
        output_path: Path to save sharpened image (if None, overwrites original)
        sharpness_factor: How much to sharpen (1.0 = no change, 2.0 = moderate, 3.0 = strong)
    """
    print(f"Loading image: {input_path}")
    
    # Load image
    img = Image.open(input_path)
    original_size = img.size
    print(f"Original size: {original_size[0]}x{original_size[1]}")
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Apply sharpening filter
    print(f"Applying sharpness factor: {sharpness_factor}")
    
    # Method 1: Unsharp mask (best for reducing pixelation)
    img_sharpened = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Method 2: Additional enhancement
    enhancer = ImageEnhance.Sharpness(img_sharpened)
    img_sharpened = enhancer.enhance(sharpness_factor)
    
    # Method 3: Edge enhancement
    img_sharpened = img_sharpened.filter(ImageFilter.EDGE_ENHANCE)
    
    # Save
    if output_path is None:
        # Backup original
        backup_path = input_path.replace('.png', '_original.png')
        if not os.path.exists(backup_path):
            print(f"Creating backup: {backup_path}")
            img.save(backup_path)
        output_path = input_path
    
    print(f"Saving sharpened image: {output_path}")
    img_sharpened.save(output_path, 'PNG')
    print("✓ Done!")


def sharpen_gentle(input_path, output_path=None):
    """
    Gentle sharpening that preserves quality and doesn't introduce artifacts
    
    Args:
        input_path: Path to input image
        output_path: Path to save result
    """
    print(f"Loading image: {input_path}")
    
    img = Image.open(input_path)
    original_size = img.size
    print(f"Size: {original_size[0]}x{original_size[1]}")
    
    # Convert to RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Apply GENTLE sharpening - just one pass with low settings
    print("Applying gentle sharpening...")
    img_sharp = img.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=1))
    
    # Very light sharpness enhancement
    enhancer = ImageEnhance.Sharpness(img_sharp)
    img_sharp = enhancer.enhance(1.5)
    
    # Save
    if output_path is None:
        output_path = input_path
    
    print(f"Saving result: {output_path}")
    img_sharp.save(output_path, 'PNG', optimize=True)
    print("✓ Done!")


def main():
    """Sharpen the Odyssey sprite"""
    odyssey_path = "assets/Ships/Federation/OdysseyClass.png"
    
    print("=" * 80)
    print("SHIP SPRITE SHARPENING TOOL")
    print("=" * 80)
    print()
    
    if not os.path.exists(odyssey_path):
        print(f"Error: File not found: {odyssey_path}")
        return
    
    print("Restoring original and applying gentle sharpening...")
    print()
    
    # First restore original if it exists
    original_backup = "assets/Ships/Federation/OdysseyClass_original.png"
    if os.path.exists(original_backup):
        print("Restoring from backup...")
        import shutil
        shutil.copy(original_backup, odyssey_path)
    
    # Apply gentle sharpening
    sharpen_gentle(odyssey_path)
    
    print()
    print("=" * 80)
    print("Original image backed up to: OdysseyClass_original.png")
    print("If you don't like the result, you can restore the original.")
    print("=" * 80)


if __name__ == "__main__":
    main()
