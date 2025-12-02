import os
from notion_client import Client
from config import NOTION_API_KEY

# Notion API クライアント作成
notion = Client(auth=NOTION_API_KEY)

# DB ID を環境変数から取得
COURSES_DB_ID = os.getenv("NOTION_DB_COURSES_ID")
LAYOUTS_DB_ID = os.getenv("NOTION_DB_LAYOUTS_ID")
HOLES_DB_ID = os.getenv("NOTION_DB_HOLES_ID")


# ------------------------------
# コース一覧取得
# ------------------------------
def get_courses():
    """
    courses DB の全コースを取得
    """
    results = []
    try:
        response = notion.databases.query(database_id=COURSES_DB_ID)
        for page in response.get("results", []):
            course = {
                "id": page["id"],
                "name": page["properties"]["name"]["title"][0]["plain_text"] if page["properties"]["name"]["title"] else "",
                "address": page["properties"]["address"]["rich_text"][0]["plain_text"] if page["properties"]["address"]["rich_text"] else "",
                "type": page["properties"]["type"]["select"]["name"] if page["properties"]["type"]["select"] else "",
                "par": page["properties"]["par"]["number"] if page["properties"]["par"]["number"] else 0,
            }
            results.append(course)
    except Exception as e:
        print("get_courses error:", e)
    return results


# ------------------------------
# コース詳細取得（layouts + holes）
# ------------------------------
def get_course_details(course_id):
    """
    layouts + holes を含めたコース詳細を取得
    """
    course_data = {}
    try:
        # layouts を取得
        layouts_response = notion.databases.query(
            database_id=LAYOUTS_DB_ID,
            filter={
                "property": "course",
                "relation": {
                    "contains": course_id
                }
            }
        )
        layouts = []
        for layout_page in layouts_response.get("results", []):
            layout_id = layout_page["id"]
            layout = {
                "id": layout_id,
                "layout_name": layout_page["properties"]["layout_name"]["title"][0]["plain_text"] if layout_page["properties"]["layout_name"]["title"] else "",
                "par": layout_page["properties"]["par"]["number"] if layout_page["properties"]["par"]["number"] else 0,
                "holes": []
            }

            # holes を取得
            holes_response = notion.databases.query(
                database_id=HOLES_DB_ID,
                filter={
                    "property": "layout",
                    "relation": {
                        "contains": layout_id
                    }
                }
            )
            holes_list = []
            for hole_page in holes_response.get("results", []):
                hole = {
                    "id": hole_page["id"],
                    "hole_number": hole_page["properties"]["hole_number"]["number"] if hole_page["properties"]["hole_number"]["number"] else 0,
                    "par": hole_page["properties"]["par"]["number"] if hole_page["properties"]["par"]["number"] else 0
                }
                holes_list.append(hole)

            # ホール番号でソート
            layout["holes"] = sorted(holes_list, key=lambda x: x["hole_number"])
            layouts.append(layout)

        course_data["layouts"] = layouts

    except Exception as e:
        print("get_course_details error:", e)

    return course_data
