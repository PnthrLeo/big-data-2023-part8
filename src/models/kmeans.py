from pyspark.ml.clustering import KMeans
from pyspark.sql import DataFrame

from configs import scaled_feature_vector_col


class CustomKMeans:
    __slots__ = ['_model', '_model_params']

    def __init__(self, model_params: dict):
        self._model = None
        self._model_params = model_params

    @property
    def model(self):
        return self._model

    @property
    def model_params(self):
        return self._model_params

    def fit(self, df: DataFrame, force=False):
        if self._model is not None and not force:
            raise Exception('Model already has been trained. Use force=True to retrain.')

        trainer = KMeans(
            featuresCol=scaled_feature_vector_col,
            k = self._model_params.get('k', 2),
            seed = self._model_params.get('random_seed', 42)
        )
        self._model = trainer.fit(df)

    def transform(self, df: DataFrame) -> DataFrame:
        if self._model is None:
            raise Exception('Model has not been trained yet. Run fit() first.')
        return self._model.transform(df)

    def save_model(self, path):
        self._model.save(path)
