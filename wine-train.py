from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def prepare_data(spark, file_path):
    df = spark.read.csv(file_path, header=True, inferSchema=True, sep=";")
    for old in df.columns:
        new = old.replace('"', '').strip()
        df = df.withColumnRenamed(old, new)
    feature_cols = [col for col in df.columns if col != 'quality']
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    return assembler.transform(df).select("features", col("quality").cast("double").alias("label"))

def train_model():
    spark = SparkSession.builder.appName("WineQualityTraining").getOrCreate()

    training_path = "TrainingDataset.csv"
    training_data = prepare_data(spark, training_path)

    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=True)
    lr = LogisticRegression(featuresCol="scaledFeatures", labelCol="label", maxIter=10)

    pipeline = Pipeline(stages=[scaler, lr])
    model = pipeline.fit(training_data)

    predictions = model.transform(training_data)
    evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")

    f1_score = evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
    accuracy = evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"})

    print("[Train] F1 score =", f1_score)
    print("[Train] Accuracy =", accuracy)

    model.write().overwrite().save("/home/ec2-user/wine_model")

    spark.stop()

if __name__ == "__main__":
    train_model()

