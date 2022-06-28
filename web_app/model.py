#   this file is used to run an interactive webapp
#   for the model discussed in model.ipynb file

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
from joblib import dump, load

#   load data

file_name = "./train-chennai-sale.csv"
df = pd.read_csv(file_name)

#   drop null rows/redundant columns

to_drop = ["QS_ROOMS", "QS_BATHROOM",
           "QS_BEDROOM", "QS_OVERALL", "DIST_MAINROAD",
           "PRT_ID", "REG_FEE", "COMMIS"]
df.drop(to_drop, axis=1, inplace=True)
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)

#   fix the dtypes


def fix_dtpes(df_):
    columns = df_.select_dtypes(include='object').columns
    dtype_map = dict(zip(columns, ['str']*len(columns)))
    df_ = df_.astype(dtype_map)
    date_cnames = list(filter(lambda cname: cname.startswith("DATE"), columns))
    for cname in date_cnames:
        df_[cname] = \
            pd.to_datetime(df_[cname].str.strip(), format="%d-%m-%Y")
    columns = df_.select_dtypes(include='float').columns
    int_cnames = list(filter(lambda cname: cname.startswith("N_"), columns))
    dtype_map_obj = dict(zip(int_cnames, [np.int32]*len(int_cnames)))
    return df_.astype(dtype_map_obj)


df = fix_dtpes(df)

#   fix spelling


def transform_str(str_: str):
    return str_.replace(" ", "").lower()


obj_cnames = df.select_dtypes(include='object').columns

for cname in obj_cnames:
    df[cname] = df[cname].apply(transform_str)

mapping_obj_ = {'AREA': {'karapakkam': [('karapakam', 95)],
                         'annanagar': [('ananagar', 94), ('annnagar', 94)],
                         'adyar': [('adyr', 89)],
                         'velachery': [('velchery', 94)],
                         'chrompet': [('chrompt', 93), ('chrmpet', 93), ('chormpet', 88)],
                         },
                'SALE_COND': {'partial': [('partiall', 93)]},
                'PARK_FACIL': {'no': [('noo', 90)]},
                'BUILDTYPE': {'commercial': [('comercial', 95)], 'other': [('others', 91)]},
                'UTILITY_AVAIL': {'nosewr': [('nosewa', 83)]},
                'STREET': {'paved': [('pavd', 89)]},
                }
mapping_obj = {}
for key, value in mapping_obj_.items():
    temp_obj = {}
    for sub_key, sub_val in value.items():
        list_ = list(map(lambda item: item[0], sub_val))
        dict_ = dict(zip(list_, [sub_key]*len(list_)))
        temp_obj = {**dict_, **temp_obj}
    mapping_obj[key] = temp_obj

df.replace(mapping_obj, inplace=True)


#   Add new features
def add_features(df_):
    df_["AVG_ROOM_SIZE"] = (df_["INT_SQFT"]/df_["N_ROOM"]).round(0)
    df_["AGE"] = (df_["DATE_SALE"]-df_["DATE_BUILD"]).dt.days
    df_["MARKET_CRASH"] = pd.Series(np.zeros(df_.shape[0], dtype=np.int8))
    mask = (df_["DATE_SALE"] >=
            "01-07-2009") & (df_["DATE_SALE"] <= "01-03-2012")
    df_.loc[mask, "MARKET_CRASH"] = 1

    #   drop redundant columns

    to_drop = ["DATE_BUILD", "DATE_SALE"]
    df_.drop(to_drop, axis=1, inplace=True)
    return df_


df = add_features(df)


#   Split to features and target

X, y = df.drop("SALES_PRICE", axis=1), df["SALES_PRICE"]


#   Encoding features

cnames = df.select_dtypes(include=['object']).columns

label_map = {}
for i, cname in enumerate(cnames):
    data = pd.DataFrame({"SALES_PRICE": y, "cname": X[cname]}).groupby("cname")\
        .mean().sort_values("SALES_PRICE")
    indices = data.index.to_list()
    label_map[cname] = dict(zip(indices, range(len(indices))))

values = list(label_map["BUILDTYPE"].values())
keys = label_map["BUILDTYPE"].keys()


def transform(x): return np.round(np.exp(x),).astype("int16")


label_map["BUILDTYPE"] = dict(zip(keys, map(transform, values)))
X.replace(label_map, inplace=True)


#   Scaling

scaler = StandardScaler()
scaler.fit_transform(X)


# Cluster labeling

cluster_model = KMeans(n_clusters=2)
scaled_df = X[["AVG_ROOM_SIZE", "INT_SQFT"]]
cluster_model.fit(scaled_df.to_numpy())


def add_cluster_label(df_):
    cluster_label = cluster_model.predict(
        df_[["AVG_ROOM_SIZE", "INT_SQFT"]].to_numpy())
    df_["AVG_ROOM_SIZE"] = pd.Series(cluster_label, index=df_.index)
    return df_


X = add_cluster_label(X)


#   Model

class GradientBoostingRange():
    def __init__(self, l_quantile=0.1, u_quantile=0.9):
        kv_hp = {"learning_rate": 0.1, "max_depth": 4, "n_estimators": 200}
        self.lower_model = GradientBoostingRegressor(loss="quantile",
                                                     alpha=l_quantile, **kv_hp)
        self.mid_model = GradientBoostingRegressor(**kv_hp)
        self.upper_model = GradientBoostingRegressor(loss="quantile",
                                                     alpha=u_quantile, **kv_hp)

    def fit(self, X_train, y_train):
        self.lower_model.fit(X_train, y_train)
        self.mid_model.fit(X_train, y_train)
        self.upper_model.fit(X_train, y_train)
        models = [self.lower_model, self.mid_model, self.upper_model]
        scores = [r2_score(y_train, model.predict(X_train))for model in models]
        print(scores, "\nModel Ready!")

    def predict(self, X_predict):
        predictions = {}
        predictions['lower'] = self.lower_model.predict(X_predict)
        predictions['mid'] = self.mid_model.predict(X_predict)
        predictions['upper'] = self.upper_model.predict(X_predict)
        return pd.DataFrame(predictions)


model = None
try:
    model = load('model.joblib')
except:
    print("Model dump loading failed!")
    print("Refitting Model!")
    model = GradientBoostingRange()
    model.fit(X, y)
    print('Dumping Model!')
    dump(model, 'model.joblib')


def predict(input_df):
    input_df = fix_dtpes(input_df)
    input_df = add_features(input_df)
    for cname in obj_cnames:
        input_df[cname] = input_df[cname].apply(transform_str)
    input_df.replace(label_map, inplace=True)
    scaler.transform(input_df)
    input_df = add_cluster_label(input_df)
    result = model.predict(input_df)
    return result
