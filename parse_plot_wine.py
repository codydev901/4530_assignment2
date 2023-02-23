import pandas as pd

import plotly.express as px

"""
Doc Doc Doc
"""


def get_quality_grade(raw_quality: int):

    if raw_quality <= 4:  # 3, 4
        return 1

    if raw_quality <= 6:  # 5, 6
        return 2

    return 3         # 7, 8


def parse_data():

    # CSV to Dataframe, basic check
    raw_df = pd.read_csv("raw_data/winequality-red.csv")
    print(raw_df.head())
    print(raw_df.info())

    # So no nulls, 12 attributes. We want quality + 5 others
    # Lets pick the 5 w/ the most potential variation
    # May or may not use this!
    abs_attr_diff = []
    for attr in raw_df.columns:
        sub_df = raw_df[attr]
        cf_var_v = sub_df.std() / sub_df.mean()
        abs_attr_diff.append([attr, cf_var_v, sub_df.min(), sub_df.max()])
    abs_attr_diff.sort(key=lambda x: x[1], reverse=True)
    for v in abs_attr_diff:
        print(v)

    # Change quality to a pure categorical string
    raw_df["quality_grade"] = raw_df["quality"].apply(lambda x: get_quality_grade(x))

    # Now need to normalize, lets use Min-Max
    # Also setup new DataFrame for eventual plotting
    parsed_df = {}
    for attr in raw_df.columns:
        if attr in ["quality", "quality_grade"]:
            parsed_df[attr] = raw_df[attr].tolist()
            continue

        sub_df = raw_df[attr]
        min_v = sub_df.min()
        max_v = sub_df.max()
        norm_v = [(v-min_v) / (max_v - min_v) for v in sub_df.tolist()]
        parsed_df[attr] = norm_v

    parsed_df = pd.DataFrame(parsed_df)

    # Check our new DF
    print(parsed_df.head())
    for attr in parsed_df.columns:
        if attr in ["quality_grade"]:
            continue
        sub_df = parsed_df[attr]
        cf_var_v = sub_df.std() / sub_df.mean()
        print(attr, cf_var_v, sub_df.min(), sub_df.max())

    # Do one more transformation for easier plotting
    final_df = [["wine_id", "attr_key", "attr_value", "quality_grade"]]
    for i, row in parsed_df.iterrows():
        for attr_key in parsed_df.columns:
            if attr_key in ["quality", "quality_grade"]:  # This is inefficient, but small size
                continue
            final_df.append([i, attr_key, row[attr_key], row["quality_grade"]])

    final_df = pd.DataFrame(data=final_df[1:], columns=final_df[0])
    print(final_df.head())

    # return parsed_df
    return final_df


def plot_data():

    df = parse_data()

    dims = df.columns.tolist()
    dims.remove("quality_grade")
    # dims.remove("quality")

    # fig = px.parallel_coordinates(data_frame=df,
    #                               color="quality_grade",
    #                               dimensions=dims,
    #                               color_continuous_scale=px.colors.diverging.Tealrose,
    #                               color_continuous_midpoint=2
    #                               )

    # fig.show()

    fig = px.scatter(data_frame=df, x="attr_key", y="attr_value", color="quality_grade")
    fig.show()


def main():

    # parse_data()

    plot_data()


if __name__ == "__main__":

    main()

