import streamlit as st
import edge_tts
import asyncio

# --- Page Setup ---
st.set_page_config(page_title="Neerja Voice App", page_icon="🎙️")
st.title("🎙️ AI Voice Generator")

# --- Inputs ---
text = st.text_area("Yahan Script Likho:", height=150, placeholder="Hello, check kar raha hu...")

col1, col2 = st.columns(2)
with col1:
    gender = st.radio("Awaaz:", ["Female (Neerja)", "Male (Prabhat)"])
with col2:
    speed = st.slider("Speed:", -50, 50, 0)
    pitch = st.slider("Pitch:", -20, 20, 0)

# --- Logic ---
async def generate_audio(text, voice, rate, pitch):
    # Agar parameters 0 hain to default string use karein taaki error na aaye
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save("output_audio.mp3")

if st.button("🔊 Generate Audio", type="primary"):
    if not text:
        st.error("Script khali hai! Kuch likho pehle.")
    else:
        # Settings Preparation
        voice_key = "en-IN-NeerjaNeural" if "Female" in gender else "en-IN-PrabhatNeural"
        
        # --- FIX: Strict formatting for Cloud ---
        # Agar 0 hai to "+0%" manually set karo, formula mat lagao
        if speed == 0:
            rate_str = "+0%"
        else:
            rate_str = f"{speed:+d}%"
            
        if pitch == 0:
            pitch_str = "+0Hz"
        else:
            pitch_str = f"{pitch:+d}Hz"

        # Debug info (Screen par dikhega ki kya bhej rahe hain)
        st.caption(f"Processing: {voice_key} | Speed: {rate_str} | Pitch: {pitch_str}")

        with st.spinner("Generating..."):
            try:
                # Async loop logic specifically for Streamlit Cloud
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate_audio(text, voice_key, rate_str, pitch_str))
                
                # Success
                st.success("Ban gaya! Niche play karo 👇")
                st.audio("output_audio.mp3", format="audio/mp3")
                
                # Download Button
                with open("output_audio.mp3", "rb") as file:
                    st.download_button(
                        label="⬇️ Download MP3",
                        data=file,
                        file_name="my_ai_voice.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"Error details: {e}")
