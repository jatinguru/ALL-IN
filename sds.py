import streamlit as st
import pandas as pd
from textblob import TextBlob
from datetime import datetime
import matplotlib.pyplot as plt

# 🧠 Set page title and layout
st.set_page_config(page_title="All In", layout="centered")

# 🖼️ Header Style and Description
st.markdown("""
<style>
    .title {
        font-size: 45px;
        font-weight: 900;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: -10px;
    }
    .subtitle {
        text-align: center;
        font-style: italic;
        font-size: 18px;
        color: #AAAAAA;
    }
    .story-box {
        background-color: #1e1e1e;
        border-left: 5px solid #FF4B4B;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 10px;
    }
</style>

<div class="title">♠️ ALL IN</div>
<div class="subtitle">Confess. Rant. Reveal. Say everything you never dared.</div>

---

Welcome to **All In** — a raw, anonymous space where:
- 🎭 You can reveal who you *really* are (or not)
- 🧠 Your emotions are analyzed — without judgment
- 📊 Your words help paint a real-time picture of collective mental energy

**Type it. Feel it. Drop it.**  
No likes. No filters. Just **go All In**.
""", unsafe_allow_html=True)

# 📝 Input Fields
pseudonym = st.text_input("Choose a pseudonym (optional):")
story = st.text_area("Write your story or thought below:")

# 🏷️ Tone selection dropdown
tone = st.selectbox(
    "How would you describe your post?",
    ["Wholesome", "Good", "Bad", "Worse", "Dark / Gore"]
)

# ✅ Submit button
if st.button("Submit"):
    if story.strip() == "":
        st.warning("Please write something.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author = pseudonym.strip() if pseudonym else "Anonymous"
        polarity = TextBlob(story).sentiment.polarity

        new_data = pd.DataFrame([[author, story, timestamp, polarity, tone]],
                                columns=["Pseudonym", "Story", "Timestamp", "Sentiment", "Tone"])

        try:
            old_data = pd.read_csv("stories.csv")
            updated_data = pd.concat([old_data, new_data], ignore_index=True)
        except FileNotFoundError:
            updated_data = new_data

        updated_data.to_csv("stories.csv", index=False)
        st.success("Your story has been submitted anonymously!")

# 🔥 Display Stories
st.write("### 🔥 Latest Stories")
try:
    all_data = pd.read_csv("stories.csv")
    all_data = all_data.sort_values("Timestamp", ascending=False)
    
    for i, row in all_data.head(10).iterrows():
        st.markdown(f"""
        <div class="story-box">
        <b>{row['Pseudonym']}</b> <span style='color:#888'>at {row['Timestamp']}</span><br>
        {row['Story']}<br><br>
        <span style='font-size:13px; color:#FFDD57;'>🧠 Sentiment: {round(row['Sentiment'],2)}</span>  
        <span style='font-size:13px; color:#FF4B4B;'>🏷️ Tone: {row['Tone']}</span>
        </div>
        """, unsafe_allow_html=True)

    # 📊 Charts
    st.write("### 📊 Tone Distribution")
    tone_counts = all_data["Tone"].value_counts()
    st.bar_chart(tone_counts)

    fig, ax = plt.subplots()
    ax.pie(tone_counts.values, labels=tone_counts.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

except FileNotFoundError:
    st.info("No stories yet. Be the first to post something real.")
