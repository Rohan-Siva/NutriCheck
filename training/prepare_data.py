# transfer learning data setup
import os
import shutil
from pathlib import Path
import random

def create_directory_structure(base_dir='training/data'):
    train_dir = Path(base_dir) / 'train'
    val_dir = Path(base_dir) / 'validation'
    
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Created directory structure at {base_dir}")
    print(f"   - Training: {train_dir}")
    print(f"   - Validation: {val_dir}")
    return train_dir, val_dir

def split_data(source_dir, train_dir, val_dir, split_ratio=0.8):
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"Source directory {source_dir} does not exist!")
        return
    
    class_dirs = [d for d in source_path.iterdir() if d.is_dir()]
    
    for class_dir in class_dirs:
        class_name = class_dir.name
        print(f"Processing class: {class_name}")
        
        (train_dir / class_name).mkdir(exist_ok=True)
        (val_dir / class_name).mkdir(exist_ok=True)
        
        images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png')) + list(class_dir.glob('*.jpeg'))
        random.shuffle(images)
        
        split_idx = int(len(images) * split_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        for img in train_images:
            shutil.copy(img, train_dir / class_name / img.name)
        
        for img in val_images:
            shutil.copy(img, val_dir / class_name / img.name)
        
        print(f"   {len(train_images)} training images, {len(val_images)} validation images")

def main():
    print("=" * 60)
    print("NutriCheck - Data Preparation for Transfer Learning")
    print("=" * 60)
    
    train_dir, val_dir = create_directory_structure()
    
    print("\n" + "=" * 60)
    print("Directory structure created!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Organize your food images into class folders")
    print("2. If you have a source directory with images, use split_data()")
    print("3. Or manually place images in train/ and validation/ folders")
    print("\nExample usage for splitting:")
    print("  split_data('path/to/source', train_dir, val_dir)")

if __name__ == "__main__":
    main()
