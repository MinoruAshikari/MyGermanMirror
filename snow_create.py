import snowflake.connector

# 1. 接続設定
conn = snowflake.connector.connect(
    user='MinoruAshikari',
    password='Minoru0520!!!!!',
    account='AKBOOYJ-BU10291',
    warehouse='COMPUTE_WH'       # 計算機（ウェアハウス）も念のため指定
)

cursor = conn.cursor()

# 2. 【重要】ここが変わりました！
# まず「python_db」という名前のデータベース（箱）を作ります
print("--- データベース（箱）を作成・選択中... ---")
cursor.execute("CREATE DATABASE IF NOT EXISTS python_db")
cursor.execute("USE DATABASE python_db")

# 3. テーブルを作る
# その箱の中に「candidates（候補者）」というファイルを作ります
sql = """
CREATE TABLE IF NOT EXISTS candidates (
    id integer,
    name string,
    skill string,
    target_country string
)
"""

print("--- シンガポールにテーブルを作成中... ---")
cursor.execute(sql)
print("成功！テーブル 'candidates' が作成されました。")

# 4. データを1つ入れてみる
cursor.execute("INSERT INTO candidates VALUES (1, 'Takiba Shacho', 'Python', 'Germany')")
print("データ入力完了：焚き火社長を登録しました。")

# 5. 後片付け
conn.commit() # 変更を確定
cursor.close()
conn.close()