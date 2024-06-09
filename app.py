import streamlit as st
import os
import pandas as pd


def load_images(folder):
    images = []
    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            images.append(os.path.join(folder, file))
        images.sort(key=os.path.getmtime)

    return images[::-1]


def load_image_results(file_path):
    return pd.read_json(file_path)


results_df = load_image_results("data/images.json")
images = load_images("data/detr")

st.title("Bird Watcher 🐦")

st.markdown(
    f"### Latest Bird Count: {results_df.tail(1)['numBirds'].values[0]}")

st.markdown("## Bird Count Over Time")
st.line_chart(results_df.set_index("time")["numBirds"]
              )


st.markdown("## Taken Photos")
if len(images) > 0:
    
    selected_image = st.selectbox("Select an image", images)

    st.image(selected_image)


if st.button("Refresh"):
    results_df = load_image_results("data/images.json")
    images = load_images("data/detr")
