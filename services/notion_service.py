import os
from notion_client import Client
from config import NOTION_API_KEY, NOTION_DB_COURSES_ID

# Notion クライアント
notion = Client(auth=NOTION_API_KEY)

# ---------------------------------
# コース一覧取得（最小）
# ---------------------------------
def get_courses():
    results = []

    try:
        data = fetch_db_properties(NOTION_DB_COURSES_ID)
        results = data
        # response = notion.databases.query(
        #     **{
        #         "database_id": NOTION_DB_COURSES_ID
        #     }
        # )

        # for page in response.get("results", []):
        #     properties = page["properties"]

        #     course = {
        #         "id": page["id"],
        #         "name": properties["name"]["title"][0]["plain_text"]
        #         if properties["name"]["title"] else "",

        #         "address": properties["address"]["rich_text"][0]["plain_text"]
        #         if properties["address"]["rich_text"] else "",

        #         "type": properties["type"]["select"]["name"]
        #         if properties["type"]["select"] else "",

        #         "par": properties["par"]["number"]
        #         if properties["par"]["number"] else 0,
        #     }

        #     results.append(course)

    except Exception as e:
        print("get_courses error:", e)

    return results

def get_property_value(prop):
    type_ = prop["type"]
    if type_ == "title":
        return prop["title"][0]["plain_text"] if prop["title"] else ""
    if type_ == "rich_text":
        return prop["rich_text"][0]["plain_text"] if prop["rich_text"] else ""
    if type_ == "number":
        return prop["number"]
    if type_ == "select":
        return prop["select"]["name"] if prop["select"] else None
    if type_ == "multi_select":
        return [v["name"] for v in prop["multi_select"]]
    if type_ == "checkbox":
        return prop["checkbox"]
    if type_ == "date":
        return prop["date"]["start"] if prop["date"] else None
    if type_ == "url":
        return prop["url"]
    if type_ == "email":
        return prop["email"]
    if type_ == "phone_number":
        return prop["phone_number"]
    if type_ == "files":
        return [f["file"]["url"] for f in prop["files"] if f["type"]=="file"]
    if type_ == "relation":
        return [r["id"] for r in prop["relation"]]
    if type_ == "rollup":
        roll_type = prop["rollup"]["type"]
        return prop["rollup"][roll_type]
    if type_ == "people":
        return [p["name"] for p in prop["people"]]
    if type_ == "formula":
        formula_type = prop["formula"]["type"]
        return prop["formula"][formula_type]
    if type_ == "created_time":
        return prop["created_time"]
    if type_ == "last_edited_time":
        return prop["last_edited_time"]
    return None

def fetch_db_properties(database_id: str, column_names: list = None):
    """
    指定 DB のデータを取得。
    column_names が None の場合は全カラム取得
    """
    results = notion.databases.query(database_id=database_id)["results"]
    data_list = []

    for page in results:
        props = page["properties"]

        # column_names が None なら全カラム取得
        if column_names is None:
            cols_to_fetch = list(props.keys())
        else:
            cols_to_fetch = column_names

        item = {}
        for col in cols_to_fetch:
            if col in props:
                item[col] = get_property_value(props[col])
            else:
                item[col] = None  # カラムが存在しない場合は None
        data_list.append(item)

    return data_list
