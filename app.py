import os
import zipfile
import gdown
from Classifier.classifier.model import Model
from Classifier.classifier.classifier import Classifier

def download_from_drive():
    url = 'https://drive.google.com/uc?id=1Wk8Y7ekbFlbPFkcN2DJ7xm47K-EEp4le'
    output = 'model.zip'
    gdown.download(url, output, quiet=False)
    path_to_zip_file = os.path.join(".","model.zip")
    directory_to_extract_to = os.path.join("Classifier")
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
    

if __name__ == "__main__":
    model_path = os.path.join("Classifier","models")
    model_bin = os.path.join(model_path,"sentimentanalysis.bin")
    dirs = os.listdir(model_path)
    if len(dirs) == 0:
        download_from_drive()
    model = Model(model_path,model_bin)
    model.model.eval()
    result = model.inference("Jorge es un buen producto")
    print(result)
    
    
    
