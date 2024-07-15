from io import StringIO
import os
import boto3
from botocore.exceptions import ClientError
from pandas import DataFrame, concat, read_csv
from functools import lru_cache
import time
from googletrans import Translator as GoogleTranslator
from translation_config import (
    fix_column_translate,
    fix_duplicate_columns,
    columns_to_be_translated,
)

translator = GoogleTranslator()
translator.raise_Exception = True
DATA_BUCKET = os.getenv("DATA_BUCKET")
s3_resource = boto3.resource("s3")
TRANSLATION_CSV_KEY = "translations.csv"


@lru_cache
def translate(text):
    if not text or type(text) != str or not text.strip():
        return text
    try:
        translation = translator.translate(text, dest="en")
    except Exception as e:
        print(e)
        if e.args[0] == "Unexpected status code \"429\" from ('translate.google.com',)":
            time.sleep(60)
            return translate(text)
        raise e
    return translation.text


class Translator:
    df: DataFrame

    def __init__(self) -> None:

        self.df = DataFrame(
            [
                {"input": "Homme", "output": "Male"},
                {"input": "Femme", "output": "Female"},
                {"input": "Oui", "output": "Yes"},
                {"input": "Non", "output": "No"},
                {"input": "Genre", "output": "Gender"},
                {"input": "Statut au Canada", "output": "Status in Canada"},
            ]
        )
        # if translations cached in s3 load csv from there else upload csv
        self._get_df_from_csv()

    def _save_df_to_csv(self):
        csv_buffer = StringIO(self.df.to_csv(index=False))
        s3_resource.Object(DATA_BUCKET, TRANSLATION_CSV_KEY).put(
            Body=csv_buffer.getvalue()
        )

    def _get_df_from_csv(self):
        try:
            s3_resource.Object(DATA_BUCKET, TRANSLATION_CSV_KEY).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self._save_df_to_csv()
            else:
                # Something else has gone wrong.
                raise e
        else:
            s3_object = s3_resource.Object(DATA_BUCKET, TRANSLATION_CSV_KEY)
            file_body = s3_object.get()["Body"]
            string_content = file_body.read().decode("utf-8")
            self.df = read_csv(StringIO(string_content), encoding="utf-8")

    # @lru_cache
    def fetch_translation(self, input):
        if not input or type(input) != str:
            return input
        result = self.df.loc[self.df["input"] == input]
        if result.values.size > 0:
            return result["output"][result.index[0]]
        self.df = concat(
            [self.df, DataFrame([{"input": input, "output": translate(input)}])],
            ignore_index=True,
        )
        self._save_df_to_csv()
        return self.fetch_translation(input)


def _copy_values_between_cols(df: DataFrame, drop_col: str, keep_col: str):
    if drop_col not in df:
        return False
    if keep_col not in df:
        df.loc[:, keep_col] = df[drop_col]
    df.loc[:, keep_col] = df[keep_col].fillna(df[drop_col])
    df.loc[:, drop_col] = df[drop_col].fillna(df[keep_col])
    df.loc[:, keep_col] = df[drop_col]
    return True


def translate_columns(df: DataFrame):
    translator_obj = Translator()
    french_cols = {}
    for col in df.columns.to_list():
        translated_text = translator_obj.fetch_translation(col)
        if translated_text != col:
            french_cols.update({col: translated_text})
    columns_to_drop = []
    for french_col, english_col in french_cols.items():
        new_col_name = fix_column_translate.get(english_col, english_col)
        if _copy_values_between_cols(df, drop_col=french_col, keep_col=new_col_name):
            columns_to_drop.append(french_col)
    for drop_col, keep_col in fix_duplicate_columns.items():
        if _copy_values_between_cols(df, drop_col=drop_col, keep_col=keep_col):
            columns_to_drop.append(drop_col)
    new_columns = [col for col in df.columns if col not in columns_to_drop]
    df = df[new_columns]
    return df


def translate_rows(df: DataFrame):
    translator_obj = Translator()
    for index, row in df.iterrows():
        for column in columns_to_be_translated:
            if column in row:
                df.at[index, column] = translator_obj.fetch_translation(
                    df.at[index, column]
                )
    return df
