from nepalitokanizer import NepaliTokenizer
import argparse
import pandas as pd
from nepali_stemmer.stemmer import NepStemmer

# parser defination
parser = argparse.ArgumentParser(
    description="Tokenizes the main news", usage='%(prog)s [options]',)
parser.add_argument('--csv', '-c', help='This is a valid path to the CSV that you want to tokenize', required=True)
args = parser.parse_args()

CSV_PATH = args.csv

def get_tokens(text):
    my_tokenzier = NepaliTokenizer()
    stems = NepStemmer()
    no_stem_text = stems.stem(text)
    cleaned_string = my_tokenzier.remove_special_characters(no_stem_text)
    tokens = my_tokenzier.tokenizer(cleaned_string)
    return ','.join(tokens)


if __name__=='__main__':
    df = pd.read_csv(CSV_PATH, dtype=str)
    df = df.dropna()
    df['tokens'] = df['MAIN_NEWS'].apply(get_tokens)
    df.to_csv(CSV_PATH, index=False)
    print("Check the CSV")