# %% Reading data
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_feather(r'data/interim/year_progress.feather')

# %% [markdown]
# # Timelines
replies_fig = go.Scatter(
    x=df['date'],
    y=df['replies'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Replies')

likes_fig = go.Scatter(
    x=df['date'],
    y=df['likes'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Likes')

retweets_fig = go.Scatter(
    x=df['date'],
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

# %% [markdown]
# # Top 10:
top_replies = df.sort_values('replies', ascending=False)[
    ['date', 'year_perc', 'replies']].head(10)
top_likes = df.sort_values('likes', ascending=False)[
    ['date', 'year_perc', 'likes']].head(10)
top_retweets = df.sort_values('retweets', ascending=False)[
    ['date', 'year_perc', 'retweets']].head(10)

# %% [markdown]
# ## Top 10 Replied Tweets
top_replies

# %% [markdown]
# ## Top 10 Liked Tweets
top_likes

# %% [markdown]
# ## Top 10 Retweeted Tweets
top_retweets

# %% [markdown]
# # Feature Engineering
# Some patterns are emerging, will add some features to the dataset.

df['is_mod_25'] = df['year_perc'].apply(lambda x: x % 25 == 0)
df['is_mod_10'] = df['year_perc'].apply(lambda x: x % 10 == 0)
df['is_100'] = df['year_perc'] == 100
df['is_50'] = df['year_perc'] == 50
df['is_0'] = df['year_perc'] == 0
df['is_69'] = df['year_perc'] == 69
df['is_99'] = df['year_perc'] == 99
df.head()

# %% [markdown]
# # Correlation Heatmap
corr = df.drop('year_perc', axis=1).corr()

# do not want modulus measures as columns
corr = corr.drop([
    'is_mod_25',
    'is_mod_10',
    'is_100',
    'is_99',
    'is_69',
    'is_50',
    'is_0'
], axis=1)

# get rid of replies/retweets/likes for rows
corr = corr.drop([
    'likes',
    'retweets',
    'replies'])

data = [go.Heatmap(
    z=corr.values.tolist(),
    x=corr.columns.tolist(),
    y=corr.index.tolist(),
    type='heatmap',
    colorscale='Viridis')]

heatmap = go.Figure(data=data)
heatmap.show()
# %% [markdown]
# # Normalizing Measures
# Correlation is not as strong as it could be, as the twitter account "activity"
# has increased over time (thus eariler years weakens the correlation between percentage
# values and tweet responses)
#
# Can counteract this by normalizing account reactions per year - so that the normalized values
# take a range from 0 - 1, with 1 being the highest in a given year

year_max = df.groupby(df['date'].dt.year)[
    ['replies', 'retweets', 'likes']].max()


def normalize_reaction(row: pd.Series, reaction: str) -> float:
    year = row['date'].year
    react_max = year_max.loc[year, reaction]

    value = row[reaction]
    normalized = value / react_max

    return normalized


df['norm_replies'] = df.apply(normalize_reaction, axis=1, reaction='replies')
df['norm_retweets'] = df.apply(normalize_reaction, axis=1, reaction='retweets')
df['norm_likes'] = df.apply(normalize_reaction, axis=1, reaction='likes')

df.head()


# %% [markdown]
# # Correlating Normalized Reactions
norm_corr = df.drop([
    'year_perc',
    'likes',
    'retweets',
    'replies'], axis=1).corr()

reaction_fields = ['norm_likes', 'norm_retweets', 'norm_replies']

norm_corr = norm_corr.drop([
    'is_mod_25',
    'is_mod_10',
    'is_100',
    'is_99',
    'is_69',
    'is_50',
    'is_0'], axis=1)

norm_corr = norm_corr.drop(reaction_fields, axis=0)

norm_data = [go.Heatmap(
    z=norm_corr.values.tolist(),
    x=norm_corr.columns.tolist(),
    y=norm_corr.index.tolist(),
    type='heatmap',
    colorscale='Viridis')]

norm_heatmap = go.Figure(data=norm_data)
norm_heatmap.show()

# %%
