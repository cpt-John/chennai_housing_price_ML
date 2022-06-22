#   this file is used to run an interactive webapp
#   for the model discussed in model.ipynb file

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

#   load data

file_name = "../train-chennai-sale.csv"
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
    df_["N_OTHERROOM"] = df_["N_ROOM"] - \
        (df_[["N_BEDROOM", "N_BATHROOM"]].sum(axis=1))
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

model = GradientBoostingRegressor(
    learning_rate=0.1, max_depth=4, n_estimators=200)
model.fit(X, y)
print(model.score(X, y))


def predict(input_data):
    # input_data =\
    #     {'AREA': 'Karapakkam', 'INT_SQFT': 1004, 'DATE_SALE': '04-05-2011', 'N_BEDROOM': 1.0, 'N_BATHROOM': 1.0, 'N_ROOM': 3, 'SALE_COND': 'AbNormal',
    #         'PARK_FACIL': 'Yes', 'DATE_BUILD': '15-05-1967', 'BUILDTYPE': 'Commercial', 'UTILITY_AVAIL': 'AllPub', 'STREET': 'Paved', 'MZZONE': 'A'}
    input_dict = {k: [float(v)] if v.isnumeric() else [str(v)]
                  for k, v in input_data.items()}
    input_df = pd.DataFrame(input_dict)
    input_df = fix_dtpes(input_df)
    input_df = add_features(input_df)
    for cname in obj_cnames:
        input_df[cname] = input_df[cname].apply(transform_str)
    input_df.replace(label_map, inplace=True)
    scaler.fit_transform(input_df)
    input_df = add_cluster_label(input_df)
    result = model.predict(input_df)[0]
    return round(result, 0)
