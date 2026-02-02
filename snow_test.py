import snowflake.connector

# 1. 接続設定（さっきと同じです）
conn = snowflake.connector.connect(
    user='MinoruAshikari',
    password='Minoru0520!!!!!',  # ←ここだけは誰にも見せない！
    account='AKBOOYJ-BU10291',
    database='DEMO_DB',          # Snowflakeに最初からある練習用DB
    schema='PUBLIC'
)

cursor = conn.cursor()

# 2. SQLの準備：テーブルを作る
# 倉庫の中に「candidates（候補者）」という棚を作ります
sql = """
CREATE TABLE IF NOT EXISTS candidates (
    id integer,
    name string,
    skill string,
    target_country string
)
"""

# 3. 実行！
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