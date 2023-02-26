import pandas as pd

import plotly.express as px

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 2

For Dataset 2 - 5 Dimensions

parse and plot steps separated into separate functions.
"""


def had_stroke(x):
    """
    Helper function for transforming 0/1 stroke state to "yes"/"no"
    """

    if x:
        return "yes"

    return "no"


def parse_data():
    """
    Parse step for stroke data.

    This one ended up being pretty simple to parse, but did use something I hadn't used yet for datasets in this
    class (.sample()).
    """

    # Read and print
    raw_df = pd.read_csv("raw_data/healthcare-dataset-stroke-data.csv")
    print(raw_df.head())
    print(raw_df.info())

    # Drop NA, roughly 200 of 5100 samples
    raw_df = raw_df.dropna()
    print(raw_df.info())

    # Count Number of Stroke/Non-Stroke
    print(raw_df[raw_df["stroke"] == 1].count())
    print(raw_df[raw_df["stroke"] == 0].count())

    # Lets get rid of some attributes/keep those we want to look at
    # We are limiting this data set to 5 attributes. These are a mix of data types and perhaps most interesting imo.
    keep_attributes = ['gender', 'age', 'bmi', 'avg_glucose_level', 'stroke']
    raw_df = raw_df[keep_attributes]
    print(raw_df.info())

    # So majority of data is non-stroke, 4700 vs 209
    # Lets take a random sample of the non-stroke to reduce number of points for scatter.
    has_stroke_df = raw_df[raw_df["stroke"] == 1]
    no_stroke_df = raw_df[raw_df["stroke"] == 0]

    print(no_stroke_df.head())
    # Note replace=False (same point cannot be sampled twice, and random_state for reproducibility)
    no_stroke_df = no_stroke_df.sample(n=len(has_stroke_df)*2, replace=False, random_state=1337)
    print(no_stroke_df.head())

    # Combine the no_stroke and has_stroke
    final_df = pd.concat([has_stroke_df, no_stroke_df])

    # Change stroke to yes/no from int
    final_df["stroke"] = final_df["stroke"].apply(lambda x: had_stroke(x))
    print(final_df.head())

    # Write out
    final_df.to_csv("parsed_data/stroke_parsed.csv", index=False)


def plot_data():
    """
    Plot step for stroke data set

    https://plotly.com/python/line-and-scatter/
    """

    df = pd.read_csv("parsed_data/stroke_parsed.csv")
    print(df.head())
    print(df.info())

    fig = px.scatter(data_frame=df, x='age', y='bmi', color='stroke',
                     size='avg_glucose_level', symbol='gender',
                     color_discrete_map={"yes": "red", "no": "green"},
                     title="Stroke Event and Age/BMI/Gender/Avg Glucose Level")
    fig.add_annotation(
        text='Size: Smaller Point Size == Lower Avg Glucose Level',
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=1.02,
        bordercolor='black',
        borderwidth=1)

    fig.show()


def main():

    parse_data()

    plot_data()


if __name__ == "__main__":

    main()


