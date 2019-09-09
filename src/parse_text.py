# -*- coding: utf-8 -*-
import re
import pandas as pd

# reading file
with open(r'data/raw/year_progress_copy.txt', 'r') as f:
    contents = f.read()

# splitting into tweets
whole_tweets_raw = re.compile(
    "^@year_progress$|^@dustinhorne$", flags=re.MULTILINE).split(contents)

# only selecting tweets with progress bars
whole_tweets = [t for t in whole_tweets_raw if ('▓' in t or '░' in t)]

tweets = [t.strip().split('\n') for t in whole_tweets]

# creating dataframe
df = pd.DataFrame({
    'date': [t[0] for t in tweets],
    'year_perc_raw': [t[2] for t in tweets],
    'stats': [t[4] for t in tweets]})

# filtering abnormal rows
# some 'non progress' tweets have been caught due to retweets/quotes etc
abnormal_rows = (
    ~df['year_perc_raw'].str.contains('%')
    | ~df['stats'].str.contains('likes'))

df = df.loc[~abnormal_rows]

# adding 2019 to current year tweets
# 2019 has been left of date stamps for current year - adding back in
no_year_rows = ~df['date'].str.contains(r'\d{4}$')
df.loc[no_year_rows, 'date'] = df.loc[no_year_rows, 'date'] + ' 2019'

# this rule is apparently broken for 31 Dec 2018 (also is missing a year)
# so the above logic has now called it 31 Dec 2019 erroneously
# fixing that
rows = df['date'] == 'Dec 31 2019'
df.loc[rows, 'date'] = 'Dec 31 2018'

# changing to date index
df['date'] = pd.to_datetime(df['date'])

# Extracting data from strings
df['year_perc'] = df['year_perc_raw'].str.extract(pat=r'(\d+)%$')

# get rid of all commas in stats
df['stats'] = df['stats'].str.replace(',', '')

df['replies'] = df['stats'].str.extract(pat=r'([\d]+) repl')
df['retweets'] = df['stats'].str.extract(pat=r'([\d]+) retweet')
df['likes'] = df['stats'].str.extract(pat=r'([\d]+) like')


df = df.loc[~pd.isna(df['year_perc_raw'])]

# converting to integers
try:
    df = df.astype({
        'year_perc': 'int',
        'replies': 'int',
        'retweets': 'int',
        'likes': 'int'})
except:
    breakpoint()

# dropping extraneous columns
df = df.drop([
    'year_perc_raw',
    'stats'], axis=1)

# writing out
df = df.reset_index(drop=True)
df.to_feather(r'data/interim/year_progress.feather')
