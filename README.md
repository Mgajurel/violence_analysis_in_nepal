# violence_analysis_in_nepal
Project to study violence based on Nepali news about violence

## USAGE

1. If you find new districts, new stop words or new suffix, add them in the script nepalitokanizer.py
2. then run myTokenizer.py as follows
```
python myTokenizer.py -c insec_online_first_lockdown.csv
```
The above code will change the tokens in insec_online_first_lockdown.csv.
Do this for other csv as well.

3. Add all the rows from all csv to data.csv which will be used to train the model


## Model Training and usage

1. After making changes to data.csv
2. Running the following command will train your model based on data.csv 
```
python train_via_mallet
```
3. The above code will create topic-model-output folder with all information for training
4. Use analysis.py to use the models described in 3