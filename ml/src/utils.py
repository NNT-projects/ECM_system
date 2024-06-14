import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def split(dataset):
    drop_cols = ["reportts", "egtm", "acnum"]
    
    X = dataset.drop(drop_cols, axis=1, errors="ignore")
    y = dataset["egtm"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)
    
    return X_train, X_test, y_train, y_test

def label_encode(dataset):
    cat_features = ['pos','dep', 'arr', 'part_of_day', 'season']

    for col in cat_features:
        dataset[col] = dataset[col].astype('category')
    
    encoder = LabelEncoder()
    features_to_encode = ['dep', 'arr']
    for col in features_to_encode:
        dataset[col] = encoder.fit_transform(dataset[col])
        
    return dataset

# Determine the part of the day
def get_part_of_day(hour):
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'


# Determine the season
def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'


def create_date_features(dataset):
    # Ensure we are not working with a copy of a slice
    dataset = dataset.copy()

    # Convert the 'reportts' column to datetime format
    dataset.loc[:, 'reportts'] = pd.to_datetime(dataset['reportts'])

    # Extracting various time-based features
    dataset.loc[:, 'year'] = dataset['reportts'].dt.year
    dataset.loc[:, 'month'] = dataset['reportts'].dt.month
    dataset.loc[:, 'day'] = dataset['reportts'].dt.day
    dataset.loc[:, 'day_of_week'] = dataset['reportts'].dt.dayofweek
    dataset.loc[:, 'hour'] = dataset['reportts'].dt.hour
    dataset.loc[:, 'minute'] = dataset['reportts'].dt.minute
    dataset.loc[:, 'second'] = dataset['reportts'].dt.second
    
    dataset.loc[:, 'part_of_day'] = dataset['hour'].apply(get_part_of_day)
    dataset.loc[:, 'season'] = dataset['month'].apply(get_season)
        
    return dataset