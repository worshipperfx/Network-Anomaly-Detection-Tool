# Network-Anomaly-Detection-Tool


## Goal

This tool is designed to detect unusual network activity in real-time using machine learning. It flags anomalies such as DDoS attacks, fuzzers, exploits, and botnet traffic. By learning normal network behavior patterns, the tool identifies threats without relying on manual inspection or static rule-based systems.

The project builds an intelligent network anomaly detection system that processes network traffic data, cleans and transforms it, trains a machine learning model, and performs real-time threat detection. It uses Kafka for streaming, PySpark and Pandas for preprocessing, and a RandomForestClassifier to identify and classify threats as they occur.

## What the Project Does

- Ingests labeled network traffic from the UNSW-NB15 dataset
- Cleans and preprocesses data with outlier detection, duplicate removal, missing value handling, and categorical encoding
- Trains a machine learning model on the cleaned data
- Streams test data using Apache Kafka, mimicking real-time network traffic
- Sends data to a consumer, which makes predictions using the trained model
- Flags abnormal behavior and potential threats

## Kafka-Based Real-Time Pipeline

The real-time component uses a Kafka pipeline to simulate network traffic and feed it into the ML model:

1. **Producer**:
   - Loads the testing dataset and one-hot encodes it using a pretrained encoder
   - Streams encoded data to Kafka topics as simulated real-time network traffic

2. **Kafka Topics & Brokers**:
   - Kafka brokers store and distribute the data across topics
   - Ensures fault tolerance and scalability in the streaming process

3. **Consumer**:
   - Listens to Kafka topics, loads the trained model, and predicts whether incoming traffic is normal or anomalous
   - Outputs classifications like Normal, DoS, Fuzzers, etc.

## Project Structure

### Data Cleaning

- Removes missing values, duplicates, and outliers using PySpark
- Encodes categorical features using StringIndexer

### Data Preprocessing

- Converts Spark DataFrame to Pandas
- Uses `.describe()` and `.hist()` for statistical summaries and visualizations

### Model Training

- Applies OneHotEncoder to categorical features
- Trains a RandomForestClassifier with scikit-learn
- Saves the model using `pickle` for use in real-time predictions

### Real-Time Streaming Simulation

- Testing dataset is streamed as real-time data using Kafka
- Consumer picks the messages and performs live predictions using the trained model

## Datasets Used

- **Testing Dataset (for streaming)**:  
  [UNSW-NB15 Testing Set – Kaggle](https://www.kaggle.com/datasets/marvellouschitenga/unsw-nb15-testing-set-parquet-4-54-mb)

- **Training Dataset (despite “testing” in the link)**:  
  [NADT Training Dataset – Kaggle](https://www.kaggle.com/datasets/marvellouschitenga/nadttesting)

## Tools and Libraries

- PySpark – Distributed data processing and cleaning
- pandas – Data manipulation
- matplotlib & seaborn – Data visualization
- scikit-learn – Machine learning (RandomForestClassifier)
- Apache Kafka – Real-time data streaming
- Python – Core programming


## Full Project Documentation

For a deep technical breakdown including architecture diagrams, setup steps, and debugging notes, refer to:  
**`Network Anomaly Detection Tool__Project Documentation_.pdf`** in this repository.

Conclusion

This tool provides an efficient way to clean and preprocess network traffic data, train machine learning models, and detect network anomalies. By incorporating real-time data simulation, it can be further enhanced to handle real-world network security challenges which will be handled in later stages.
