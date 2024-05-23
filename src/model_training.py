import pandas as pd

# !pip install lightgbm -q
import lightgbm as lgbm
from lightgbm import Dataset
import pickle

def train_model(X_train_path, X_val_path, y_train_path, y_val_path, model_path):

    X_train = pd.read_csv(X_train_path)
    X_val = pd.read_csv(X_val_path)

    y_train = pd.read_csv(y_train_path)
    y_val = pd.read_csv(y_val_path)

    random_state = 42

    if model_path == 'models/lgb_model_BGU.txt':
        lgb_model_rmse = lgbm.LGBMRegressor(objective="rmse",
                                        learning_rate=0.25,
                                        random_state=random_state,
                                        cat_feature=[0,2,3],
                                        boosting_type="dart",
                                        max_bin=200,
                                        num_leaves=10,
                                        reg_lambda=1,
                                        n_jobs=1,
                                        verbose=-1
                                        )
    else:
        lgb_model_rmse = lgbm.LGBMRegressor(objective="rmse",
                                        learning_rate=0.25,
                                        random_state=random_state,
                                        cat_feature=[0,2,3],
                                        boosting_type="dart",
                                        max_bin=400,
                                        num_leaves=10,
                                        reg_lambda=1,
                                        n_jobs=1,
                                        verbose=-1
                                        )

    lgb_model_rmse.fit(X_train,
                    y_train,
                    eval_set=[(X_val, y_val)],
                    eval_metric='rmse',
                    # callbacks=[lgbm.early_stopping(stopping_rounds=50)],
                    )

    # lgb_model_rmse.booster_.save_model('models/lgb_model.txt')
    # joblib.dump(lgb_model_rmse, 'models/lgb_model.pkl')
    pickle.dump(lgb_model_rmse, open(model_path, 'wb'))

    
    return lgb_model_rmse