import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process as aksharamukha_process
from gtts import gTTS
from io import BytesIO
import pandas as pd

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Korean → Kannada Learning",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------ HIDE STREAMLIT UI ------------------ #
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------ AUDIO GENERATOR ------------------ #
def make_audio(text, lang="kn"):
    fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# ------------------ PAGE TITLE ------------------ #
st.title("📝 Learn Kannada using Korean Script")
st.subheader("한국어로 칸나다어 배우기")

text = st.text_area("한국어 문장을 입력하세요 (Enter Korean text):", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # ---------------- FULL SENTENCE PROCESSING ---------------- #

            # Korean → Kannada translation
            kannada = GoogleTranslator(source="ko", target="kn").translate(text)

            # Kannada → Latin script (for Korean users)
            kannada_in_latin = aksharamukha_process("Kannada", "ISO", kannada)

            # Kannada → English phonetics (ITRANS)
            kannada_english = transliterate(kannada, sanscript.KANNADA, sanscript.ITRANS)

            # Kannada audio
            audio_sentence = make_audio(kannada)

            # ---------------- DISPLAY ---------------- #
            st.markdown("## 🔹 Translation Results")

            st.markdown(f"**Korean Input:**  \n:blue[{text}]")
            st.markdown(f"**Kannada Translation:**  \n:green[{kannada}]")
            st.markdown(f"**Kannada in Latin Script:**  \n:orange[{kannada_in_latin}]")
            st.markdown(f"**English Phonetics:**  \n`{kannada_english}`")

            st.markdown("### 🔊 Kannada Audio (Sentence)")
            st.audio(audio_sentence, format="audio/mp3")
            st.download_button("Download Sentence Audio", audio_sentence, "sentence.mp3")

            # ---------------- WORD-BY-WORD FLASHCARDS ---------------- #

            st.markdown("---")
            st.markdown("## 🃏 Flashcards (Word-by-Word)")

            korean_words = text.split()      # Korean already spaced!
            kan_words = kannada.split()

            limit = min(len(korean_words), len(kan_words))

            for i in range(limit):
                kw_input = korean_words[i]
                kw = kan_words[i]

                # Kannada → Latin (word)
                kw_lat = aksharamukha_process("Kannada", "ISO", kw)

                # Phonetics
                kw_ph = transliterate(kw, sanscript.KANNADA, sanscript.ITRANS)

                # Word audio
                kw_audio = make_audio(kw)

                with st.expander(f"Word {i+1}: {kw_input}", expanded=False):
                    st.write("**Korean word:**", kw_input)
                    st.write("**Kannada word:**", kw)
                    st.write("**Kannada in Latin script:**", kw_lat)
                    st.write("**Phonetics:**", kw_ph)

                    st.audio(kw_audio, format="audio/mp3")
                    st.download_button(
                        f"Download Audio (Word {i+1})",
                        kw_audio,
                        f"word_{i+1}.mp3"
                    )

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please enter Korean text.")
