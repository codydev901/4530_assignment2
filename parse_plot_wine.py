import pandas as pd

import plotly.graph_objs as go

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 2

For Dataset 3 - 6 Dimensions (technically did 7, 6 continuous quantitative and 1 ordinal)

parse and plot steps separated into separate functions.
"""


def get_quality_grade(raw_quality: int):
    """
    Helper function for reducing range of possible values for quality attribute
    """

    if raw_quality <= 4:  # 3, 4
        return 0.0

    if raw_quality <= 6:  # 5, 6
        return 0.5

    return 1.0         # 7, 8


def parse_data():
    """
    Parsing portion of the wine quality data set.

    Writes to parsed_data.
    """

    # CSV to Dataframe, basic check
    raw_df = pd.read_csv("raw_data/winequality-red.csv")
    print(raw_df.head())
    print(raw_df.info())

    # So no nulls, 12 attributes. We want quality + 6 others
    # Lets pick the 6 w/ the observed variation by comparing the coefficient of variation for each attribute
    abs_attr_diff = []
    for attr in raw_df.columns:
        sub_df = raw_df[attr]
        cf_var_v = sub_df.std() / sub_df.mean()
        abs_attr_diff.append([attr, cf_var_v, sub_df.min(), sub_df.max()])
    abs_attr_diff.sort(key=lambda x: x[1], reverse=True)
    for v in abs_attr_diff:
        print(v)

    keep_attributes = [v[0] for v in abs_attr_diff[:6]] + ["quality"]
    print("Keep Attributes - We Want 6 + Quality")
    print(keep_attributes)

    # Remove the unused attributes
    raw_df = raw_df[keep_attributes]
    print(raw_df.info())

    # Bucket quality to 3 grades from 6, where 1 is low, 2 is medium, 3 is high
    print("Bucket Quality From 6 to 3 Levels")
    print(raw_df.head())
    print(raw_df.tail())
    raw_df["quality"] = raw_df["quality"].apply(lambda x: get_quality_grade(x))
    print(raw_df.head())
    print(raw_df.tail())

    # Write this to .csv for PCA stuff
    raw_df.to_csv("parsed_data/wine_pca.csv", index=False)

    # Reduce Complexity Further By Taking Median Values For Each Quality Level
    final_df = [raw_df.columns.tolist()]
    for quality in raw_df["quality"].unique().tolist():
        sub_df = raw_df[raw_df["quality"] == quality]
        quality_row = []
        for attr in raw_df.columns.tolist():
            median_value = sub_df[attr].median()
            quality_row.append(median_value)
        final_df.append(quality_row)

    final_df = pd.DataFrame(data=final_df[1:], columns=final_df[0])
    print(final_df.head())

    # But let's also preserve the original full ranges for use in the plot
    range_df = [["attr_key", "attr_min", "attr_max"]]
    for attr in raw_df.columns:
        sub_df = raw_df[attr]
        min_v = sub_df.min()
        max_v = sub_df.max()
        range_df.append([attr, min_v, max_v])

    range_df = pd.DataFrame(data=range_df[1:], columns=range_df[0])
    print(range_df.head())

    # Write for use in plots
    final_df.to_csv("parsed_data/wine_quality_median_values.csv", index=False)
    range_df.to_csv("parsed_data/wine_quality_original_range.csv", index=False)


def plot_data():
    """
    Plotting portion for the wine quality dataset

    https://plotly.com/python/parallel-coordinates-plot/
    """

    value_df = pd.read_csv("parsed_data/wine_quality_median_values.csv")
    range_df = pd.read_csv("parsed_data/wine_quality_original_range.csv")

    # Put range_df into a dict for easy access below
    range_dict = {}
    for i, row in range_df.iterrows():
        range_dict[row["attr_key"]] = [row["attr_min"], row["attr_max"]]

    # Plot rather manually w/ go.Figure, this avoids a continuous color_scale display w/ express.
    fig = go.Figure(data=
                    go.Parcoords(
                        line=dict(color=value_df["quality"],
                                  colorscale=[[0.0, 'red'], [0.5, 'yellow'], [1.0, 'green']]),
                        dimensions=list([
                            dict(range=[range_dict['citric acid'][0], range_dict['citric acid'][1]],
                                 label='citric acid', values=value_df['citric acid']),
                            dict(range=[range_dict['total sulfur dioxide'][0], range_dict['total sulfur dioxide'][1]],
                                 label='total sulfur dioxide', values=value_df['total sulfur dioxide']),
                            dict(range=[range_dict['free sulfur dioxide'][0], range_dict['free sulfur dioxide'][1]],
                                 label='free sulfur dioxide', values=value_df['free sulfur dioxide']),
                            dict(range=[range_dict['residual sugar'][0], range_dict['residual sugar'][1]],
                                 label='residual sugar', values=value_df['residual sugar']),
                            dict(range=[range_dict['chlorides'][0], range_dict['chlorides'][1]],
                                 label='chlorides', values=value_df['chlorides']),
                            dict(range=[range_dict['volatile acidity'][0], range_dict['volatile acidity'][1]],
                                 label='volatile acidity', values=value_df['volatile acidity'])
                        ])
                    ))

    # Set Title and add a Color/Quality Annotation
    fig.update_layout(title="Median Physicochemical Property Values and Quality For Red Wine")
    fig.add_annotation(
        text='Color: Green indicates high quality, Yellow medium quality, and Red low quality',
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.01,
        y=1.07,
        bordercolor='black',
        borderwidth=1)

    fig.show()


def main():

    parse_data()

    plot_data()


if __name__ == "__main__":

    main()

