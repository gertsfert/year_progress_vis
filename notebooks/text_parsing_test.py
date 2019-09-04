# This notebook is formatted in Visual Studio Code Format (cells delimited by # %%)
# %% [markdown]
# # Text Parsing - A Test
import re

import pandas as pd


# %% [markdown]
# ## Reading File
test = []
with open(r'data/raw/year_progress_copy.txt', 'r') as f:
    contents = f.read()

# %% [markdown]
# ## Splitting into tweets
# Tweets are delimited by the line `@year_progress`
# as well as `@dustinhorne` (random reply in the mix)
whole_tweets = re.compile(
    "^@year_progress$|^@dustinhorne$", flags=re.MULTILINE).split(contents)

# %% [markdown]
# ## Only selecting tweets with progress bars
whole_tweets = [t for t in whole_tweets if ('▓' in t or '░' in t)]

# %% [markdown]
# ## Tweet parts are delimited by linebreaks
# Create 2d list using comprehension
tweets = [t.strip().split('\n') for t in whole_tweets]

# %% [markdown]
# ## Looking at the size of these tweets
lens = pd.Series([len(t) for t in tweets], name='tweet_lengths')

lens.value_counts()

# %% [markdown]
# ## Examining abnormally shaped tweets
abnormal_indexes = lens.loc[lens != 9].index

abnormal = [tweets[index] for index in abnormal_indexes]
# %% [markdown]
# ## Getting Data
# Want to extract the following data from each tweet
# - Date: Index 0
# - Year Percentage: Index 2
# - Replies: Index 4
# - Retweets: Index 4
# - Likes: Index 4

df = pd.DataFrame({
    'date': [t[0] for t in tweets],
    'year_perc_raw': [t[2] for t in tweets],
    'stats': [t[4] for t in tweets]})

pd.concat([df.head(), df.tail()])

# %% [markdown]
# ## Filtering Abnormal Tweets
abnormal_rows = (
    ~df['year_perc_raw'].str.contains('%')
    | ~df['stats'].str.contains('likes'))

abnormal = df.loc[abnormal_rows]
df = df.loc[~abnormal_rows]

abnormal
# %% [markdown]
# ## Adding 2019 to Current Year Tweets
# Year is left off date stamps for current year - lets
# add it back in eh?
no_year_rows = ~df['date'].str.contains(r'\d{4}$')
df.loc[no_year_rows, 'date'] = df.loc[no_year_rows, 'date'] + ' 2019'

df.head()
# %% [markdown]
# ## Extracting Percentage
