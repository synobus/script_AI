import streamlit as st
import edge_tts
import asyncio

# --- Page Setup ---
st.set_page_config(page_title="Neerja & Swara AI Voice", page_icon="🎙️")
st.title("🎙️ AI Voice Generator")
st.markdown("Hindi text ke liye **Swara** ya **Madhur** use karein.")

# --- Inputs ---
text = st.text_area("Script:", height=150, placeholder="Yahan Hindi ya English likhein...")

# Dropdown for Voices (Hindi added)
voice_option = st.selectbox(
    "Voice Select Karein:",
    [
        "Female - Neerja (English/Hindi Mix)",
        "Male - Prabhat (English/Hindi Mix)",
        "Female - Swara (Pure Hindi)",
        "Male - Madhur (Pure Hindi)"
    ]
)

col1, col2 = st.columns(2)
with col1:
    speed = st.slider("Speed:", -50, 50, 0)
with col2:
    pitch = st.slider("Pitch:", -20, 20, 0)

# --- Logic ---
async def generate_audio(text, voice, rate_str, pitch_str):
    # Agar parameters default (0) hain, to unhe bhejo hi mat (Library default use karegi)
    # Isse "Invalid Pitch/Rate" error nahi aayega.
    params = {}
    if rate_str: 
        params['rate'] = rate_str
    if pitch_str: 
        params['pitch'] = pitch_str
        
    communicate = edge_tts.Communicate(text, voice, **params)
    await communicate.save("output_audio.mp3")

if st.button("🔊 Generate Audio", type="primary"):
    if not text:
        st.error("Script khali hai!")
    else:
        # 1. Voice Mapping
        if "Neerja" in voice_option:
            voice_key = "en-IN-NeerjaNeural"
        elif "Prabhat" in voice_option:
            voice_key = "en-IN-PrabhatNeural"
        elif "Swara" in voice_option:
            voice_key = "hi-IN-SwaraNeural"  # Best for Hindi Text
        else:
            voice_key = "hi-IN-MadhurNeural" # Best for Hindi Male

        # 2. Smart Settings (0 hone par None bhejo)
        final_rate = f"{speed:+d}%" if speed != 0 else None
        final_pitch = f"{pitch:+d}Hz" if pitch != 0 else None

        st.caption(f"Processing: {voice_key} | Speed: {final_rate if final_rate else 'Default'} | Pitch: {final_pitch if final_pitch else 'Default'}")

        with st.spinner("Generating..."):
            try:
                # Async loop logic
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate_audio(text, voice_key, final_rate, final_pitch))
                
                # Success
                st.success("Audio Ban Gaya! ✅")
                st.audio("output_audio.mp3", format="audio/mp3")
                
                # Download
                with open("output_audio.mp3", "rb") as file:
                    st.download_button(
                        label="⬇️ Download MP3",
                        data=file,
                        file_name="ai_voice.mp3",
                        mime="audio/mp3"
                    )
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Tip: Agar Hindi text hai to 'Swara' ya 'Madhur' voice select karein.")
