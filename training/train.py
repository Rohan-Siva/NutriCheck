#transfer learning pipeline
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os
from pathlib import Path
import json

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.0001
TRAIN_DIR = 'training/data/train'
VAL_DIR = 'training/data/validation'
MODEL_SAVE_PATH = 'training/models/nutricheck_custom.h5'
CLASS_INDICES_PATH = 'training/models/class_indices.json'

def create_model(num_classes):
    
    # load MobileNetV2 without top layers, freeze base layers for tuning
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    base_model.trainable = False
    
    # custom classification layers
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    # final model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_data_generators():
    
    # training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # validation data (no augmentation, only rescaling)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    return train_generator, val_generator

def train():
    
    print("=" * 60)
    print("NutriCheck - Transfer Learning Training")
    print("=" * 60)
    
    if not os.path.exists(TRAIN_DIR) or not os.path.exists(VAL_DIR):
        print(f"   Please run prepare_data.py first and organize your images.")
        return
    
    print("\n Loading data...")
    train_generator, val_generator = create_data_generators()
    
    num_classes = len(train_generator.class_indices)
    print(f"Found {num_classes} classes")
    print(f"   Training samples: {train_generator.samples}")
    print(f"   Validation samples: {val_generator.samples}")
    
    Path('training/models').mkdir(parents=True, exist_ok=True)
    with open(CLASS_INDICES_PATH, 'w') as f:
        class_names = {v: k for k, v in train_generator.class_indices.items()}
        json.dump(class_names, f, indent=2)
    print(f"Saved class indices to {CLASS_INDICES_PATH}")
    
    print("\nBuilding model...")
    model = create_model(num_classes)
    print(f"Model created with {num_classes} output classes")
    
    print("\nModel Summary:")
    model.summary()
    
    callbacks = [
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    print(f"\nStarting training for {EPOCHS} epochs...")
    print("=" * 60)
    
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    print(f"\nTraining complete!")
    print(f"   Best model saved to: {MODEL_SAVE_PATH}")
    print(f"   Class indices saved to: {CLASS_INDICES_PATH}")
    
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    print(f"\nFinal Metrics:")
    print(f"   Training Accuracy: {final_train_acc:.4f}")
    print(f"   Validation Accuracy: {final_val_acc:.4f}")

if __name__ == "__main__":
    train()
