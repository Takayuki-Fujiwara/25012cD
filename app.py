from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import tempfile
import os

# StreamlitのSecretsからAzure APIキーとエンドポイントを取得
subscription_key = st.secrets.AzureAPI.api_key
endpoint = st.secrets.AzureAPI.endpoint

# Azure Computer Visionクライアントの初期化
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# 画像の物体検出関数
def detect_objects(filepath):
    """指定された画像内の物体を検出する"""
    try:
        with open(filepath, "rb") as local_image:
            detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
            return detect_objects_results.objects
    except Exception as e:
        st.error(f"物体検出エラー: {e}")
        return []

# 画像のタグ情報取得関数
def get_tags(filepath):
    """指定された画像のタグ情報を取得する"""
    try:
        with open(filepath, "rb") as local_image:
            tags_result = computervision_client.tag_image_in_stream(local_image)
            return [tag.name for tag in tags_result.tags]
    except Exception as e:
        st.error(f"タグ取得エラー: {e}")
        return []

# アプリのタイトル
st.title("物体検出アプリ")

# サイドバーで画像をアップロード
uploaded_file = st.sidebar.file_uploader("画像を選択してください...", type=["jpg", "png"])

if uploaded_file is not None:
    # 一時的なファイルとして画像を保存
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        img_path = temp_file.name

    try:
        # 画像の読み込み
        img = Image.open(img_path)
        objects = detect_objects(img_path)

        # 検出された物体に矩形とラベルを描画
        draw = ImageDraw.Draw(img)
        for obj in objects:
            x, y, w, h = obj.rectangle.x, obj.rectangle.y, obj.rectangle.w, obj.rectangle.h
            caption = obj.object_property

            # フォントの読み込み
            font_path = os.path.join(os.path.dirname(__file__), "font/Helvetica 400.ttf")
            font = ImageFont.truetype(font=font_path, size=50)

            # ラベルのサイズ計算と描画
            text_bbox = draw.textbbox((0, 0), caption, font=font)
            text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            draw.rectangle([(x, y), (x + w, y + h)], outline="green", width=5)
            draw.rectangle([(x, y), (x + text_w, y + text_h + 15)], fill="green")
            draw.text((x, y), caption, fill="white", font=font)

        # 画像をStreamlit上に表示
        st.image(img, caption="認識された物体")

        # タグ情報の取得と表示
        tags = get_tags(img_path)
        st.markdown("**認識されたコンテンツタグ**")
        st.markdown("> " + ", ".join(tags))

    finally:
        # 一時ファイルの削除
        os.remove(img_path)
