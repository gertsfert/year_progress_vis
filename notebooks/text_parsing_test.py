# This notebook is formatted in Visual Studio Code Format (cells delimited by # %%)
# %% [markdown]
# # Text Parsing - A Test
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
whole_tweets_raw = re.compile(
    "^@year_progress$|^@dustinhorne$", flags=re.MULTILINE).split(contents)

# %% [markdown]
# ## Only selecting tweets with progress bars
whole_tweets = [t for t in whole_tweets_raw if ('▓' in t or '░' in t)]

# %% [markdown]
# ## Tweet parts are delimited by linebreaks
# Create 2d list using comprehension
tweets = [t.strip().split('\n') for t in whole_tweets]

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
# ## Extracting Data From Strings

df['year_perc'] = df['year_perc_raw'].str.extract(pat=r'(\d+)%$')


# get rid of all commas in stats
df['stats'] = df['stats'].str.replace(',', '')

df['replies'] = df['stats'].str.extract(pat=r'([\d]+) repl')
df['retweets'] = df['stats'].str.extract(pat=r'([\d]+) retweet')
df['likes'] = df['stats'].str.extract(pat=r'([\d]+) like')

# converting to integers
df = df.astype({
    'year_perc': 'int',
    'replies': 'int',
    'retweets': 'int',
    'likes': 'int'})

df.sample(10)

# %% [markdown]
# ## Fixing 31 Dec 2019
# For some reason, 31 Dec 2018 did not have a year attached,
# as a result previous logic assigned it the year 2019 (which is incorrect)
# changing year for these rows
rows = df['date'] == 'Dec 31 2019'

df.loc[rows, 'date'] = df.loc[rows, 'date'].str.replace('2019', '2018')


# %% [markdown]
# ## Changing To Date Index
df['date'] = pd.to_datetime(df['date'])
df = df.set_index(df['date'])

df = df.sort_index()

df.tail()


# %% [markdown]
# ## Dropping Extranious Columns
df = df.drop([
    'date',
    'year_perc_raw',
    'stats'], axis=1)

df.sample(20)

# %% Visulising for the hell of it

replies_fig = go.Scatter(
    x=df.index,
    y=df['replies'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Replies')

likes_fig = go.Scatter(
    x=df.index,
    y=df['likes'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Likes')

retweets_fig = go.Scatter(
    x=df.index,
    y=df['retweets'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Retweets')

fig = make_subplots(
    rows=3, cols=1,
    vertical_spacing=0.1)

fig.append_trace(replies_fig, 1, 1)
fig.append_trace(likes_fig, 2, 1)
fig.append_trace(retweets_fig, 3, 1)


fig.update_layout(
    height=900,
    width=800,
    title_text='Year Progress Twitter Account'
)


fig.show()

# %%
