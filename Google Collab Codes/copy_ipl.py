# -*- coding: utf-8 -*-
"""copy_IPL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n6fV4hmHmfLKYxbN_hq0wcmi3AtEjzD2
"""

import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

batting_data = pd.read_csv('/content/drive/MyDrive/IPL dataset/all_season_batting_card.csv')

bowling_data = pd.read_csv('/content/drive/MyDrive/IPL dataset/all_season_bowling_card.csv')
details_data = pd.read_csv('/content/drive/MyDrive/IPL dataset/all_season_details.csv')
summary_data = pd.read_csv('/content/drive/MyDrive/IPL dataset/all_season_summary.csv')
points_table = pd.read_csv('/content/drive/MyDrive/IPL dataset/points_table.csv')

pd.set_option('display.max_columns', None)

batting_data.head(5)

details_data.head()

bowling_data.head()

summary_data.head()

points_table.head()

points_table['season'] = points_table['season'].astype(float)

import matplotlib.pyplot as plt

# Filter the DataFrame for home wins
home_wins = summary_data[summary_data['winner'] == summary_data['home_team']]

# Group by home team and count the number of wins
team_wins = home_wins.groupby('home_team').size().reset_index(name='wins')

# Plotting
plt.figure(figsize=(12, 8))
plt.bar(team_wins['home_team'], team_wins['wins'], color='skyblue')
plt.xlabel('Team')
plt.ylabel('Number of Wins')
plt.title('Number of Wins for Each Team at Their Home Venues')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

plt.style.use('fivethirtyeight')
df_fil=summary_data[summary_data['toss_won']==summary_data['winner']]
slices=[len(df_fil),(577-len(df_fil))]
plt.pie(slices,labels=['Toss & win','Toss & lose'],startangle=90,shadow=True,explode=(0,0),autopct='%1.1f%%',colors=['r','g'])
fig = plt.gcf()
fig.set_size_inches(6,6)
plt.show()

import seaborn as sns
plt.figure(figsize=(16,6))
color_palette = sns.color_palette("Spectral")
sns.countplot(x='season', hue='decision', data=summary_data,palette=color_palette,saturation=1)
plt.title('Toss Decision in each Season of IPL');

# Filter the DataFrame for matches where teams chose to bowl first
bowl_first_matches = summary_data[summary_data['decision'] == 'BOWL FIRST']

# Count the number of wins for matches where teams chose to bowl first
bowl_first_wins = bowl_first_matches['winner'].value_counts()

# Filter the DataFrame for matches where teams chose to bat first
bat_first_matches =  summary_data[summary_data['decision'] == 'BAT FIRST']

# Count the number of wins for matches where teams chose to bat first
bat_first_wins = bat_first_matches['winner'].value_counts()

# Plotting
plt.figure(figsize=(12, 8))

# Plot bowl first wins
plt.bar(bowl_first_wins.index, bowl_first_wins.values, color='skyblue', label='Bowl First')

# Plot bat first wins
plt.bar(bat_first_wins.index, bat_first_wins.values, color='orange', label='Bat First')

plt.xlabel('Team')
plt.ylabel('Number of Wins')
plt.title('Number of Wins when Choosing to Bowl First vs Bat First')
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='winner', y='1st_inning_score', data=summary_data)
plt.title('Average 1st Inning Score by Winner')
plt.xlabel('Winner')
plt.ylabel('Average 1st Inning Score')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

summary_feats = summary_data[['id','home_team','away_team','toss_won','decision','winner','venue_id','home_runs','away_runs','home_wickets','away_wickets']].copy()
pt_feats = points_table[['season','short_name','matcheswon','nrr']].copy()
final_feats = pd.merge(summary_feats,pt_feats, left_on='home_team', right_on='short_name', how='right')

final_feats.head(50)

final_feats.shape

final_feats.isnull().sum()

final_feats.dropna(inplace=True)

final_feats.shape

final_feats.isnull().sum()

#Preprocessing
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

label_encoder = LabelEncoder()

# Encode each categorical column
for column in final_feats.columns:
    if final_feats[column].dtype == 'object':
        final_feats[column] = label_encoder.fit_transform(final_feats[column])

final_feats.head(30)

import seaborn as sns
import matplotlib.pyplot as plt

# Calculate correlation matrix
corr = final_feats.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
plt.title('Correlation Matrix')
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

X = final_feats[['home_team', 'away_team', 'toss_won']]
y = final_feats['winner']

# Standard scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Random Forest Classifier
rf_classifier = RandomForestClassifier()

# Fitting the model
rf_classifier.fit(X_train, y_train)

# Predicting the test set results
y_pred = rf_classifier.predict(X_test)

# Evaluating the model
accuracy = (y_pred == y_test).mean()
print(f"Accuracy: {accuracy}")

print(batting_data.dtypes)

batting_data['strikeRate'].dtype

batting_data['strikeRate'].isnull().sum()

batting_data.shape

batting_data['strikeRate'] = pd.to_numeric(batting_data['strikeRate'],errors='coerce')

average_strike_rate_team = batting_data.groupby(['match_id', 'current_innings'])['strikeRate'].mean().reset_index()
print(average_strike_rate_team)

for column in average_strike_rate_team.columns:
    if average_strike_rate_team[column].dtype == 'object':
        average_strike_rate_team[column] = label_encoder.fit_transform(average_strike_rate_team[column])

average_strike_rate_team.head()

final_feats1 = pd.merge(final_feats,average_strike_rate_team,left_on='id', right_on='match_id', how='left')
final_feats1.head()

corr = final_feats1.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
plt.title('Correlation Matrix')
plt.show()

X = final_feats1[['home_team', 'away_team','decision', 'toss_won','nrr','strikeRate']]
y = final_feats1['winner']

# Standard scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Random Forest Classifier
rf_classifier = RandomForestClassifier()

# Fitting the model
rf_classifier.fit(X_train, y_train)

# Predicting the test set results
y_pred = rf_classifier.predict(X_test)

# Evaluating the model
accuracy = (y_pred == y_test).mean()
print(f"Accuracy: {accuracy}")

bowling_data['economyRate'].dtype

bowling_data['economyRate'] = pd.to_numeric(bowling_data['economyRate'],errors='coerce')

team_economy_rate = bowling_data.groupby('match_id')['economyRate'].mean()

print(team_economy_rate)

team_economic_rate = bowling_data.groupby(['match_id', 'bowling_team'])['economyRate'].mean().reset_index()
print(team_economic_rate)

for column in team_economic_rate.columns:
    if team_economic_rate[column].dtype == 'object':
        team_economic_rate[column] = label_encoder.fit_transform(team_economic_rate[column])

team_economic_rate.head()

final_feats2 = pd.merge(final_feats1,team_economic_rate,left_on='id', right_on='match_id', how='left')
final_feats2.head()

corr = final_feats2.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
plt.title('Correlation Matrix')
plt.show()

X = final_feats2[['home_team','away_team','venue_id','toss_won','decision','nrr']]
y = final_feats2['winner']

# Standard scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Random Forest Classifier
rf_classifier = RandomForestClassifier()

# Fitting the model
rf_classifier.fit(X_train, y_train)

# Predicting the test set results
y_pred = rf_classifier.predict(X_test)

# Evaluating the model
accuracy = (y_pred == y_test).mean()
print(f"Accuracy: {accuracy}")

from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

xgb_classifier = XGBClassifier()

# Fitting the model
xgb_classifier.fit(X_train, y_train)

# Predicting the test set results
y_pred = xgb_classifier.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

final_feats2.head(200)

input_data = {
    'home_team': 3,
    'away_team': 0,
    'venue_id': 57851,
    'toss_won': 3,
    'decision': 1,
    'nrr': 0.809
}

input_features = scaler.transform(pd.DataFrame(input_data, index=[0]))


predicted_winner = rf_classifier.predict(input_features)[0]

#stpredicted_winner = label_encoder.inverse_transform(predicted_winner)
print("Predicted Winner:", predicted_winner)

input_data = {
    'home_team': 4,
    'away_team': 1,
    'venue_id': 57980,
    'toss_won': 4,
    'decision': 0,
    'nrr': 2.518
}

input_features = scaler.transform(pd.DataFrame(input_data, index=[0]))

predicted_winner = rf_classifier.predict(input_features)[0]

predicted_winner_team = label_encoder.inverse_transform([predicted_winner])[0]
print("Predicted Winner:", predicted_winner_team)

input_data = {
    'home_team': 4,
    'away_team': 1,
    'venue_id': 57980,
    'toss_won': 4,
    'decision': 0,
    'nrr': 2.518
}

input_features = scaler.transform(pd.DataFrame(input_data, index=[0]))

predicted_winner = xgb_classifier.predict(input_features)[0]

predicted_winner_team = label_encoder.inverse_transform([predicted_winner])[0]
print("Predicted Winner:", predicted_winner_team)

original_values_encoded = label_encoder.classes_

print("Original values encoded for each team:")
for encoded_value, team in enumerate(original_values_encoded):
    print(f"{team}: {encoded_value}")

distinct_venues = summary_data[['venue_name', 'venue_id']].drop_duplicates()

# Print distinct list of venues with their respective IDs
print(distinct_venues)