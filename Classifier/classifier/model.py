import torch
from torch.utils.data import Dataset, DataLoader
from torch import cuda
from transformers import AutoModel, AutoTokenizer, BertTokenizer, BertForSequenceClassification, AutoModelForSequenceClassification, BertModel, AutoConfig
import numpy as np
import pandas as pd
import os

from Classifier.tools.data_loader import Data

device = 'cuda' if cuda.is_available() else 'cpu'
#device = 'cpu' 
torch.set_grad_enabled(False)

class Model(object):
    def __init__(self, model_path, model_bin):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model=torch.load(model_bin)
        self.model.to(device)
        self.MAX_LEN = 512
        
    def inference(self, text):
        review = " ".join(text.lower().split())
        inputs = self.tokenizer.encode_plus(
            review,
            None,
            add_special_tokens=True,
            max_length=512,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']

        data_set = [{
                    'ids': torch.tensor(ids, dtype=torch.long),
                    'mask': torch.tensor(mask, dtype=torch.long),
                }]
        params = {'batch_size': 1, 'num_workers': 0}
        loader = DataLoader(data_set, **params)
        for _,data in enumerate(loader, 0):
            ids = data['ids'].to(device, dtype = torch.long)
            mask = data['mask'].to(device, dtype = torch.long)
            output = self.model(ids, mask)
        _, val = torch.max(output.data, dim=1)
        values = {0: "Negativo", 1: "Positivo"}
        return values[int(val)]
        

    def inference_df(self, df):
        inference_params = {'batch_size': 1, 'num_workers': 0}
        inference_test = Data(df, self.tokenizer, self.MAX_LEN)
        inference_loader = DataLoader(inference_test, **inference_params)
        outputs = []
        values = {0: "Negativo", 1: "Positivo"}
        for _,data in enumerate(inference_loader, 0):
            ids = data['ids'].to(device, dtype = torch.long)
            mask = data['mask'].to(device, dtype = torch.long)
            output = self.model(ids, mask)
            _, val = torch.max(output.data, dim=1)
            outputs.append(values[int(val)])
        return outputs
        