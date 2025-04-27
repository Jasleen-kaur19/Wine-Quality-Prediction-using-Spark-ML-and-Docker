from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import PipelineModel
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import logging

def load_and_prepare_test_data(spark, file_path):
    df = spark.read.csv(file_path, header=True, inferSchema=True, sep=";")
    for old in df.columns:
        new = old.replace('"', '').strip()
        df = df.withColumnRenamed(old, new)
    feature_cols = [c for c in df.columns if c != 'quality']
    df = df.withColumn("label", col("quality").cast("double"))
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    return assembler.transform(df)

def test_model():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    spark = SparkSession.builder.appName("WineQualityTesting").getOrCreate()

    test_path = "ValidationDataset.csv"
    model_path = "/home/ec2-user/wine_model"

    try:
        # Load test data
        logger.info("Loading test dataset...")
        test_data = load_and_prepare_test_data(spark, test_path)

        # Load saved model pipeline
        logger.info(f"Loading model from {model_path}")
        model = PipelineModel.load(model_path)

        # Predict and evaluate
        logger.info("Generating predictions...")
        predictions = model.transform(test_data)
        predictions.select("label", "prediction").show(10)

        # Evaluate model
        evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")
        f1_score = evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
        accuracy = evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"})

        print("[Test] F1 score =", f1_score)
        print("[Test] Accuracy =", accuracy)

    except Exception as e:
        logger.error("Error occurred: %s", e, exc_info=True)
    finally:
	spark.stop()

if __name__ == "__main__":
    test_model()

