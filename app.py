import streamlit as st
import pandas as pd
from openai import OpenAI
import json

# ページ設定
st.set_page_config(page_title="MyGermanMirror 🇩🇪", layout="wide")
st.title("MyGermanMirror 🇩🇪 : 専属AIドイツ語コーチ")

# OpenAIクライアント
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# --- 関数1: 日記添削 & JSONデータ作成 ---
def correct_diary(diary_text):
    prompt = f"""
    あなたはドイツ語教師です。以下の日記を添削し、JSON形式で返してください。
    【日記】{diary_text}
    【出力形式】
    {{
        "correction": "修正後の全文",
        "explanation": "解説（日本語、箇条書き）",
        "vocab_list": [{{"german": "単語", "japanese": "意味", "level": "B1"}}]
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 関数2: 音声認識 (Whisper) & 発音判定 ---
def analyze_speech(audio_file, target_text):
    # 1. Whisperで文字起こし（耳で聞く）
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    heard_text = transcript.text

    # 2. GPTで発音判定（頭で考える）
    prompt = f"""
    ユーザーは「{target_text}」と言おうとしました。
    しかし、AIの耳には「{heard_text}」と聞こえました。
    
    以下の評価をJSONで行ってください。
    {{
        "score": "100点満点中の点数（整数）",
        "advice": "発音のアドバイス（日本語）",
        "heard": "AIに聞こえた言葉"
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# ==========================================
# 画面レイアウト（タブで機能を分ける）
# ==========================================
tab1, tab2 = st.tabs(["📝 書く (Schreiben)", "🎙️ 話す (Sprechen)"])

# --- タブ1: 日記添削 ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("日記を書く")
        diary_input = st.text_area("ドイツ語日記を入力", height=200)
        if st.button("添削開始 🚀", key="btn_diary"):
            if diary_input:
                with st.spinner("AI先生が添削中..."):
                    res = correct_diary(diary_input)
                    st.session_state["diary_result"] = json.loads(res)
    
    with col2:
        st.subheader("フィードバック")
        if "diary_result" in st.session_state:
            data = st.session_state["diary_result"]
            st.success(f"✅ 修正: {data['correction']}")
            st.info(f"👨‍🏫 解説: {data['explanation']}")
            # CSVダウンロード
            df = pd.DataFrame(data['vocab_list'])
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 単語帳CSVを保存", csv, "vocab.csv", "text/csv")

# --- タブ2: スピーキング練習 ---
with tab2:
    st.subheader("発音チェック道場")
    st.caption("指定されたドイツ語を読み上げてください。AIがあなたの発音を採点します！")

    # お題の例
    target_text = st.text_input("読み上げる文章（自分でお題を決めてOK）", value="Guten Tag! Ich möchte bitte einen Kaffee.")
    
    # 録音ボタン（Streamlitの最新機能！）
    audio_value = st.audio_input("マイクに向かって話してください 🎤")

    if audio_value:
        st.audio(audio_value) # 自分の声を確認
        
        if st.button("採点する 💯"):
            with st.spinner("AIがあなたの声を解析中...👂"):
                # Whisper評価の実行
                res_speech = analyze_speech(audio_value, target_text)
                speech_data = json.loads(res_speech)
                
                # 結果発表
                score = int(speech_data["score"])
                st.metric("発音スコア", f"{score}点")
                
                if score >= 80:
                    st.balloons() # 80点以上なら風船が飛ぶ！🎈
                    st.success(f"👏 AIにはこう聞こえました: 「{speech_data['heard']}」")
                else:
                    st.error(f"👂 AIにはこう聞こえました: 「{speech_data['heard']}」")
                
                st.write(f"💡 アドバイス: {speech_data['advice']}")