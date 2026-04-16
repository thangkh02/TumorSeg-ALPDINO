"""
Configuration file for SSL upload and training setup
"""

# Model configuration
MODEL_CONFIG = {
    "encoder": "dinov2",
    "decoder": "alpnet",
    "input_channels": 4,
    "output_channels": 4,
}

# Data configuration
DATA_CONFIG = {
    "dataset": "BraTS2023",
    "data_path": "./data",
    "batch_size": 24,
    "num_workers": 4,
}

# Training configuration
TRAINING_CONFIG = {
    "epochs": 50,
    "learning_rate": 1e-4,
    "optimizer": "AdamW",
    "loss_fn": "CrossEntropyDiceLoss",
}

# SSL configuration
SSL_CONFIG = {
    "use_ssl": True,
    "ssl_model": "DINOv2",
    "pretrained": True,
}
