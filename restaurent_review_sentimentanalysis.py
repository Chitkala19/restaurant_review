# -*- coding: utf-8 -*-
"""restaurent_review_sentimentanalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ONEOrSBQruMCBo3Gye7k39vZqq9FPNzs
"""

#libraries
import numpy as np
import pandas as pd
# from google.colab import drive
import unicodedata
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
import joblib

data_set = pd.read_csv('/content/dataset_2.csv',encoding='latin-1')

# Print first 5 rows
print("Top 5 rows of dataset")
print(data_set.describe())

# Print random 10 rows
print("Random 10 rows")
print(data_set.sample(10))

# Print total number of rows and columns in dataset
print("Total rows and columns in dataset")
print(data_set.shape)

# Print number of rows and columns in dataset separately
print("Total Rows =", data_set.shape[0])
print("Total Columns =", data_set.shape[1])

print("Columns in dataset")
print(data_set.columns)

#Check information of dataset
print("Dataset information")
print(data_set.info())

data_set.describe()

data_set.head()

#Check for duplicate values
print("Checking for duplicate data")
print("Total Duplicated values =", data_set.duplicated().sum())

#Check for null values
print("Checking for null values")
print("Total NULL values =\n\n",data_set.isnull().sum())

print("Sort by no of ratings")
print(data_set['sentiment'].value_counts())

stopwords_set = set(stopwords.words('english'))
def processing(text):

    # Step 1: Remove Accented Characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # Step 2: Tokenization
    tokens = word_tokenize(text)

    # Step 3: Stopwords Removal
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Step 4: Remove Numbers and Extra Whitespaces
    filtered_tokens = [re.sub(r'\d+', '', word) for word in filtered_tokens]
    filtered_tokens = [word.strip() for word in filtered_tokens if word.strip()]

    # Step 5: Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Step 6: Stemming (optional)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in lemmatized_tokens]

    # Step 7: Remove Single Letters
    filtered_tokens = [word for word in stemmed_tokens if len(word) > 1]

    # Join the tokens back into a clean text string
    clean_text = ' '.join(filtered_tokens)


    return clean_text

i=0
for reviews in data_set['review']:
  data_set.at[i,'review'] = processing(reviews)
  # data_set.at[i,'rating']= data_set.at[i,'rating'][0]
  # data_set.at[i,'review_time'] = convert_time_to_days(data_set.at[i,'review_time'])
  # print(convert_time_to_days(data_set.at[i,'review_time']))
  # if i==5:
  #   break
  i+=1
data_set.head()

random_sample = data_set.sample(n=20, random_state=42)
random_sample

sia = SentimentIntensityAnalyzer()
sentiments = []

for review in data_set['review']:
    sentiment = sia.polarity_scores(review)
    sentiments.append(sentiment)

i=0
while i!=10:
  print(sentiments[i])
  i+=1

sentiment_labels = []

for sentiment in sentiments:
    compound_score = sentiment['compound']
    # compound_score = sentiment
    if compound_score >= 0.05:
        sentiment_labels.append(1)
    elif compound_score <= -0.05:
        sentiment_labels.append(-1)
    else:
        sentiment_labels.append(0)

data_set['sentiment'] = sentiment_labels
data_set[['review', 'sentiment']]

X = data_set['review']
y = data_set['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Create a LinearSVC model
linear_svc_model = LinearSVC()

# Fit the model to the TF-IDF training data
linear_svc_model.fit(X_train_tfidf, y_train)

# Predict on the TF-IDF test data
linear_svc_y_pred = linear_svc_model.predict(X_test_tfidf)

# Calculate accuracy and print the results
linear_svc_accuracy = accuracy_score(y_test, linear_svc_y_pred)
print("LinearSVC Accuracy:", linear_svc_accuracy)
print("Classification Report:")
print(classification_report(y_test, linear_svc_y_pred))

# Create a MultinomialNB model
naive_bayes_model = MultinomialNB()

# Fit the model to the TF-IDF training data
naive_bayes_model.fit(X_train_tfidf, y_train)

# Predict on the TF-IDF test data
naive_bayes_y_pred = naive_bayes_model.predict(X_test_tfidf)

# Calculate accuracy and print the results
naive_bayes_accuracy = accuracy_score(y_test, naive_bayes_y_pred)
print("Multinomial Naive Bayes Accuracy:", naive_bayes_accuracy)
print("Classification Report:")
print(classification_report(y_test, naive_bayes_y_pred))

# Create a Logistic Regression model
logistic_regression_model = LogisticRegression()

# Fit the model to the TF-IDF training data
logistic_regression_model.fit(X_train_tfidf, y_train)

# Predict on the TF-IDF test data
logistic_regression_y_pred = logistic_regression_model.predict(X_test_tfidf)

# Calculate accuracy and print the results
logistic_regression_accuracy = accuracy_score(y_test, logistic_regression_y_pred)
print("Logistic Regression Accuracy:", logistic_regression_accuracy)
print("Classification Report:")
print(classification_report(y_test, logistic_regression_y_pred))

# Create a Random Forest model
random_forest_model = RandomForestClassifier()

# Fit the model to the TF-IDF training data
random_forest_model.fit(X_train_tfidf, y_train)

# Predict on the TF-IDF test data
random_forest_y_pred = random_forest_model.predict(X_test_tfidf)

# Calculate accuracy and print the results
random_forest_accuracy = accuracy_score(y_test, random_forest_y_pred)
print("Random Forest Accuracy:", random_forest_accuracy)
print("Classification Report:")
print(classification_report(y_test, random_forest_y_pred))

model1 = LinearSVC()
model2 = MultinomialNB()
model3 = LogisticRegression()

ensemble_model = VotingClassifier(
    estimators=[('model1', model1), ('model2', model2), ('model3', model3)],
    voting='hard'  # You can choose 'hard' or 'soft' voting depending on your use case
)

# Fit the ensemble model on the training data
ensemble_model.fit(X_train_tfidf, y_train)

# Make predictions using the ensemble model
y_pred = ensemble_model.predict(X_test_tfidf)

# Evaluate the performance of the ensemble model (you can use different metrics)
accuracy = accuracy_score(y_test, y_pred)
print(f'Ensemble Model Accuracy: {accuracy:.2f}')

# Finally, you can use the trained ensemble model to make predictions on your test data
y_test_pred = ensemble_model.predict(X_test_tfidf)

# Save the ensemble model
joblib.dump(ensemble_model, 'ensemble_model_1.joblib')
joblib.dump(vectorizer, 'tfidf_vectorizer_1.joblib')

loaded_model = joblib.load('ensemble_model_1.joblib')
loaded_vectorizer = joblib.load('tfidf_vectorizer_1.joblib')
Input="The delectable aroma of the freshly baked bread filled the air as I stepped into the cozy bakery. The warm, crusty baguette I ordered was a delightful treat. It had a perfect crunch on the outside and a soft, airy interior. Absolutely delicious!"
input_vector = loaded_vectorizer.transform([processing(Input)])
predicted_rating = loaded_model.predict(input_vector)
print("Predicted Rating:", predicted_rating)