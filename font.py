import os
import requests
import json
import base64
import streamlit as st
from fontTools.ttLib import TTFont

try:
    import fake_useragent
except ModuleNotFoundError:
    print("fake_useragent library not found. Installing...")
    os.system("pip install fake_useragent")
    import fake_useragent


def fetch_fonts_from_api(api_url):
    ua = fake_useragent.UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(f"{api_url}/api/fonts", headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    fonts = response.json()

    for font in fonts:
        font["path"] = "data:font/woff;base64," + font["path"].replace("data:.*?;base64,", "")

    return fonts


def convert_woff_to_ttf(woff_file_path):
    ttf_file_path = woff_file_path.replace(".woff", ".ttf")
    font = TTFont(woff_file_path)
    font.flavor = "woff"
    font.save(ttf_file_path)
    return ttf_file_path


def save_font_to_file(item):
    base64_data = item["path"].split(";base64,")[-1]
    binary_data = base64.b64decode(base64_data)

    directory = "fonts"
    if not os.path.exists(directory):
        os.makedirs(directory)

    woff_file_path = os.path.join(directory, f"{item['name']}.woff")

    with open(woff_file_path, "wb") as file:
        file.write(binary_data)

    ttf_file_path = convert_woff_to_ttf(woff_file_path)

    return ttf_file_path


api_url = "https://chrome.fontiran.com"
fonts = fetch_fonts_from_api(api_url)

st.title("Download Fonts")
for font in fonts:
    if st.button(f"Download {font['name']}"):
        ttf_file_path = save_font_to_file(font)
        st.success(f"Font '{font['name']}' saved and converted to '{ttf_file_path}'")
