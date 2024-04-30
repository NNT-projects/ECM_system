import pickle
import pandas as pd


from data_preprocessing import preprocess_raw_data

def make_predictions(X_test_path, acnum):
    try:
        X_test = pd.read_csv(X_test_path, parse_dates=['reportts'])
        
        X_processed = preprocess_raw_data(X_test, f'VQ-{acnum}')

        with open(f'models/lgb_model_{acnum}.txt', 'rb') as f:
            trained_model = pickle.load(f)

        predictions = trained_model.predict(X_processed)
        
        predictions_df = pd.DataFrame(predictions, columns=['egtm'])
        merged_dataset = pd.concat([X_test[X_test['acnum'] == f'VQ-{acnum}'], predictions_df], axis=1)

        return merged_dataset

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# def make_predictions(X_test_path, acnum):
#     try:
#         X_processed = preprocess_raw_data(X_test_path, f'VQ-{acnum}')

#         # Load the trained model
#         with open(f'models/lgb_model_{acnum}.txt', 'rb') as f:
#             trained_model = pickle.load(f)

#         # Make predictions using the trained model
#         predictions = trained_model.predict(X_processed)
        
#         predictions_df = pd.DataFrame(predictions, columns=['egtm'])
#         predictions_df.to_csv(f'data/predictions_{acnum}', index=False)

#         return "success"

#     except Exception as e:
#         return str(e)

# problem: predictions according to sorted by time dataset
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

