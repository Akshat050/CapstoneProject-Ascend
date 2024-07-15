import json
import boto3
from datetime import datetime
from config import DATA_PROCESSOR_STEP_FN
from data_cleaner import clean_data, fill_nas
from db import save_df_to_sql
from translations import translate_columns, translate_rows
from util import (
    get_csv_file_from_s3,
    get_data_type_from_file_path,
    get_df_from_s3,
    put_df_in_s3,
)

sfn_client = boto3.client("stepfunctions")


def csv_reciever(event, context):
    """Lambda triggered on s3 upload starts step function executions"""
    print(json.dumps(event))
    records = event["Records"]
    response = {}
    for item in records:
        data_type, df = get_csv_file_from_s3(
            bucket=item["s3"]["bucket"]["name"],
            key=item["s3"]["object"]["key"],
        )
        execution_id = f"{datetime.now():%Y_%m_%d_%H_%M_%S_%f}"
        object_key = f"{data_type}/{execution_id}/step_1.csv"
        response["df_csv"] = put_df_in_s3(df, object_key)
        response["data_snippet_json"] = json.loads(df.head().to_json(orient="records"))
        sfn_client.start_execution(
            stateMachineArn=DATA_PROCESSOR_STEP_FN,
            name=f"{data_type}_{execution_id}",
            input=json.dumps(response),
        )
    return response


def remove_test_users(event, context):
    df_csv: str = event.get("df_csv")
    execution_folder = "/".join(df_csv.split("/")[:-1])
    df = get_df_from_s3(df_csv)
    df = df[
        ~df["Username"].str.contains("test|proton|demo|@ascend", case=False, na=False)
    ]
    df = df[~df["Program Version"].str.contains("Facilitator", case=False, na=False)]
    if "DepartmentName" in df:
        df = df[~df["DepartmentName"].str.contains("Facilitator", case=False, na=False)]
    df.reset_index(drop=True, inplace=True)
    result_csv = f"{execution_folder}/step_2.csv"
    event["df_csv"] = put_df_in_s3(df, result_csv)
    event["data_snippet_json"] = json.loads(df.head().to_json(orient="records"))
    return event


def translate_french_data_columns(event, context):
    df_csv: str = event.get("df_csv")
    execution_folder = "/".join(df_csv.split("/")[:-1])
    df = translate_columns(get_df_from_s3(df_csv))
    result_csv = f"{execution_folder}/step_3.csv"
    event["df_csv"] = put_df_in_s3(df, result_csv)
    event["data_snippet_json"] = json.loads(df.head().to_json(orient="records"))
    return event


def translate_french_data_rows(event, context):
    df_csv: str = event.get("df_csv")
    execution_folder = "/".join(df_csv.split("/")[:-1])
    df = translate_rows(get_df_from_s3(df_csv))
    result_csv = f"{execution_folder}/step_4.csv"
    event["df_csv"] = put_df_in_s3(df, result_csv)
    event["data_snippet_json"] = json.loads(df.head().to_json(orient="records"))
    return event


def cleanup_data(event, context):
    df_csv: str = event.get("df_csv")
    execution_folder = "/".join(df_csv.split("/")[:-1])
    df = get_df_from_s3(df_csv)
    data_type = get_data_type_from_file_path(df_csv)
    df = clean_data(df, data_type)
    result_csv = f"{execution_folder}/step_5.csv"
    event["df_csv"] = put_df_in_s3(df, result_csv)
    event["data_snippet_json"] = json.loads(df.head().to_json(orient="records"))
    return event


def put_data_in_db(event, context):
    df_csv: str = event.get("df_csv")
    df = get_df_from_s3(df_csv)
    df = fill_nas(df)
    table_name = get_data_type_from_file_path(df_csv)
    save_df_to_sql(table_name, df)
    return event
