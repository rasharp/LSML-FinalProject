# LSML-FinalProject
Final project for MDS LSML-2 course

## 1. Project documentation
Idea of project  is to classify financial news sentiment. In comparison with usual sentiment analysis (like movies or hotels reviews and so on) financial news much less emotional and language is more formal. But in most cases human can definitely recognize wether news is positive or negative in terms of market impact (but it doesn't mean that market response will be the same :) )
Unfortunately labeled datasets for financial news are rare, I find one on Kaggle but it is not so big, therefore I decided add unlabeled data and solve task of topic discovering using LDA model.

## 2. Dataset
### 2.1 Dataset for sentiment analysis (labeled)
I use this one from kaggle https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news
Dataset consist of 4000+ news with labels (positive, negative or neutral)
Also it can be found here in data folder.

### 1.2 Dataset for LDA model (unlabeled)
I use this one from kaggle https://www.kaggle.com/jeet2016/us-financial-news-articles
This dataset contains news from prime news providers (reuters, CNBC, WSJ) from Jan till May of 2018.
Total there are more than 300000 news articles (~1 Gb).
Cleaned dataset in convienient form (tab-separated file) shared on my google drive:
https://drive.google.com/file/d/1-5fzHbjQa3E9wd61FHG70SaJ6mPTL_M3/view?usp=sharing

## 1. Model
### 1.2 BERT fine-tuned classifier
### 1.2 LDA
I used standard sklearn implementation of LDA for simplicity, but using "big data tools" as PySpark is very straightforward in this case.


## 1. Usage instructions
