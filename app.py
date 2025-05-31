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
endpoint = st.secrets.AzureAPI.endpoint

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))