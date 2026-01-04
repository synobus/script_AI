import streamlit as st
import edge_tts
import asyncio

# --- Page Setup ---
st.set_page_config(page_title="Neerja Voice App", page_icon="🎙️")
st.title("🎙️ AI Voice Generator")

# --- Inputs ---
text = st.text_area("Yahan Script Likho:", height=150, placeholder="Hello dosto...")

col1, col2 = st.columns(2)
with col1:
    gender = st.radio("Awaaz:", ["Female (Neerja)", "Male (Prabhat)"])
with col2:
    speed = st.slider("Speed:", -50, 50, -10)
    pitch = st.slider("Pitch:", -20, 20, 0)

# --- Logic ---
async def generate_audio(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save("output_audio.mp3")

if st.button("🔊 Generate Audio", type="primary"):
    if not text:
        st.error("Kuch likho to sahi!")
    else:
        # Settings set karo
        voice_key = "en-IN-NeerjaNeural" if "Female" in gender else "en-IN-PrabhatNeural"
        
        # Format fix for API
        rate_str = f"{speed:+d}%"
        pitch_str = f"{pitch:+d}Hz"

        with st.spinner("Generating..."):
            try:
                # Async loop logic for Cloud
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate_audio(text, voice_key, rate_str, pitch_str))
                
                # Success
                st.success("Audio Ban Gaya! ✅")
                st.audio("output_audio.mp3", format="audio/mp3")
                
                # Download Button
                with open("output_audio.mp3", "rb") as file:
                    st.download_button(
                        label="⬇️ Download MP3",
                        data=file,
                        file_name="my_voice.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"Error aaya: {e}")
