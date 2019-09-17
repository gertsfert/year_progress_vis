# %% Reading data
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_feather(r'data/interim/year_progress.feather')

# %% [markdown]
# # Timelines
REPLIES_COLOR = 'crimson'
LIKES_COLOR = 'darkmagenta'
RETWEETS_COLOR = 'dodgerblue'


replies_fig = go.Scatter(
    x=df['date'],
    y=df['replies'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Replies',
    yaxis="y1",
    line=dict(color=REPLIES_COLOR))

likes_fig = go.Scatter(
    x=df['date'],
    y=df['likes'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Likes',
    yaxis='y2',
    line=dict(color=LIKES_COLOR))

retweets_fig = go.Scatter(
    x=df['date'],
    y=df['retweets'],
    hovertext=df['year_perc'],
    hoverinfo='text',
    mode='lines',
    name='Retweets',
    yaxis="y3",
    line=dict(color=RETWEETS_COLOR))

fig = make_subplots(
    rows=3, cols=1,
    vertical_spacing=0.1,
    subplot_titles=("Replies", "Likes", "Retweets"))

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
# # Multiple Axes Test
multiple_axes_fig = go.Figure()

replies_fig.update(
    line=dict(
        color=REPLIES_COLOR,
        width=2,
        dash='dot'))

likes_fig.update(
    line=dict(
        color=LIKES_COLOR,
        width=3,
        dash='dash'))


multiple_axes_fig.add_trace(replies_fig)
multiple_axes_fig.add_trace(likes_fig)
multiple_axes_fig.add_trace(retweets_fig)

# Create Axis objects
multiple_axes_fig.update_layout(
    xaxis=dict(
        domain=[0.1, 1]
    ),

    yaxis=dict(
        title="Replies",
        titlefont=dict(
            color=REPLIES_COLOR),
        tickfont=dict(
            color=REPLIES_COLOR),
        position=0),
    yaxis2=dict(
        title="Likes",
        titlefont=dict(
            color=LIKES_COLOR),
        tickfont=dict(
            color=LIKES_COLOR),
        anchor="free",
        overlaying="y",
        side="left",
        position=0.1),
    yaxis3=dict(
        title="Retweets",
        titlefont=dict(
            color=RETWEETS_COLOR),
        tickfont=dict(
            color=RETWEETS_COLOR),
        anchor="free",
        overlaying="y",
        side="right",
        position=1
    )
)

# update layout properties
multiple_axes_fig.show()

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

# %% correlating reactions
corr = df.drop([
    'year_perc',
    'norm_likes',
    'norm_retweets',
    'norm_replies'], axis=1).corr()


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
    'replies'], axis=0)


# %% correlating normalized reactions
norm_corr = df.drop([
    'year_perc',
    'likes',
    'retweets',
    'replies'], axis=1).corr()

norm_corr = norm_corr.drop([
    'is_mod_25',
    'is_mod_10',
    'is_100',
    'is_99',
    'is_69',
    'is_50',
    'is_0'], axis=1)

norm_corr = norm_corr.drop([
    'norm_likes',
    'norm_retweets',
    'norm_replies'], axis=0)


# %% [markdown]
# # Correlation Heatmaps
max_corr = max(corr.max().max(), norm_corr.max().max())

corr_fig = make_subplots(
    rows=2, cols=1,
    vertical_spacing=0.1,
    subplot_titles=("Raw Reactions", "Normalized Reactions"))

corr_fig.append_trace(
    go.Heatmap(
        z=corr.values.tolist(),
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        type='heatmap',
        colorscale='Viridis',
        zmin=0,
        zmax=max_corr,
        showscale=False), 1, 1)

corr_fig.append_trace(
    go.Heatmap(
        z=norm_corr.values.tolist(),
        x=norm_corr.columns.tolist(),
        y=norm_corr.index.tolist(),
        type='heatmap',
        colorscale='Viridis',
        zmin=0,
        zmax=max_corr,
        showscale=True), 2, 1)

corr_fig.update_layout(
    height=900,
    width=800,
    title_text='Correlation Heatmaps')

corr_fig.show()


# %%
