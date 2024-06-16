import pickle
import pandas as pd


from data_preprocessing import preprocess_raw_data

def make_predictions(X_test_path, acnum):
    try:
        X_test = pd.read_csv(X_test_path, parse_dates=['reportts'])

        X_test_filtered = X_test[X_test['acnum'] == f'VQ-{acnum}']
        if X_test_filtered.empty:
            raise ValueError(f"No data found for aircraft number VQ-{acnum}")

        X_processed = preprocess_raw_data(X_test_filtered, f'VQ-{acnum}')
        if X_processed is None:
            raise ValueError("Error in preprocessing raw data")

        with open(f'../ml/models/lgb_model_{acnum}.txt', 'rb') as f:
            trained_model = pickle.load(f)
        
        predictions = trained_model.predict(X_processed)
        
        predictions_df = pd.DataFrame(predictions, columns=['egtm'], index=X_test_filtered.index)

        # Ensure indices match for concatenation
        if not X_test_filtered.index.equals(predictions_df.index):
            raise ValueError("Indices of X_test_filtered and predictions_df do not match for concatenation")
        
        merged_dataset = pd.concat([X_test_filtered, predictions_df], axis=1)

        return merged_dataset

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


"""
if __name__ == "__main__":
    X_test_path = 'data/X_test.csv'
    fleet = ['BGU', 'BDU']
    for acnum in fleet:
        merged_predictions = make_predictions(X_test_path, acnum)
        if merged_predictions is not None:
            merged_predictions.to_csv(f'data/X_with_predictions_{acnum}.csv', index=False)
            print("Predictions saved successfully.")
        else:
            print("Failed to make predictions.")
"""