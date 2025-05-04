import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, isnan, count, mean, stddev
from pyspark.ml.feature import StringIndexer, OneHotEncoder

class DataCleaning:
    def __init__(self, dataset_path):
        self.spark = SparkSession.builder.appName("DataCleaning").getOrCreate()
        self.df = self.spark.read.parquet(dataset_path, header = True, inferSchema= True)

    def drop_proto_index(self):
        print("Before dropping:", self.df.columns)
        self.df = self.df.drop('proto_index') #drop proto_index as it is non - existant in testing df
        self.df = self.df.cache()
        self.df.show(5)  # Force evaluation
        print("After dropping:", self.df.columns)
        return self.df

    def handle_missing_values(self):
        print("Before handling missing values:", self.df.columns) 
        missing_values = self.df.select(
        [count(when(col(c).isNull() | (col(c).isNotNull() if c not in self.df.columns else isnan(c)), c)).alias(c) 
         for c in self.df.columns])
    
        missing_values.show()
        
        # Fill missing values with mean for numeric columns
        numeric_cols = [c for c, dtype in self.df.dtypes if dtype in ['int', 'double']]
        for col_name in numeric_cols:
            mean_value = self.df.select(mean(col_name)).collect()[0][0]
            self.df = self.df.na.fill({col_name: mean_value})
        self.df.show(5)  # Force evaluation again
        print("After handling missing values:", self.df.columns)
        return self.df

    def handle_duplicates(self):
        self.df = self.df.dropDuplicates()
        return self.df

    def inconsistent_formatting(self):
        self.df = self.df.withColumn("column_name", col("column_name").lower().trim())
        return self.df

    def handle_outliers(self):
        numeric_cols = [c for c, dtype in self.df.dtypes if dtype in ['int', 'double']]
        for col_name in numeric_cols:
            stats = self.df.select(mean(col_name), stddev(col_name)).first()
            mean_value = stats[0]
            stddev_value = stats[1]
            self.df = self.df.filter((col(col_name)> (mean_value - 3 * stddev_value)) & (col(col_name)< (mean_value + 3 * stddev_value)))
        return self.df

    def encode_categorical_values(self):
       string_cols = [c for c, dtype in self.df.dtypes if dtype == 'string']
       for col_name in string_cols:
           indexer = StringIndexer(inputCol=col_name, outputCol=col_name + "_index")
           self.df = indexer.fit(self.df).transform(self.df)
           print("After encoding categorical values:", self.df.columns)
           return self.df

    def return_cleaned_data(self):
        return self.df

class DataPreprocessing:
    def __init__(self, cleaned_df):
        self.df = cleaned_df.toPandas()

    def visualize_data(self):
        few_rows = self.df.head()
        print(few_rows)
        
        data_description = self.df.describe()
        print(data_description)
        
        #plot a histogram for the data
        self.df.hist(figsize=(10, 10), bins=20)
        plt.show()

data_cleaning = DataCleaning('/home/chitengamarvellous/UNSW_NB15_training-set.parquet')
data_cleaning.drop_proto_index()
data_cleaning.handle_missing_values()
data_cleaning.handle_duplicates()
data_cleaning.handle_outliers()
data_cleaning.encode_categorical_values()

cleaned_df = data_cleaning.return_cleaned_data()
print(f"Cleaned dataframe:{cleaned_df}")

data_preprocessing = DataPreprocessing(cleaned_df)
data_preprocessing.visualize_data()
print(f"Prepocessed Data:{data_preprocessing}")

rows = cleaned_df.count()
print(rows)
columns = len(cleaned_df.columns)
print(columns)
print(cleaned_df.columns)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class TrainModel:
    def __init__(self, training_df):
        self.df = training_df
        self.encoder = None

    def one_hot_encoding(self):
        string_cols = self.df.select_dtypes(include=['object']).columns.drop('attack_cat') # target label to be non - encoded
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        # Encode string columns
        transformed_data = self.encoder.fit_transform(self.df[string_cols])
        encoded_cols = self.encoder.get_feature_names_out(string_cols)
        encoded_df = pd.DataFrame(transformed_data, columns=encoded_cols, index=self.df.index)
        print(len(encoded_cols))
        print(len(encoded_df))
        self.df = self.df.drop(columns=string_cols)
        self.df = pd.concat([encoded_df, self.df['attack_cat']], axis=1)
        with open('onehot_encoder.pk1', 'wb') as f:
            pickle.dump(self.encoder, f)
        return self.df.columns.tolist()

    def train_model(self):
        # Drop attack_cat only from features (X), not from the target variable (y)
        X = self.df.drop('attack_cat', axis=1)
        print(f"Number of features used to train the model: {X.shape[1]}")
        print(f"Features used to train the model: {list(X.columns)}")
        y = self.df['attack_cat']

        # Split the dataset into training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # predictions
        y_pred = model.predict(X_test)

        # Output classification results with actual class names
        print("Classification result: \n", classification_report(y_test, y_pred))

        feature_importances = pd.DataFrame(model.feature_importances_, index=X.columns, columns=['importance']).sort_values('importance', ascending=False)
        print("\nFeature Importance: \n", feature_importances)
        with open('network_model.pk3', 'wb') as m:
            pickle.dump(model, m)
        print("Model saved to 'network_model.pk3'")

train_model = TrainModel(cleaned_df.toPandas())
train_model.one_hot_encoding()
train_model.train_model()
