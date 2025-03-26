import tensorflow as tf
import os
import pandas as pd
import numpy as np

zip_path = tf.keras.utils.get_file(
    origin='https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip',
    fname='jena_climate_2009_2016.csv.zip',
    extract=True
)

extracted_dir = os.path.splitext(zip_path)[0]
csv_path = os.path.join(extracted_dir, "jena_climate_2009_2016.csv")

# Read the CSV file
df = pd.read_csv(csv_path)
print(df.head())
