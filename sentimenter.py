
#Helper Module for trading_bot which takes care of the sentiment analysis setup

#IMPORTS
from transformers import AutoTokenizer, AutoModelForSequenceClassification  
#Tokenzier allows us to pass string and convert to sequence of numbers, so we can pass to NLP model
#AutoModel gives architechture to be able to load in NLP model
import torch  #Allows us to use argmaths to extract highest sequence result
from typing import Tuple

device = "cuda:0" if torch.cuda.is_available() else "cpu"  #Checks if cuda is available on laptop, if yes then it uses it on GPU at index 0, else it uses CPU
#Cuda is software that gives access to the computer's GPU, using GPU helps speed up calculations, especially for things like ML

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert") 
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")  #Gotten from https://huggingface.co/ProsusAI/finbert?library=transformers
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news) :
    if news :
        tokens = tokenizer(news, return_tensors = "pt", padding = True).to(device) #return_tensor="pt" returns data in pytorch objects format, padding pads data to longest sequence in batch, .to(device) sends processing to device (GPU/CPU in this case)

        result = model(tokens["input_ids"], attention_mask = tokens["attention_mask"])["logits"] #runs the model with tokens's input_ids values, and uses the attention mask returned by tokens (attention mask dictates which token values the model should care about), it then stores the logits part of the model's return list

        result = torch.nn.functional.softmax(torch.sum(result, 0), dim = -1) #torch.sum(result, 0) sums up the logits in result, torch.nn.functional.softmax converts the logits into probabilities, and dim = -1 helps us do it over the classes
        probability = result[torch.argmax(result)] #finds highest tensor and stores it as probability
        sentiment = labels[torch.argmax(result)] #finds sentiment label corresponding with highest tensor
        return probability, sentiment
    else: 
        return 0, labels[-1]
    

