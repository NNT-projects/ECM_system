import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# получаем датасет
# разбиваем на X,y
# делаем train-test split
# либо меняем тип на category, либо делаем label encoding
# заполняем nan'ы
# делаем другие фичи
# возвращаем X_train, X_test, y_train, y_test

def split(dataset):
    drop_cols = ["reportts", "egtm", "acnum"]
    
    X = dataset.drop(drop_cols, axis=1, errors="ignore")
    y = dataset["egtm"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)
    
    return X_train, X_test, y_train, y_test

def label_encode(dataset):
    encoder = LabelEncoder()
    features_to_encode = ['dep', 'arr']
    for col in features_to_encode:
        dataset[col] = encoder.fit_transform(dataset[col])
        
    return dataset