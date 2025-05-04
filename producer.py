from kafka import KafkaProducer
import json
import pandas as pd
import os
import pickle
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ProducerApp").getOrCreate()

directory_path = 'dataset path' #excluded it for security reasons
# you can find the dataset path in the README file

# List all partitioned files, files that start with 'part-'
all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.startswith('part-')]
# Read each partitioned file into a list of DataFrames
df_list = [pd.read_csv(file) for file in all_files]
# Concatenate all DataFrames into one DataFrame
df = pd.concat(df_list, ignore_index=True)

print(f"Columns in testing dataset: {df.columns.tolist()}")

with open('onehot_encoder.pk1', 'rb') as f:
    encoder = pickle.load(f)

string_cols = df.select_dtypes(include=['object']).columns.drop('attack_cat')
encoded_data = encoder.transform(df[string_cols])

# Convert encoded data to a df
encoded_cols = encoder.get_feature_names_out(string_cols)
encoded_df = pd.DataFrame(encoded_data, columns=encoded_cols)
print(f"Columns after one hot encoding:{encoded_df.columns.tolist()}")
print(f"Columns:{len(encoded_df.columns)}")

df = pd.concat([df.drop(string_cols, axis=1), encoded_df], axis=1)

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Send each row to Kafka
for _, row in df.iterrows():
    data = {col: row[col] for col in row.index if pd.api.types.is_numeric_dtype(row[col]) or col in encoded_cols}
    print(f"Sending data: {data}")

    producer_output = producer.send('test-data', value=data)

    record_metadata = producer_output.get(timeout=10)  # Wait for 10 seconds
    print(f"Message sent to topic {record_metadata.topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")

# Flush producer to ensure all data is sent
producer.flush()
producer.close()
print("Data sent to Kafka topic 'test-data'.")
