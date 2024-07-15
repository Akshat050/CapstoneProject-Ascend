from pandas import DataFrame, isna
import re

from dateutil import parser


def clean_data(df: DataFrame, type: str):
    df = fill_nas(df)
    df["Year landed in Canada enter 0 if not yet landed"] = df[
        "Year landed in Canada enter 0 if not yet landed"
    ].apply(extract_year)
    df = df.drop_duplicates()
    df = fix_country_columns(df)
    df.reset_index(drop=True, inplace=True)
    if type == "signup":
        result_df = clean_signup(df)
    elif type == "exams":
        result_df = clean_exams(df)
    elif type == "eval":
        result_df = clean_eval(df)
    elif type == "survey":
        result_df = clean_survey(df)
    return result_df


def fill_nas(df: DataFrame):
    for colum in df.columns.to_list():
        if colum == "CompletionDate":
            df.fillna({colum: "0"}, inplace=True)
        elif colum in ["Eval Response", "UserAnswer"]:
            df.fillna({colum: "NA"}, inplace=True)
        else:
            df.fillna({colum: "Prefer not to disclose"}, inplace=True)
    return df


# Function to extract the year from various date formats
def extract_year(date_str):
    if isna(date_str):
        return None  # Handle NaN values
    elif str(date_str).strip() == "0":  # Explicitly check for '0' as a string
        return "0"  # Return '0' as a string to keep the format consistent

    try:
        # Convert to string to handle any non-string types
        date_str = str(date_str)
        # Parse the date and extract the year
        return str(parser.parse(date_str).year)
    except ValueError:
        return None  # Returns None if the date string is invalid


def looks_like_date(value):
    date_patterns = [
        r"\d{1,2}-[A-Za-z]{3}",  # e.g., 12-Sep
        r"[A-Za-z]{3} \d{1,2} \d{4}",  # e.g., OCT 11 1973
        r"[A-Za-z]{4,9}-\d{2}-\d{4}",  # e.g., june-03-1991
        r"\d{2}/\d{2}/\d{4}",  # e.g., 24/12/1994
        r"\d{1,2}/\d{1,2}/\d{4}",  # e.g., 1/1/1993
        r"\d{4}/[A-Za-z]{4,9} \d{1,2}",  # e.g., 1967/september 24
        r"\d{1,2}/\d{1,2}/\d{4}",  # e.g., 9/9/1990
        r"[A-Za-z]{3,9}-\d{1,2}-\d{4}",  # e.g., june-03-1991
        r"\d{4}\.\d{1,2}\.\d{1,2}",  # e.g., 1991.03.02 or 1991.3.2
    ]
    return any(re.match(pattern, str(value)) for pattern in date_patterns)


def fix_country_columns(df: DataFrame):
    # Optionally, normalize the text to handle any special characters
    df["Country you have_will immigrate from"] = (
        df["Country you have_will immigrate from"]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )
    df["Country of birth"] = (
        df["Country of birth"]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )
    # Apply the function to identify date-like entries
    condition = df["Country of birth"].apply(looks_like_date)

    # Replace date-like entries with the corresponding values from "Country you have_will immigrate from"
    df.loc[condition, "Country of birth"] = df.loc[
        condition, "Country you have_will immigrate from"
    ]
    condition = (
        df["Country you have_will immigrate from"] == "Prefer not to disclose"
    ) & (df["Country of birth"] != "Prefer not to disclose")

    df.loc[condition, "Country you have_will immigrate from"] = df.loc[
        condition, "Country of birth"
    ]
    condition = (df["Country of birth"] == "Prefer not to disclose") & (
        df["Country you have_will immigrate from"] != "Prefer not to disclose"
    )
    df.loc[condition, "Country of birth"] = df.loc[
        condition, "Country you have_will immigrate from"
    ]
    # Update the 'Country of birth' and 'Country you have_will immigrate from' columns
    df.loc[
        df["Username"] == "fessehad27@gmail.com",
        ["Country of birth", "Country you have_will immigrate from"],
    ] = "Euthiopia"
    df.loc[
        df["Username"] == "hong008sec@hotmail.com",
        ["Country of birth", "Country you have_will immigrate from"],
    ] = "China"
    df.loc[
        df["Username"] == "chudasama.h@northeastern.edu",
        ["Country you have_will immigrate from"],
    ] = "Canada"
    df.loc[
        df["Username"] == "howladerony@gmail.com",
        ["Country you have_will immigrate from"],
    ] = "Bangladesh"
    df.loc[
        df["Username"] == "liujun02122023@163.com",
        ["Country you have_will immigrate from"],
    ] = "China"
    df.loc[
        df["Username"] == "danitacarrasco@hotmail.com",
        ["Country of birth", "Country you have_will immigrate from"],
    ] = "Chile"
    df.loc[
        df["Username"] == "feng.xiaom@northeastern.edu",
        ["Country of birth", "Country you have_will immigrate from"],
    ] = "China"
    df.loc[
        df["Username"] == "Rajindersingh090990@gmail.com",
        ["Country of birth", "Country you have_will immigrate from"],
    ] = "India"
    df.loc[
        df["Username"] == "howladerony@gmail.com",
        ["Country of birth", "Country you have_will immigrate from"],
    ] = "Bangladesh"

    # List of variations to be replaced with 'China'
    variations_to_replace = [
        "china",
        "CN",
        # "China, PeopleÂ’s Republic of",
        # "Chinia",
        "Hong Kong",
        "Hong Kong, China",
    ]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(variations_to_replace, "China")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(
        variations_to_replace, "China"
    )

    # Update 'Country you have_will immigrate from' column from 'Brasil' to 'Brazil'
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace("Euthiopia", "Ethiopia")

    df["Country of birth"] = df["Country of birth"].replace("Euthiopia", "Ethiopia")

    df["Country of birth"] = df["Country of birth"].replace("Hyderabad", "India")
    korea_variations = [
        "Korea",
        "South Korea",
        "Korea, Republic of",
        "Republic of Korea",
        "Korea South",
    ]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(korea_variations, "South Korea")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(
        korea_variations, "South Korea"
    )

    # List of variations to be replaced with 'South Korea'
    Ukraine_variations = [
        "Ukrainian",
        "Kyiv",
        "Ukrain",
        "Ikey",
        "Ukraine/Canada",
    ]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(Ukraine_variations, "Ukraine")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(
        Ukraine_variations, "Ukraine"
    )

    # List of variations to be replaced with 'South Korea'
    Canada_variations = [
        "British Columbia",
    ]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(Canada_variations, "Canada")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(Canada_variations, "Canada")

    # List of variations to be replaced with 'South Korea'
    Pakistan_variations = ["PAKISTAN", "Pakistani", "pakistan"]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(Pakistan_variations, "Pakistan")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(
        Pakistan_variations, "Pakistan"
    )

    # List of variations to be replaced with 'South Korea'
    Nigeria_variations = ["NIGERIA", "lagos", "Nigerian"]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(Nigeria_variations, "Nigeria")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(
        Nigeria_variations, "Nigeria"
    )
    # Update 'Country you have_will immigrate from' column from 'Brasil' to 'Brazil'
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace("North", "Iran")
    # Update 'Country you have_will immigrate from' column from 'Brasil' to 'Brazil'
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace("Rwanada", "Rwanda")
    # List of variations to be replaced with 'South Korea'
    Turkey_variations = ["turky", "turkiy"]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(Turkey_variations, "Turkey")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(Turkey_variations, "Turkey")
    # List of variations to be replaced with 'South Korea'
    UAE_variations = [
        "UEA",
        "UAE",
        "United Arab Emarites",
    ]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(UAE_variations, "United Arab Emirates")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(
        Nigeria_variations, "United Arab Emirates"
    )

    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace("US", "USA")
    # List of variations to be replaced with 'South Korea'
    afghanistan_variations = ["Afghanistan", "Afganistan", "Afghanistan"]

    # Update 'Country you have_will immigrate from' column
    df["Country you have_will immigrate from"] = df[
        "Country you have_will immigrate from"
    ].replace(afghanistan_variations, "Afghanistan")

    # Update 'Country of birth' column
    df["Country of birth"] = df["Country of birth"].replace(
        afghanistan_variations, "Afghanistan"
    )
    return df


def clean_signup(df: DataFrame):
    return df


def clean_exams(df: DataFrame):
    return df


def clean_eval(df: DataFrame):
    return df


def clean_survey(df: DataFrame):
    return df
