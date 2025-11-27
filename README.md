# NutriCheck

## Overview
NutriCheck is a machine learning application that analyzes food images and provides nutritional information. It uses a CNN (Convolutional Neural Network) to classify food items and retrieves nutritional data from a Supabase database. The application supports both pre-trained models and custom models trained via transfer learning.

## Tools Used
- **Language**: Python 3.10+
- **Machine Learning**: 
  - TensorFlow 2.x
  - Keras
  - **Transfer Learning**: MobileNetV2 (pre-trained on ImageNet)
- **Database**: Supabase (PostgreSQL)
- **Data Processing**: NumPy, Pillow
- **Environment**: python-dotenv
- **Data Augmentation**: ImageDataGenerator (for training)

## Structure
```
NutriCheck/
├── classifier.py           # CNN-based food classifier (supports custom models)
├── database.py             # Supabase client and query functions
├── seed_db.py              # Database seeding script
├── main.py                 # Main application CLI
├── schema.sql              # Supabase table schema
├── .env                    # Environment variables (Supabase credentials)
├── requirements.txt        # Python dependencies
└── training/               # Transfer learning training scripts
    ├── prepare_data.py     # Data organization script
    ├── train.py            # Transfer learning training script
    ├── README.md           # Training documentation
    ├── data/               # Training data (train/validation splits)
    └── models/             # Saved custom models
```

## Setup

### Prerequisites
- Python 3.10+
- Supabase account (free tier works)

### Installation

1. Clone the repository and navigate to the project directory.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Supabase:
   - Create a new project at [supabase.com](https://supabase.com)
   - In the SQL Editor, run the contents of `schema.sql` to create the `foods` table
   - Get your project URL and anon key from Settings > API

4. Configure environment variables:
   - Edit the `.env` file and add your Supabase credentials:
     ```
     SUPABASE_URL=your_supabase_url_here
     SUPABASE_KEY=your_supabase_anon_key_here
     ```

5. Seed the database with food data:
   ```bash
   python seed_db.py
   ```

## Usage

### Using Pre-trained Model (Default)

To analyze a food image with the default MobileNetV2 model:
```bash
python main.py path/to/your/food_image.jpg
```

Example:
```bash
python main.py pizza.jpg
```

### Using Custom Trained Model

If you've trained a custom model (see Transfer Learning section below):
```bash
python main.py path/to/image.jpg --custom-model training/models/nutricheck_custom.h5
```

The application will:
1. Classify the food in the image using the CNN
2. Display the top 3 predictions with confidence scores
3. Query the database for nutritional information
4. Display calories, protein, carbs, and fat content

## Transfer Learning

NutriCheck supports training custom models using transfer learning with MobileNetV2 as the base.

### Why Transfer Learning?

- **Faster Training**: Leverage pre-trained ImageNet weights
- **Better Accuracy**: Especially with limited training data
- **Custom Classes**: Train on your specific food categories
- **Efficient**: Freeze base layers, only train classification head

### Training Your Own Model

1. **Prepare Your Data**:
   ```bash
   python training/prepare_data.py
   ```
   Then organize images into `training/data/train/` and `training/data/validation/` folders by class.

2. **Train the Model**:
   ```bash
   python training/train.py
   ```
   This will:
   - Load MobileNetV2 with frozen base layers
   - Add custom classification layers
   - Train with data augmentation
   - Save the best model to `training/models/nutricheck_custom.h5`

3. **Use Your Custom Model**:
   ```bash
   python main.py image.jpg --custom-model training/models/nutricheck_custom.h5
   ```

### Transfer Learning Architecture

- **Base Model**: MobileNetV2 (ImageNet weights, frozen)
- **Custom Layers**:
  - GlobalAveragePooling2D
  - Dense(512, relu) + Dropout(0.5)
  - Dense(256, relu) + Dropout(0.3)
  - Dense(num_classes, softmax)
- **Optimizer**: Adam (lr=0.0001)
- **Data Augmentation**: Rotation, shifts, zoom, horizontal flip
- **Callbacks**: ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

For more details, see [training/README.md](training/README.md).

## How It Works

### Pre-trained Model Mode
1. **Image Classification**: Uses MobileNetV2 pre-trained on ImageNet (1000+ classes including many foods)
2. **Preprocessing**: Image resized to 224x224 and normalized
3. **Prediction**: Top-K predictions with confidence scores
4. **Database Lookup**: Predicted food name queries Supabase
5. **Results**: Nutritional data displayed if found

### Custom Model Mode (Transfer Learning)
1. **Image Classification**: Uses your custom trained model
2. **Preprocessing**: Same as pre-trained (224x224, normalized)
3. **Prediction**: Predictions based on your custom classes
4. **Database Lookup**: Same as above
5. **Results**: Nutritional data for your custom food categories

## Adding New Foods

To add more foods to the database, edit `seed_db.py` and add entries to the `foods_data` list, then run:
```bash
python seed_db.py
```

## Contact
For collaborations or questions, please reach out to rohansiva123@gmail.com.
