import sqlite3

# 1. データベース（ファイル）に接続
conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# 2. テーブル（表）を作る呪文
# もし既にあったらエラーにならないように IF NOT EXISTS をつけています
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        country TEXT
    )
''')

# 3. 【INSERT】データを入れる呪文
# あなたのデータを入れます
cursor.execute("INSERT INTO employees (name, country) VALUES ('Takiba Shacho', 'Malaysia')")
cursor.execute("INSERT INTO employees (name, country) VALUES ('Tanaka', 'Japan')")

# 変更を確定する（コミットと言います）
conn.commit()

# 4. 【SELECT】データを読む呪文
# 「countryがMalaysiaの人」だけを探して連れてきます
cursor.execute("SELECT * FROM employees WHERE country = 'Malaysia'")

# 結果を受け取る
results = cursor.fetchall()

print("--- 検索結果 ---")
for row in results:
    print(row)

# 後始末
conn.close()