# Network-Anomaly-Detection-Tool

GOAL

The project aims to create a network anomaly detection tool that processes network traffic data, cleans the data, applies pre-processing steps, and trains a machine learning model to classify network traffic and detect threats. The tool was trained through  large datasets and apply techniques such as outlier detection, data encoding, and using machine learning classification models to detect malicious network behaviour.

Project Structure

Data Cleaning

The tool handles missing values, duplicates, inconsistent formatting, and outliers in the dataset. Categorical data is also encoded using StringIndexer.

Data Preprocessing

Visualize the cleaned data and generate basic descriptive statistics. A histogram is also generated to show the distribution of features.

Model Training

The tool uses RandomForestClassifier from scikit-learn to classify the network traffic into different attack categories. Before training, categorical values are encoded using one-hot encoding.

Simulating Network Traffic 

While this project works on static datasets, integrating tools like TCP replay for real-time network traffic simulation is possible to create a more dynamic testing environment.

The full simulation test will be detailed during the deployment phase in the later stages of the project

Tools and Libraries

•	PySpark: Used for handling large datasets and performing data cleaning tasks on a distributed system.
•	pandas: For data manipulation and analysis.
•	matplotlib and seaborn: For data visualization.
•	scikit-learn: Machine learning algorithms, including RandomForestClassifier for classification tasks.
•	Python: General-purpose programming language used for all tasks.

Installation

To get started with this project, you need to have Python installed. You can install the required libraries using pip:


 install pyspark
 install pandas
 install scikit-learn
 install matplotlib seaborn
 the Dataset

This project uses the UNSW-NB15 dataset, which can be downloaded from Kaggle. The dataset contains labelled network traffic with attack categories and normal behavior. It was split into training and testing data.  The dataset is provided in .parquet format.

How to Run the Project:

Data Cleaning:

Load the dataset using the DataCleaning class. This class will handle missing values, outliers, and duplicates.
data_cleaning = DataCleaning('path_to_dataset.parquet')
data_cleaning.handle_missing_values()
data_cleaning.handle_duplicates()
data_cleaning.handle_outliers()
data_cleaning.encode_categorical_values()
cleaned_df = data_cleaning.return_cleaned_data()

Data Preprocessing:

Visualize the cleaned dataset using the DataPreprocessing class.
data_preprocessing = DataPreprocessing(cleaned_df)
data_preprocessing.visualize_data()

Model Training:

Use the TrainModel class to apply one-hot encoding and train a RandomForestClassifier on the data.
train_model = TrainModel(cleaned_df)
train_model.one_hot_encoding()
train_model.train_model()

Save Cleaned Dataset:

The cleaned dataset can be saved as a CSV file for further analysis or re-use.
cleaned_df.coalesce(1).write.csv("cleaned_dataset.csv", header=True)

•	Additional Algorithms:

Explore other machine learning algorithms, such as neural networks or gradient boosting, to improve classification accuracy.

Conclusion

This tool provides an efficient way to clean and preprocess network traffic data, train machine learning models, and detect network anomalies. By incorporating real-time data simulation, it can be further enhanced to handle real-world network security challenges which will be handled in later stages.
