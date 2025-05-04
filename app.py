import streamlit as st
import openai
import os
from audio_recorder_streamlit import audio_recorder
import io
import time
import pandas as pd
import plotly.express as px
from datetime import datetime

# OpenAI APIキーの設定
openai.api_key = st.secrets["OPENAI_API_KEY"]

# セッション状態の初期化
if 'practice_history' not in st.session_state:
    st.session_state.practice_history = []

# 高校情報の定義
schools = {
    "都立高校": {
        "特徴": "都立高校は、東京都が運営する公立高校です。一般的に学力重視の傾向があり、進学実績が高い学校が多いです。",
        "よくある質問": [
            "都立高校を志望する理由は？",
            "都立高校の特色について知っていることは？",
            "都立高校での学習計画は？",
            "都立高校の部活動について興味のあるものは？",
            "都立高校の進学実績についてどう思いますか？"
        ]
    },
    "私立高校": {
        "特徴": "私立高校は、学校法人が運営する高校です。独自の教育方針や特色があり、施設や設備が充実していることが多いです。",
        "よくある質問": [
            "私立高校を志望する理由は？",
            "本校の教育方針についてどう思いますか？",
            "私立高校の学費についてどう考えていますか？",
            "本校の特色ある教育プログラムについて知っていることは？",
            "私立高校での学校生活についてどのように考えていますか？"
        ]
    },
    "中高一貫校": {
        "特徴": "中高一貫校は、中学校と高校が一貫した教育を行う学校です。6年間の一貫した教育プログラムが特徴です。",
        "よくある質問": [
            "中高一貫校を志望する理由は？",
            "6年間の一貫教育についてどう思いますか？",
            "中高一貫校での学習計画は？",
            "中高一貫校のメリットについてどう考えていますか？",
            "中高一貫校での学校生活についてどのように考えていますか？"
        ]
    }
}
# ページ設定
st.set_page_config(
    page_title="高校受験面接練習アプリ",
    page_icon="🎓",
    layout="wide"
)

# タイトル
st.title("高校受験面接練習アプリ")
st.markdown("AIと一緒に面接練習をしましょう！")

# サイドバー
with st.sidebar:
    st.header("面接モード選択")
    mode = st.radio(
        "練習モードを選択してください",
        ["自由練習", "よくある質問", "フィードバック", "模擬面接", "高校別練習", "練習記録"]
    )
    
    # タイマー設定
    if mode in ["模擬面接", "高校別練習"]:
        st.header("タイマー設定")
        timer_minutes = st.slider("面接時間（分）", 1, 30, 10)
        if st.button("タイマー開始"):
            st.session_state.start_time = time.time()
            st.session_state.timer_running = True

# メインコンテンツ
if mode == "自由練習":
    st.header("自由練習モード")
    user_input = st.text_area("面接官の質問を入力してください", height=100)
    if st.button("回答を生成"):
        if user_input:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは高校受験の面接官です。受験生の回答に対して、建設的なフィードバックを提供してください。"},
                    {"role": "user", "content": user_input}
                ]
            )
            st.write("AI面接官からの回答：")
            st.write(response.choices[0].message.content)
            
            # 練習記録の保存
            st.session_state.practice_history.append({
                "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "モード": "自由練習",
                "質問": user_input,
                "回答": response.choices[0].message.content
            })
          elif mode == "よくある質問":
    st.header("よくある質問")
    questions = [
        "志望動機を教えてください",
        "将来の夢は何ですか？",
        "この学校を選んだ理由は？",
        "部活動は何をしたいですか？",
        "得意な科目と苦手な科目は？"
    ]
    
    selected_question = st.selectbox("質問を選択してください", questions)
    if st.button("模範解答を表示"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは高校受験の面接官です。選ばれた質問に対する模範解答を提供してください。"},
                {"role": "user", "content": selected_question}
            ]
        )
        st.write("模範解答：")
        st.write(response.choices[0].message.content)
        
        # 練習記録の保存
        st.session_state.practice_history.append({
            "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "モード": "よくある質問",
            "質問": selected_question,
            "回答": response.choices[0].message.content
        })

elif mode == "フィードバック":
    st.header("フィードバックモード")
    user_answer = st.text_area("あなたの回答を入力してください", height=150)
    if st.button("フィードバックを取得"):
        if user_answer:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは高校受験の面接官です。受験生の回答に対して、具体的な改善点とアドバイスを提供してください。"},
                    {"role": "user", "content": user_answer}
                ]
            )
            st.write("フィードバック：")
            st.write(response.choices[0].message.content)
            
            # 練習記録の保存
            st.session_state.practice_history.append({
                "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "モード": "フィードバック",
                "回答": user_answer,
                "フィードバック": response.choices[0].message.content
            })
          elif mode == "模擬面接":
    st.header("模擬面接モード")
    
    # タイマー表示
    if 'timer_running' in st.session_state and st.session_state.timer_running:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = timer_minutes * 60 - elapsed_time
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.write(f"残り時間: {minutes}分{seconds}秒")
        else:
            st.session_state.timer_running = False
            st.write("時間切れです！")
    
    # 音声録音
    st.write("回答を録音してください：")
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        # 音声をテキストに変換（OpenAI Whisper APIを使用）
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "recording.wav"
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        
        st.write("録音内容：")
        st.write(transcript["text"])
        
        # フィードバック生成
        if st.button("フィードバックを取得"):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは高校受験の面接官です。受験生の回答に対して、具体的な改善点とアドバイスを提供してください。"},
                    {"role": "user", "content": transcript["text"]}
                ]
            )
            st.write("フィードバック：")
            st.write(response.choices[0].message.content)
            
            # 練習記録の保存
            st.session_state.practice_history.append({
                "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "モード": "模擬面接",
                "回答": transcript["text"],
                "フィードバック": response.choices[0].message.content
            })
          elif mode == "高校別練習":
    st.header("高校別練習モード")
    
    # 高校選択
    selected_school = st.selectbox("高校の種類を選択してください", list(schools.keys()))
    
    # 高校情報の表示
    st.subheader(f"{selected_school}の特徴")
    st.write(schools[selected_school]["特徴"])
    
    # タイマー表示
    if 'timer_running' in st.session_state and st.session_state.timer_running:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = timer_minutes * 60 - elapsed_time
        if remaining_time > 0:
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.write(f"残り時間: {minutes}分{seconds}秒")
        else:
            st.session_state.timer_running = False
            st.write("時間切れです！")
    
    # 高校別の質問選択
    st.subheader("質問を選択してください")
    selected_question = st.selectbox("質問を選択", schools[selected_school]["よくある質問"])
    
    # 音声録音
    st.write("回答を録音してください：")
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        
        # 音声をテキストに変換
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "recording.wav"
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        
        st.write("録音内容：")
        st.write(transcript["text"])
        
        # フィードバック生成
        if st.button("フィードバックを取得"):
            system_prompt = f"あなたは{selected_school}の面接官です。受験生の回答に対して、{selected_school}の特色を考慮した具体的な改善点とアドバイスを提供してください。"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript["text"]}
                ]
            )
            st.write("フィードバック：")
            st.write(response.choices[0].message.content)
            
            # 練習記録の保存
            st.session_state.practice_history.append({
                "日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "モード": "高校別練習",
                "高校": selected_school,
                "質問": selected_question,
                "回答": transcript["text"],
                "フィードバック": response.choices[0].message.content
            })

else:  # 練習記録モード
    st.header("練習記録")
    
    if st.session_state.practice_history:
        # データフレームの作成
        df = pd.DataFrame(st.session_state.practice_history)
        
        # 練習回数のグラフ
        st.subheader("練習回数の推移")
        practice_counts = df.groupby('モード').size().reset_index(name='回数')
        fig = px.bar(practice_counts, x='モード', y='回数', title='モード別練習回数')
        st.plotly_chart(fig)
        
        # 練習記録の表示
        st.subheader("練習記録一覧")
        st.dataframe(df)
        
        # 記録のエクスポート
        if st.button("記録をエクスポート"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="CSVファイルをダウンロード",
                data=csv,
                file_name="practice_history.csv",
                mime="text/csv"
            )
    else:
        st.write("まだ練習記録がありません。")
      
