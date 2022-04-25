import altair as alt
import boto3
import pandas as pd
import streamlit as st
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal

deserializer = TypeDeserializer()

st.title("Castle Vault Analytics")


def get_aws_credentials():
    return {
        "aws_access_key_id": st.secrets["AWS_ACCESS"],
        "aws_secret_access_key": st.secrets["AWS_SECRET"],
    }


# client = boto3.client("dynamodb", **get_aws_credentials())
dynamodb = boto3.resource("dynamodb", region_name="us-east-1", **get_aws_credentials())
table = dynamodb.Table("vault-history")

response = table.scan(
    FilterExpression=Attr("vaultId").eq("5zwJzQbw8PzNT2SwkhwrYfriVsLshytWk1UQkkudQv6G")
)
items = response["Items"]

df = pd.DataFrame(items)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["apy"] = [float(Decimal(a)) for a in df["apy"]]
df["value"] = [float(a) / 1000000000 for a in df["value"]]

st.altair_chart(
    alt.Chart(df)
    .mark_line()
    .encode(
        x="timestamp",
        y="apy",
    )
)

st.altair_chart(
    alt.Chart(df)
    .mark_line()
    .encode(
        x="timestamp",
        y="value",
    )
)

st.write(df)
