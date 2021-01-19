import os
import zipfile
import gdown

from flask import Flask, render_template, jsonify, request
import pandas as pd
from io import StringIO, BytesIO
from base64 import b64encode
from io import StringIO
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt

from Classifier.classifier.model import Model
from Classifier.classifier.classifier import Classifier
from Classifier.topic.topic_modelling import TopicAna
from Classifier.tools.reader import Reader

matplotlib.use('Agg')


def get_image_b64(b64encoded):
    image = """
        <img src="data:image/png;base64,{b64}"/>
    """
    return image.format(b64=b64encoded.decode("utf-8"))


def get_html_by_figure(figure):
    pic_IObytes = BytesIO()
    figure.savefig(pic_IObytes,format='png')
    pic_IObytes.seek(0)
    pic_hash = b64encode(pic_IObytes.read())
    image_hash = get_image_b64(pic_hash)
    plt.close()
    return image_hash


def download_from_drive():
    url = 'https://drive.google.com/uc?id=1Wk8Y7ekbFlbPFkcN2DJ7xm47K-EEp4le'
    output = 'model.zip'
    gdown.download(url, output, quiet=False)
    path_to_zip_file = os.path.join(".","model.zip")
    directory_to_extract_to = os.path.join("Classifier")
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

def get_wordcloud(iterable):
    long_string = " ".join(iterable)
    wordcloud = WordCloud(background_color="#242526", max_words=5000, contour_width=3, contour_color='steelblue')
    cloud = wordcloud.generate(long_string)
    figure = plt.figure(facecolor="#242526")
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    return get_html_by_figure(figure)

app = Flask("Demo Sentiment Analysis")
model_path = os.path.join("Classifier","models")
model_bin = os.path.join(model_path,"sentimentanalysis.bin")
dirs = os.listdir(model_path)
if len(dirs) == 0:
    download_from_drive()    
model = Model(model_path,model_bin)
model.model.eval()

@app.route("/inference_text" , methods=["POST"])
def inference_text():
    response = {}
    text = request.form["card_text"]
    response["result"] = model.inference(text)
    return jsonify(response)

@app.route("/inference_file" , methods=["POST"])
def inference_file():
    response = {}
    file_content = request.files["file"].read().decode("utf-8", 'ignore')
    filename = request.files["file"].filename
    reader = Reader(StringIO(file_content),filename)
    new_df = reader.topytorch()
    outputs = model.inference_df(new_df)
    reader.df["sentiment"] = outputs
    number = reader.df.groupby("sentiment")["review"].count()
    number = [val for val in number]
    negative = reader.df[reader.df["sentiment"]=="Negativo"]["review"].values.tolist()
    positive = reader.df[reader.df["sentiment"]=="Positivo"]["review"].values.tolist()
    topics_positive = TopicAna(positive).get_topics()
    topics_negative = TopicAna(negative).get_topics()
    response["sentiment_data"] = number
    response["img_positive"] = get_wordcloud(topics_positive)
    response["img_negative"] = get_wordcloud(topics_negative)
    return jsonify(response)

@app.route("/")
def index():
    return render_template("index.html")
  

app.run(debug=True)
    
    
