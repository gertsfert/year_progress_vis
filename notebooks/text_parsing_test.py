# This notebook is formatted in Visual Studio Code Format (cells delimited by # %%)
# %% [markdown]
# # Text Parsing - A Test

# %% [markdown]
# ## Reading File
test = []
with open(r'data/raw/year_progress_copy.txt', 'r') as f:
    contents = f.read()

# %% [markdown]
# ## Splitting into tweets
# Tweets are delimited by the line `@year_progress`
whole_tweets = contents.split('@year_progress')

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
