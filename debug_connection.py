import streamlit as st
import snowflake.connector

st.title("🕵️‍♂️ 犯人探し：Snowflake接続テスト")

# --- 実験1: 秘密のファイルが読めるか？ ---
st.write("Step 1: 秘密の鍵（secrets.toml）を確認中...")

try:
    # ユーザー名だけチラ見してみる
    user_check = st.secrets["snowflake"]["user"]
    st.success(f"✅ 成功！鍵ファイルを発見しました。ユーザー名: {user_check}")
except Exception as e:
    st.error(f"❌ 失敗！鍵ファイルが見つかりません: {e}")
    st.stop() # ここで強制終了

# --- 実験2: Snowflakeに繋がるか？ ---
st.write("Step 2: シンガポールのSnowflakeに電話しています...（応答待ち）")

try:
    # 実際に接続を試みる
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    st.success("✅ 大成功！！Snowflakeと繋がりました！犯人はAPI側かもしれません。")
    conn.close()
except Exception as e:
    st.error("❌ 接続失敗！ここで止まっています。")
    st.error(f"エラー内容: {e}")