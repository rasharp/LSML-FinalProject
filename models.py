import torch, pickle
import numpy as np
from functools import partial

# 1. BERT
# 1.1 import BERT model and BERT tokenizer

with open("bert-model.bin", 'rb') as f:
    _bert = torch.load(f, map_location=torch.device('cpu'))
    
with open("bert-tokenizer.bin", 'rb') as f:
    _bert_tokenizer = pickle.load(f)

# 1.2 model prediction
def _predict_sentiment(model, tokenizer, text):
    enc_dict = tokenizer.encode_plus(
                        text,                      # Sentence to encode.
                        add_special_tokens = True, # Add '[CLS]' and '[SEP]'
                        truncation = True,
                        max_length = 300,           # Pad & truncate all sentences.
                        padding = 'max_length',
                        return_attention_mask = True,   # Construct attn. masks.
                        return_tensors = 'pt',     # Return pytorch tensors.
                   )

    # Add the encoded sentence to the list.    
    input_ids = [enc_dict['input_ids']]

    # And its attention mask (simply differentiates padding from non-padding).
    attention_mask = [enc_dict['attention_mask']]

    # Convert the lists into tensors.
    input_ids = torch.cat(input_ids, dim=0)
    attention_mask = torch.cat(attention_mask, dim=0)

    model.to("cpu")
    model.eval()
    res = model(input_ids, token_type_ids=None, 
              attention_mask=attention_mask, labels=None)
    probs = torch.nn.functional.softmax(res['logits'], dim=1).detach().numpy().flat
    return {label: probs[i] for i, label in enumerate(['negative', 'neutral', 'positive'])} 

predict_sentiment = partial(_predict_sentiment, _bert, _bert_tokenizer)

# 2. LDA
# 2.1 import LDA model and TF tokenizer

with open("LDA.bin", 'rb') as f_model:
    _lda = pickle.load(f_model)
    
with open("LDA_vec.bin", 'rb') as f_vec:
    _tf_vectorizer = pickle.load(f_vec)

# 2.2 model prediction
def _get_text_topics(text, model, vectorizer):
    vtext = vectorizer.transform([text])
    res = model.transform(vtext)
    return res

# 2.3 topics info
def _json_text_topics(model, vectorizer, text, n_topics=5):
    text_topics = _get_text_topics(text, model, vectorizer).flat
    top_topics = np.argsort(text_topics)[:-n_topics-1:-1]
    
    feature_names = vectorizer.get_feature_names()

    components = model.components_[top_topics]
    norm_weigh_sum = model.components_.sum(axis=1).reshape(-1, 1)
    res = {}
    for topic_idx, topic in enumerate(components):
        top_features_ind = topic.argsort()[:-6:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind] / norm_weigh_sum[topic_idx] * 100
        
        res_item = {feature: weight for feature, weight in zip(top_features, weights)}
        res["Topic "+str(topic_idx+1)] = (text_topics[top_topics[topic_idx]]*100, res_item)
    
    return res

json_text_topics = partial(_json_text_topics, _lda, _tf_vectorizer)