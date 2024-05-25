from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import os
from torch import tensor
import matplotlib.pyplot as plt
import time
import json

processor = DetrImageProcessor.from_pretrained(
    "facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained(
    "facebook/detr-resnet-50", revision="no_timm")


def convert_unix_time_to_human_readable(unix_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_time))


def generate_bounding_boxes(model, processor):
    image = Image.open("data/detr/image.jpg")
    current_time = time.time()
    current_time = convert_unix_time_to_human_readable(current_time)
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = tensor([image.size[::-1]])

    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes, threshold=0.9)[0]

    found_objects = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        found_objects.append(
            {'score': score.item(), 'label': model.config.id2label[label.item()], 'box': box.tolist(),  'time': current_time})

    return found_objects


def plot_bounding_boxes(image, found_objects):
    plt.imshow(image)
    ax = plt.gca()
    for obj in found_objects:
        box = obj['box']
        rect = plt.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                             fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        plt.text(
            box[0], box[1], f'{obj["label"]}: {obj["score"]}', fontsize=12, color='red')
    plt.axis('off')
    # save image
    plt.savefig(f"data/images/{obj['time']}.jpg")


def count_birds(found_objects):
    bird_counter = 0
    for obj in found_objects:
        if obj['label'] == 'bird':
            bird_counter += 1

    return bird_counter


def update_bird_tracker():
    os.system("libcamera-still -o data/detr/image.jpg")
    found_objects = generate_bounding_boxes(model, processor)

    bird_count = count_birds(found_objects)
    print("Number of birds: ", bird_count)
    if os.path.exists("data/images.json") == False:
        with open("data/images.json", "w") as file:
            json.dump([], file)

    with open("data/images.json", "r") as file:
        data = json.load(file)

    data.append({'time': found_objects[0]['time'], 'numBirds': bird_count})

    with open("data/images.json", "w") as file:
        json.dump(data, file)

    plot_bounding_boxes(Image.open("data/detr/image.jpg"), found_objects)


def bird_tracker_loop():
    while True:
        update_bird_tracker()
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = float(temp.split('=')[1].split("'")[0])
        print("Current temp: ", temp)
        if temp <= 60:
            time.sleep(30)

        elif temp > 60 and temp < 70:
            time.sleep(120)

        elif temp > 70:
            time.sleep(300)


if __name__ == "__main__":
    bird_tracker_loop()
