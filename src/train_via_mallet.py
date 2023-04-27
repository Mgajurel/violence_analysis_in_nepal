import little_mallet_wrapper
import seaborn
import glob
from pathlib import Path
import pandas as pd
import random
import os

path_to_mallet = os.path.join(os.path.dirname(__file__), "..", '..', 'Mallet-202108', 'bin', 'mallet')


pd.options.display.max_colwidth = 100
data_path = os.path.join(os.path.dirname(__file__), "..", "data","data.csv")
news_df = pd.read_csv(data_path)

#*************************TRAINING MODEL***********************************

# Ready Data
training_data = [' '.join(token.split(',')) for token in news_df['tokens']]
original_texts = [text for text in news_df['MAIN_NEWS']]
news_titles = [title for title in news_df['TITLE']]

# Ready train config
print(little_mallet_wrapper.print_dataset_stats(training_data))

num_topics = 15
output_directory_path = os.path.join('topic-model-output', 'news')

Path(f"{output_directory_path}").mkdir(parents=True, exist_ok=True)

path_to_training_data = f"{output_directory_path}/training.txt"
path_to_formatted_training_data = f"{output_directory_path}/mallet.training"
path_to_model = f"{output_directory_path}/mallet.model.{str(num_topics)}"
path_to_topic_keys = f"{output_directory_path}/mallet.topic_keys.{str(num_topics)}"
path_to_topic_distributions = f"{output_directory_path}/mallet.topic_distributions.{str(num_topics)}"

# Train
little_mallet_wrapper.quick_train_topic_model(path_to_mallet,
                                            output_directory_path,
                                            num_topics,
                                            training_data)

#*************************TRAINING MODEL***********************************
