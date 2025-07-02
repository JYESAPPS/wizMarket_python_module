import pandas as pd
from app.db.connect import (
    get_db_connection,
    close_connection,
    close_cursor,
    commit,
    rollback,
)
import pymysql

def update_local_store(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_query = """
            UPDATE LOCAL_STORE
            SET SMALL_CATEGORY_CODE = %(SMALL_CATEGORY_CODE)s,
                SMALL_CATEGORY_NAME = %(SMALL_CATEGORY_NAME)s
            WHERE STORE_BUSINESS_NUMBER = %(STORE_BUSINESS_NUMBER)s
        """
        cursor.execute(update_query, data)
        commit(conn)
        print(f"[OK] 업데이트 완료: {data['STORE_BUSINESS_NUMBER']}")
    except pymysql.MySQLError as e:
        rollback(conn)
        print(f"[ERROR] {e}")
    finally:
        close_cursor(cursor)
        close_connection(conn)

EXCEL_PATH = r"C:\Users\jyes_semin\Desktop\add_image.xlsx"

df = pd.read_excel(EXCEL_PATH)

for _, row in df.iterrows():
    data = {
        "STORE_BUSINESS_NUMBER": row["STORE_BUSINESS_NUMBER"],
        "SMALL_CATEGORY_CODE": "G20605",
        "SMALL_CATEGORY_NAME": "녹즙 소매업",
    }
    update_local_store(data)
