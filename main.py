import praw
import streamlit as st
from gtts import gTTS 
import base64
from pydub import AudioSegment
import time

#from io import BytesIO


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def get_duration_pydub(file_path):
   audio_file = AudioSegment.from_file(file_path)
   duration = audio_file.duration_seconds
   return duration


def main():
    reddit = praw.Reddit()

    reddit.read_only = True

    output = st.container()
    input = st.text_input("Reddit post Id")

    with output:
        st.markdown(
            """
        <style>
            audio {
                display:none
            }
        </style>
        """,
        unsafe_allow_html=True,
        )
    if input:
        post = reddit.submission(input)
        post.comment_sort = 'top'
        post.comments.replace_more(limit=0)
        with output:
            st.write(f"{post.subreddit}: {post.title}]")
        comments = post.comments.list()
        for comment in range(40):
            with output:
                st.write(comments[comment].body)
                st.divider()
                #mp3_speech = BytesIO()
                speech = gTTS(comments[comment].body, slow=False)
                #tts.write_to_fp(mp3_speech)
                speech.save('test.mp3')
                autoplay_audio('test.mp3')
                time.sleep(get_duration_pydub('test.mp3'))
        #for comment in comments:
         #   print(comment.body)

if __name__ == "__main__":
    main()
