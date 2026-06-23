import streamlit as st
import yt_dlp
import os

# 1. Page Configuration & Custom Aesthetic CSS Injection
st.set_page_config(page_title="HQ Downloader", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
        /* Main page background */
        .stApp {
            background-color: #0b0c10;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Glowing Gradient Text for Heading */
        .glowing-title {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(to right, #4facfe, #00f2fe, #66fcf1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 12px rgba(102, 252, 241, 0.6));
            text-align: center;
            margin-bottom: 30px;
        }
        
        /* Custom styling for text input */
        div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5) !important;
            transition: 0.3s ease-in-out;
        }
        
        div[data-baseweb="input"]:focus-within {
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5), 0 0 15px rgba(79, 172, 254, 0.5) !important;
            border: 1px solid #66fcf1 !important;
        }

        input {
            color: white !important;
        }

        /* Gradient styling for buttons */
        div.stButton > button {
            background: linear-gradient(45deg, #45a247, #283c86) !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
            padding: 12px 30px !important;
            border-radius: 10px !important;
            box-shadow: 0 0 15px rgba(69, 162, 71, 0.5) !important;
            transition: all 0.3s ease !important;
            width: 100%;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 0 25px rgba(69, 162, 71, 0.8) !important;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Rendering the Visual Elements
st.markdown('<div class="glowing-title">HQ Downloader</div>', unsafe_allow_html=True)

video_url = st.text_input("", placeholder="Paste YouTube link here...")

if video_url:
    if "youtube.com" in video_url or "youtu.be" in video_url:
        st.write("✨ URL Verified. Click below to fetch the high quality stream.")
        
        if st.button("Process & Download Video"):
            with st.spinner("Stitching 1080p streams... Please wait..."):
                
                # Optimized options: limits format to 1080p max height to eliminate playback lag
                ydl_opts = {
                    'format': 'bestvideo[height<=1080]+bestaudio/best',
                    'outtmpl': 'downloaded_hq_video',
                    'merge_output_format': 'mp4',
                    'quiet': True,
                    'overwrites': True
                }
                
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        filename = "downloaded_hq_video.mp4"
                        
                        if os.path.exists(filename):
                            with open(filename, "rb") as file:
                                st.success("✓ Video successfully compiled!")
                                st.download_button(
                                    label="🔥 Save Video to Device",
                                    data=file,
                                    file_name=f"{info.get('title', 'video')}.mp4",
                                    mime="video/mp4"
                                )
                        else:
                            st.error("Error: Output file processing mismatch.")
                except Exception as e:
                    st.error(f"Extraction failed: {str(e)}")
    else:
        st.error("Please enter a valid YouTube link.")