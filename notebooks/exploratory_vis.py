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

# %%
top_replies

# %%
top_likes

# %%
top_retweets

# %%
