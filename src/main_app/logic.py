import numpy as np
import pandas as pd
from scipy.cluster.vq import kmeans2

def do_cluster(_df, n_clusters):
    
    df = _df.copy()

    encode = {cat:i for i,cat in enumerate(df["mode_category"].unique())}
    decode = {v:k for k,v in encode.items()}

    df["mode_category"] = df["mode_category"].map(encode)
    df["bought_premium"] = df["bought_premium"].astype(int)

    _centroids, labels = kmeans2(df.iloc[:,1:], k=n_clusters,
                iter=10, thresh=1e-5, minit='++')
    
    centroids = []
    for i,c in enumerate(_centroids):
        d = dict()
        d["cluster_size"] = int(np.where(labels==i,1,0).sum())
        d["cluster"] = i
        d["cnt_sales"] = int(max(0, c[0]))
        d["avg_price"] = float(c[1])
        d["med_price"] = float(c[2])
        d["user_age"] = float(c[3])
        d["bought_premium"] = bool(abs(c[-2]-1) <= abs(c[-2]-0))
        d["mode_category"] = decode[min(max(0,int(c[-1])),7)]
        centroids.append(d)

    return centroids, labels

