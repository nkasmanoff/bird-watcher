import gradio as gr
import os
import pandas as pd


def load_images(folder):
    images = []
    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            images.append(os.path.join(folder, file))
    return images


def load_image_results(file_path):
    return pd.read_json(file_path)


def refresh():
    print("refreshing")
    # take another photo
    os.system("python take_photo.py")
    # update the results
    results_df = load_image_results("data/images.json")
    return results_df.sample(n=1)


with gr.Blocks() as demo:
    # plot all images
    results_df = load_image_results("data/images.json")
    images = load_images("data/images")

    # plot count versus time
    count_vs_time = gr.LinePlot(
        results_df, x="time", y="numBirds", title="Birds at Feeder",
        height=300,
        width=1500,
    )

    take_photo_button = gr.Button("Take another photo")

    # add a refresh_button which updates results_df
    refresh_button = gr.Button("Refresh")
    refresh_button.set_action(refresh)


if __name__ == "__main__":
    demo.launch()
