from pandas import DataFrame
from sqlalchemy import create_engine
from config import MYSQL_URL

mysql_engine = create_engine(MYSQL_URL, echo=False) if MYSQL_URL else None


def save_df_to_sql(table_name: str, df: DataFrame):
    if mysql_engine:
        df.to_sql(name=table_name, con=mysql_engine, index=False, if_exists="append")
