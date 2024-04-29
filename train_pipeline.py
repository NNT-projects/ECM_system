import numpy as np
from sklearn.metrics import mean_squared_error

import sys
sys.path.append('src')

from data_preprocessing import preprocess_training_data
from model_training import train_model

if __name__ == "__main__":
    X_train_path = '../data/X_train.csv'
    y_train_path = '../data/y_train.csv'
    
    X_train_tmp_path = 'tmp_data/X_train.csv'
    y_train_tmp_path = 'tmp_data/y_train.csv'
    X_val_tmp_path = 'tmp_data/X_val.csv'
    y_val_tmp_path = 'tmp_data/y_val.csv'
    model_save_path = 'models/lgb_model.txt'

    X_train_processed, y_train_processed, X_val_processed, y_val_processed = preprocess_training_data(X_train_path, y_train_path, 'VQ-BGU')

    trained_model = train_model(X_train_tmp_path,X_val_tmp_path, y_train_tmp_path, y_val_tmp_path, model_save_path)

    # Evaluation
    y_pred = trained_model.predict(X_val_processed)
    rmse = np.sqrt(mean_squared_error(y_val_processed, y_pred))

    print("RMSE:", rmse)