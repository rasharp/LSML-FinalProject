# LSML-FinalProject
Final project for MDS LSML-2 course

## 1. Project description
Idea of project  is to classify financial news sentiment. In comparison with usual sentiment analysis (like movies or hotels reviews and so on) financial news much less emotional and language is more formal. But in most cases human can definitely recognize whether news is positive or negative in terms of expected market impact (but it doesn't mean that market response will be really the same as expected :) )

Unfortunately labeled datasets for financial news are rare, I find one on Kaggle but it is not so big, therefore I decided add unlabeled data and solve task of topic discovering using LDA model as an example of unsupervised learning task.

Models are realized as API with Flask web-server (with Celery-Redis asynchronous engine for LDA model and simple synchronous for sentiment analysis model)

## 2. Dataset
### 2.1 Dataset for sentiment analysis (labeled)
I use this one from kaggle https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news. Also it can be found here in data folder / [all-data.csv](https://github.com/rasharp/LSML-FinalProject/raw/main/data/all-data.csv)

Dataset consist of 4000+ news with labels (positive, negative or neutral)

### 2.2 Dataset for LDA model (unlabeled)
I use this one from kaggle https://www.kaggle.com/jeet2016/us-financial-news-articles
This dataset contains news from prime news providers (reuters, CNBC, WSJ) from Jan till May of 2018.
Total there are more than 300000 news articles (~1 Gb).
Cleaned dataset in convienient form (tab-separated file) is presented here in data / [news.zip](https://github.com/rasharp/LSML-FinalProject/raw/main/data/news.zip)
Use git-lfs to clone.

## 3. Model
### 3.1 BERT fine-tuned classifier
Standard pre-trained [BERT-base-uncased](https://huggingface.co/bert-base-uncased) model is used.
Model fine-tuned with standard parameters.
All pipeline is available in [Google Colab notebook](https://github.com/rasharp/LSML-FinalProject/blob/main/LSML-2%20Final_BERT.ipynb).
Accuracy of the model is about 85%.
Saved [BERT model](https://github.com/rasharp/LSML-FinalProject/raw/main/models/bert-model.bin) and [BERT tokenizer](https://github.com/rasharp/LSML-FinalProject/raw/main/models/bert-tokenizer.bin) are in the models folder (use git-lfs to clone).

### 3.2 LDA
I used standard sklearn implementation of LDA for simplicity, but using "big data tools" as PySpark is very straightforward in this case.
Number of topics is 10.
All pipeline is available in [Google Colab notebook](https://github.com/rasharp/LSML-FinalProject/blob/main/LSML-2%20FInal_LDA.ipynb).

## 4. Usage instructions
For deploy use docker repo rasharp
Source code is presented in docker folder.
