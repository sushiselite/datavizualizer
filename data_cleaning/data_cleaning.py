import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy import stats

def handle_missing_values(df):
    df.fillna(method='ffill', inplace=True)
    return df

def drop_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df

def normalize_data(df):
    min_max_scaler = preprocessing.MinMaxScaler()
    df[df.select_dtypes(include=[np.number]).columns] = min_max_scaler.fit_transform(
        df.select_dtypes(include=[np.number])
    )
    return df

def encode_categorical(df):
    return pd.get_dummies(df)

def filter_outliers(df):
    z_scores = stats.zscore(df.select_dtypes(include=[np.number]))
    return df[(np.abs(z_scores) < 3).all(axis=1)]
