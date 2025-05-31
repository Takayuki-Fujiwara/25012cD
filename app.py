from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import streamlit as st

# Streamlit Cloudの「Secrets」からAzure API keyとエンドポイントを取得
subscription_key = st.secrets.AzureAPI.api_key
endpoint = https://udemy-0511.cognitiveservices.azure.com/

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# 画像の物体検出をする関数
def detect_objects(filepath):
    local_image = open(filepath, "rb")

    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects

# 画像のタグ情報を取得する関数
def get_tags(filepath):
    local_image = open(filepath, "rb") 
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    return tags_name



st.title("物体検出アプリ")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type = ["jpg", "png"])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f"img/{uploaded_file.name}"
    img.save(img_path)
    objects = detect_objects(img_path)
    
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font="font/Helvetica 400.ttf", size=50)
        # Udemy講座で使われているImageDrawのtextsizeは廃止
        # 代わりにImageDrawのtextboxを使用
        text_bbox = draw.textbbox((0, 0), caption, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]

        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline="green", width=5)
        draw.rectangle([(x, y), (x+text_w, y+text_h+15)], fill="green")
        draw.text((x, y ), caption, fill="white", font=font)

    st.image(img)

    tags_name = get_tags(img_path)
    tags_name = ", ".join(tags_name)
    print(tags_name)

    st.markdown("**認識されたコンテンツタグ**")
    st.markdown("> " + tags_name)

    os.remove(img_path)
