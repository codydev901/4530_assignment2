import pandas as pd

import plotly.express as px

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 2

For Dataset 1 - 4 Dimensions

parse and plot steps separated into separate functions.
"""


def make_country_continent_lookup():

    df = pd.read_csv("raw_data/countryContinent.csv")

    lu = {}
    for i, row in df.iterrows():
        lu[row["country"]] = row["continent"]

    return lu


def parse_data():
    """
    Parse step for life expectancy/school data
    """

    # Load and take quick look
    raw_df = pd.read_csv("raw_data/Life Expectancy Data.csv")
    print(raw_df.head())
    print(raw_df.info())

    # Subset to attributes of interest
    raw_df = raw_df[["Country", "Year", "Life expectancy ", "Schooling"]]  # Note the " " after life-expectancy in raw..
    print(raw_df.head())
    print(raw_df.info())

    # DropNA (~200 of 2938 points)
    raw_df = raw_df.dropna()
    print(raw_df.info())

    # rename columns
    raw_df = raw_df.rename(columns={"Country": "country", "Year": "year",
                                    "Life expectancy ": "life_expectancy",
                                    "Schooling": "years_education"})
    print("OK")
    print(raw_df.info())

    # Map country to continent
    # Doing this iteratively since might needed to fix things in the lookup (The former Yugoslav republic of Macedonia)
    continent_lu = make_country_continent_lookup()
    continent_values = []
    for i, row in raw_df.iterrows():
        try:
            continent = continent_lu[row["country"]]
        except KeyError:
            print(row["country"])
            exit()
        continent_values.append(continent)
    raw_df["continent"] = continent_values
    print(raw_df.head())
    print(raw_df.info())

    # So now we want to get the average life_expectancy and years_education each year/each continent
    # Will just do this iteratively
    # Note the attr_key/attr_value format, for easier plotting
    final_df = [["year", "continent", "quality_metric", "quality_value"]]
    for year in raw_df["year"].unique().tolist():
        for continent in raw_df["continent"].unique().tolist():
            sub_df = raw_df[(raw_df["year"] == year) &
                            (raw_df["continent"] == continent)]
            mean_life = sub_df["life_expectancy"].mean()
            mean_school = sub_df["years_education"].mean()
            final_df.append([year, continent, "avg_life_expectancy_minus_50", mean_life-50.0])  # Mean Life-50 to Scale
            final_df.append([year, continent, "avg_years_education", mean_school])

    final_df = pd.DataFrame(data=final_df[1:], columns=final_df[0])
    print(final_df.head())
    print(final_df.info())

    # Write
    final_df.to_csv("parsed_data/school_life_parsed.csv", index=False)


def plot_data():
    """
    Plot step for life expectancy/school data
    """

    df = pd.read_csv("parsed_data/school_life_parsed.csv")

    fig = px.bar(data_frame=df, x="year", y="quality_value", color="quality_metric",
                 barmode="group", facet_col="continent", facet_col_wrap=2,
                 text_auto='.2f',
                 title="Avg Life Expectancy and Years Schooling By Continent For Years 2000-2015")
    fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    fig.show()


def main():

    parse_data()

    plot_data()


if __name__ == "__main__":

    main()

