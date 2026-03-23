import pymysql
import os

# Database connection details
DB_CONFIG = {
    'host': '127.0.0.1', # 로컬 터널링 기준
    'port': 3307,
    'user': 'admin',
    'password': 'mysql_password', # 실제 비밀번호는 환경 변수에서 가져오는 것이 좋으나, 
                                  # 여기서는 기존 스크립트의 패턴을 따릅니다.
    'db': 'hisubtory_db',
    'charset': 'utf8mb4'
}

def clean_duplicates():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            print("중복된 장면(Cut) 데이터를 조회 중입니다...")
            
            # 중복된 (episode_id, cut_order) 쌍을 찾아 가장 작은 cut_id만 남기고 나머지를 삭제하는 SQL
            # MySQL에서는 자기 자신을 참조하며 삭제할 수 없으므로 서브쿼리를 사용합니다.
            
            sql_find = """
                SELECT episode_id, cut_order, COUNT(*) 
                FROM cuts 
                GROUP BY episode_id, cut_order 
                HAVING COUNT(*) > 1
            """
            cursor.execute(sql_find)
            duplicates = cursor.fetchall()
            
            if not duplicates:
                print("중복된 데이터가 없습니다.")
                return

            print(f"발견된 중복 세트: {len(duplicates)}개")
            
            sql_delete = """
                DELETE FROM cuts 
                WHERE cut_id NOT IN (
                    SELECT min_id FROM (
                        SELECT MIN(cut_id) AS min_id 
                        FROM cuts 
                        GROUP BY episode_id, cut_order
                    ) AS t
                )
            """
            cursor.execute(sql_delete)
            affected_rows = cursor.rowcount
            
            conn.commit()
            print(f"성공: 총 {affected_rows}개의 중복 장면 데이터가 삭제되었습니다.")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clean_duplicates()
