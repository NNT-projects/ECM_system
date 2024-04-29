import pickle


# import sys
# sys.path.append('src')

from data_preprocessing import preprocess_raw_data

if __name__ == "__main__":
    X_test_path = 'data/X_test.csv'
    # model_save_path = 'model/lgb_model.txt'

    X_processed = preprocess_raw_data(X_test_path, 'VQ-BGU')

    with open('models/lgb_model.txt', 'rb') as f:
        trained_model = pickle.load(f)

    predictions = trained_model.predict(X_processed)

    print("Predictions:", predictions)
