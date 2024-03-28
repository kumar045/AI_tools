# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")
    logging.warning("GPU Not Found, using CPU, language Detection will be very slow.")


def loadModelCheckLanguage(
    pretrained_model: str= "papluca/xlm-roberta-base-language-detection",
    cache_dir: str = "apiAppTranslation/mlModel/",
):
    
    # Creating Tokenizer for Model
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model,
        cache_dir=cache_dir
    )
    
    # Creating Model
    model = AutoModelForSequenceClassification.from_pretrained(
        pretrained_model,
        cache_dir=cache_dir
    ).to(device)
    
    # Put model in eval mode
    model.eval()
    
    return tokenizer, model, device
    