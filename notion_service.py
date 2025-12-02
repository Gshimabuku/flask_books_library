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
        response = notion.databases.query(
            **{
                "database_id": NOTION_DB_COURSES_ID
            }
        )

        for page in response.get("results", []):
            properties = page["properties"]

            course = {
                "id": page["id"],
                "name": properties["name"]["title"][0]["plain_text"]
                if properties["name"]["title"] else "",

                "address": properties["address"]["rich_text"][0]["plain_text"]
                if properties["address"]["rich_text"] else "",

                "type": properties["type"]["select"]["name"]
                if properties["type"]["select"] else "",

                "par": properties["par"]["number"]
                if properties["par"]["number"] else 0,
            }

            results.append(course)

    except Exception as e:
        print("get_courses error:", e)

    return results
