import tensorflow as tf
from tensorflow import keras
import pandas as pd
from joblib import load
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import models


class RatingBasedRecommender:
    def __init__(self, path, output_ids):
        self.model = keras.models.load_model(path,
                                             custom_objects={"masked_rmse_clip": models.masked_rmse_clip,
                                                             "masked_mse": models.masked_mse})
        self.ids = output_ids

    def predict_ratings(self, user_hist):
        predictions = self.model.predict(user_hist)
        predictions = predictions - user_hist
        predictions = pd.DataFrame(predictions.T, index=self.ids, columns=["rating"]).sort_values(by="rating",
                                                                                                  ascending=False)
        return predictions

    def recommend(self, user_hist, n, movies):
        preds = self.predict_ratings(user_hist).iloc[:n]
        preds["name"] = movies.loc[preds.index]
        return preds


class TagBasedRecommender:
    def __init__(self, autoencoder_path, vectorizer_path, n_layers=12):
        self._load_encoder(autoencoder_path, n_layers)
        self._load_vectorizer(vectorizer_path)

    def _load_encoder(self, path, n_layers):
        autoencoder = keras.models.load_model(path)
        self._encoder = keras.models.Sequential()
        self._encoder.add(autoencoder.input)
        for layer in autoencoder.layers[:12]:
            self._encoder.add(layer)

    def _load_vectorizer(self, path):
        self._vectorizer: "TfidfVectorizer" = load(path)

    def _transform(self, movies_tags):
        vectorized = self._vectorizer.transform((movies_tags["tag"]))
        embeddings = self._encoder.predict(vectorized.todense())
        return pd.DataFrame(data=embeddings, index=movies_tags.index)

    def calculate_similarity_matrix(self, movies_tags):
        embeddings = self._transform(movies_tags)
        self.similarity_matrix = pd.DataFrame(data=cosine_similarity(embeddings), index=movies_tags.index,
                                              columns=movies_tags.index)

    def recommend(self, movies, item, n):
        similar_items = pd.DataFrame(self.similarity_matrix.loc[item])
        similar_items.columns = ['similarity']
        similar_items.sort_values(by="similarity", ascending=False, inplace=True)
        similar_items.drop(index=item, inplace=True)
        similar_items = similar_items.head(n)
        similar_items["name"] = movies.loc[similar_items.index]
        return similar_items
