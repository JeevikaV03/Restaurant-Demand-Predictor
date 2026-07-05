import pandas as pd

def load_and_preprocess(path):
    df = pd.read_csv(path)

    # convert date column
    df['date'] = pd.to_datetime(df['date'])

    # create features
    df['day'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day'].apply(lambda x: 1 if x >= 5 else 0)

    # convert item to numbers
    df = pd.get_dummies(df, columns=['item'])

    # split input/output
    X = df.drop(columns=['date', 'orders'])
    y = df['orders']

    return X, y


# test code
if __name__ == "__main__":
    X, y = load_and_preprocess("data/orders.csv")
    print(X.head())