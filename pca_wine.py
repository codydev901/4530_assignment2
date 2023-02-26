import pandas as pd
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from sklearn.decomposition import PCA

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 2

PCA Portion, just did this in one step since it was quick.

I followed steps in this post from the Assignment 2 Doc
https://medium.com/swlh/an-intuitive-approach-to-pca-fc4d05c14c19
"""


def main():

    raw_df = pd.read_csv("parsed_data/wine_pca.csv")
    print("Raw Data")
    print(raw_df.head())

    # Only perform PCA on the quantitative attributes
    features = raw_df.columns.tolist()
    features.remove("quality")
    print("Features")
    print(features)

    # SVD Scale
    features_df = raw_df[features]
    scaled_features = StandardScaler().fit_transform(features_df)

    # PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_features)
    pca_1, pca_2 = [], []
    for row in principal_components:
        pca_1.append(row[0])
        pca_2.append(row[1])

    # Add PCA back to original DataFrame
    raw_df["pca_1"] = pca_1
    raw_df["pca_2"] = pca_2
    print(raw_df.head())

    # Change to string cat for plot color
    quality_bucket = {0.0: "low",
                      0.5: "medium",
                      1.0: "high"}
    raw_df["quality_str"] = raw_df["quality"].apply(lambda x: quality_bucket[x])

    # PCA Graph
    fig = px.scatter(data_frame=raw_df,
                     x="pca_1",
                     y="pca_2",
                     color="quality_str",
                     color_discrete_map={"low": "red",
                                         "medium": "yellow",
                                         "high": "green"},
                     title="Red Wine Quality PCA 2 vs. PCA 1")

    fig.show()

    # Original Graph
    fig = px.scatter(data_frame=raw_df,
                     x="citric acid",
                     y="volatile acidity",
                     color="quality_str",
                     color_discrete_map={"low": "red",
                                         "medium": "yellow",
                                         "high": "green"},
                     title="Red Wine Quality Volatile Acidity vs. Citric Acid")

    fig.show()


if __name__ == "__main__":

    main()
