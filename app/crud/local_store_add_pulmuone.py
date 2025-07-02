import pandas as pd
from app.db.connect import (
    get_db_connection,
    close_connection,
    close_cursor,
    commit,
    rollback,
)
import pymysql

DEFAULT_STORE_DATA = {
    "REFERENCE_ID": 3,
    "LARGE_CATEGORY_CODE": "G2",
    "LARGE_CATEGORY_NAME": "소매",
    "MEDIUM_CATEGORY_CODE": "G206",
    "MEDIUM_CATEGORY_NAME": "음료 소매",
    "SMALL_CATEGORY_CODE": "G20603",
    "SMALL_CATEGORY_NAME": "생수/음료 소매업",
    "INDUSTRY_CODE": "G47221",
    "INDUSTRY_NAME": "음료 소매업",
    "LOCAL_YEAR": 2024,
    "LOCAL_QUARTER": 4,
    "IS_EXIST": 1,
    "ktmyshop": 0,
    "jsam": 0,
    "PULMUONE": 1
}

def insert_local_store(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        insert_query = """
        INSERT INTO local_store (
            CITY_ID, DISTRICT_ID, SUB_DISTRICT_ID,
            REFERENCE_ID, STORE_BUSINESS_NUMBER, STORE_NAME,
            LARGE_CATEGORY_CODE, LARGE_CATEGORY_NAME,
            MEDIUM_CATEGORY_CODE, MEDIUM_CATEGORY_NAME,
            SMALL_CATEGORY_CODE, SMALL_CATEGORY_NAME,
            INDUSTRY_CODE, INDUSTRY_NAME,
            ROAD_NAME_ADDRESS, LONGITUDE, LATITUDE,
            LOCAL_YEAR, LOCAL_QUARTER,
            IS_EXIST, ktmyshop, jsam, PULMUONE
        ) VALUES (
            %(CITY_ID)s, %(DISTRICT_ID)s, %(SUB_DISTRICT_ID)s,
            %(REFERENCE_ID)s, %(STORE_BUSINESS_NUMBER)s, %(STORE_NAME)s,
            %(LARGE_CATEGORY_CODE)s, %(LARGE_CATEGORY_NAME)s,
            %(MEDIUM_CATEGORY_CODE)s, %(MEDIUM_CATEGORY_NAME)s,
            %(SMALL_CATEGORY_CODE)s, %(SMALL_CATEGORY_NAME)s,
            %(INDUSTRY_CODE)s, %(INDUSTRY_NAME)s,
            %(ROAD_NAME_ADDRESS)s, %(LONGITUDE)s, %(LATITUDE)s,
            %(LOCAL_YEAR)s, %(LOCAL_QUARTER)s,
            %(IS_EXIST)s, %(ktmyshop)s, %(jsam)s, %(PULMUONE)s
        )
        """
        cursor.execute(insert_query, data)
        commit(conn)
        print(f"[OK] {data['ROAD_NAME_ADDRESS']} 삽입 완료")
    except pymysql.MySQLError as e:
        rollback(conn)
        print(f"[ERROR] {data['ROAD_NAME_ADDRESS']} - {e}")
    finally:
        close_cursor(cursor)
        close_connection(conn)

if __name__ == "__main__":
    # # 엑셀 파일 경로 지정 및 불러오기 (현재 주석 처리)
    # excel_path = r"C:\Users\jyes_semin\Desktop\PUL.xlsx"
    # df = pd.read_excel(excel_path)
    #
    # for _, row in df.iterrows():
    #     variable_data = {
    #         "CITY_ID": row["CITY_ID"],
    #         "DISTRICT_ID": row["DISTRICT_ID"],
    #         "SUB_DISTRICT_ID": row["SUB_DISTRICT_ID"],
    #         "STORE_BUSINESS_NUMBER": row["STORE_BUSINESS_NUMBER"],
    #         "STORE_NAME": row["STORE_NAME"],
    #         "ROAD_NAME_ADDRESS": row["ROAD_NAME_ADDRESS"],
    #         "LONGITUDE": str(row["LONGITUDE"]),
    #         "LATITUDE": str(row["LATITUDE"])
    #     }
    #     store_data = {**DEFAULT_STORE_DATA, **variable_data}
    #     insert_local_store(store_data)

    # ✅ 직접 입력해서 테스트용 데이터 삽입
    variable_data = {
        "CITY_ID": 9,
        "DISTRICT_ID": 139,
        "SUB_DISTRICT_ID": 2186,
        "STORE_BUSINESS_NUMBER": "JS0050",
        "STORE_NAME": "이례유통",
        "ROAD_NAME_ADDRESS": "서울시 서초구 효령로34길 62",
        "LONGITUDE": "127.000631089558",
        "LATITUDE": "37.4789984677988 "
    }
    store_data = {**DEFAULT_STORE_DATA, **variable_data}
    insert_local_store(store_data)

