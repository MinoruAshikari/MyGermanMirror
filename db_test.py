import sqlite3

# 1. 接続
conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# --- ここからが新しい魔法 ---

# 【UPDATE】データを書き換える
# 「名前がSaburoの人」を探して、国を「Germany」に書き換える
print("--- Saburoさんがドイツへ移住しました ---")
cursor.execute("UPDATE employees SET country = 'Germany' WHERE name = 'Saburo'")

# 【DELETE】データを消す
# 「名前がIchiroの人」を探して、その行を消す
print("--- Ichiroさんのデータを削除しました ---")
cursor.execute("DELETE FROM employees WHERE name = 'Ichiro'")

# 変更を確定する（これを忘れると反映されません！）
conn.commit()

# --- 結果確認 ---

# 全員を表示して、結果を見てみる
print("\n--- 最新の社員名簿 ---")
cursor.execute("SELECT * FROM employees")
results = cursor.fetchall()

for row in results:
    print(row)

# 後片付け
conn.close()