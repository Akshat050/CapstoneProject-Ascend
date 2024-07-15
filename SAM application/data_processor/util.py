from io import StringIO
from typing import Optional, Tuple
from urllib.parse import unquote_plus
import boto3
from pandas import DataFrame, read_csv
from config import ANSI_ENCODING, DATA_BUCKET

s3_resource = boto3.resource("s3")
DATA_TYPE = ["signup", "exams", "eval", "survey"]


def put_df_in_s3(df: DataFrame, object_key: str):
    csv_buffer = StringIO(df.to_csv(index=False))
    s3_resource.Object(DATA_BUCKET, object_key).put(Body=csv_buffer.getvalue())
    return object_key


def get_df_from_s3(
    object_key: str,
    bucket: str = DATA_BUCKET,
    encoding: str = "utf-8",
) -> DataFrame:
    print(f"getting {object_key} object from {bucket} bucket")
    s3_object = s3_resource.Object(bucket, object_key)
    file_body = s3_object.get()["Body"]
    string_content = file_body.read().decode(encoding)
    return read_csv(
        StringIO(string_content),
        dtype=str,
        encoding=encoding,
    )


def get_csv_file_from_s3(
    bucket: str, key: str
) -> Tuple[Optional[str], Optional[DataFrame]]:
    key = unquote_plus(key)
    data_type = get_data_type_from_file_path(key)
    print(f"data_type: {data_type}")
    if data_type and key.endswith(".csv"):
        encoding = ANSI_ENCODING if data_type == "signup" else "utf-8"
        print(f"update encoding {encoding}")
        df = get_df_from_s3(key, bucket, encoding)
        # remove trailing spaces
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return data_type, df
    return None, None


def get_data_type_from_file_path(file_path: str) -> Optional[str]:
    for data_type in DATA_TYPE:
        if data_type in file_path.lower():
            return data_type
    return None
