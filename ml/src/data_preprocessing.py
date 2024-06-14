import pandas as pd
from sklearn.preprocessing import LabelEncoder, FunctionTransformer
from sklearn.pipeline import Pipeline

from utils import split, label_encode, create_date_features

def preprocess_training_data(X_train_path, y_train_path, acnum):

    X_train = pd.read_csv('data/X_train.csv', parse_dates=['reportts'])
    y_train = pd.read_csv('data/y_train.csv', parse_dates=['reportts'])

    # X_test = pd.read_csv('../data/X_test.csv', parse_dates=['reportts'])

    X_train.rename(columns={"reportts": "datetime"}, inplace=True);
    # X_test.rename(columns={"reportts": "datetime"}, inplace=True);
    y_train.rename(columns={"reportts": "datetime"}, inplace=True);

    dataset = X_train.merge(y_train, on=['acnum', 'pos', 'datetime']).dropna(subset=['egtm'])
    dataset_time_sorted = dataset.sort_values(by='datetime').reset_index(drop=True)

    pipeline_training = Pipeline([
        ('drop_nan_columns', FunctionTransformer(lambda X: X.dropna(axis=1, how='all'))),
    #     ('custom_feature_engineering', FunctionTransformer(custom_feature_engineering)),
        ('filter_data', FunctionTransformer(lambda X: X[X['acnum'] == acnum].reset_index(drop=True))),
        ('label_encode', FunctionTransformer(label_encode)),
        ('train_test_split', FunctionTransformer(split))
    ])

    X_train_processed, X_val_processed, y_train_processed, y_val_processed = pipeline_training.fit_transform(dataset_time_sorted)

    # Fill NaNs after train-test split
    # imputer = SimpleImputer(strategy='constant', fill_value=0)
    # X_train = imputer.fit_transform(X_train)
    # X_test = imputer.transform(X_test)

    # Save X_train and X_val to CSV files
    X_train_processed.to_csv('tmp_data/X_train.csv', index=False)
    X_val_processed.to_csv('tmp_data/X_val.csv', index=False)
    y_train_processed.to_csv('tmp_data/y_train.csv', index=False, header=True)
    y_val_processed.to_csv('tmp_data/y_val.csv', index=False, header=True)
    
    return X_train_processed, y_train_processed, X_val_processed, y_val_processed

def preprocess_raw_data(X, acnum):
    try:
        dataset_time_sorted = X.sort_values(by='reportts').reset_index(drop=True)
        
        pipeline_predicting = Pipeline([
            ('drop_nan_columns', FunctionTransformer(lambda X: X.dropna(axis=1, how='all'))),
            ('custom_feature_engineering', FunctionTransformer(create_date_features)),
            ('filter_data', FunctionTransformer(lambda X: X[X['acnum'] == acnum].reset_index(drop=True))),
            ('label_encode', FunctionTransformer(label_encode)),
        ])
        
        X_processed = pipeline_predicting.transform(dataset_time_sorted).drop(["reportts", "egtm", "acnum"], axis=1, errors="ignore")
        
        return X_processed

    except Exception as e:
        print(f"Error in preprocess_raw_data: {str(e)}")
        return None
