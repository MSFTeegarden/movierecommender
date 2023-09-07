import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.redis import Redis as RedisVectorStore
import pandas as pd
from bing_image_urls import bing_image_urls
from langchain.vectorstores.redis import RedisText, RedisNum
import os


# ----------Set up Azure OpenAI Embeddings--------------

OPENAI_ENDPOINT = os.environ.get("OPENAI_ENDPOINT")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
DEPLOYMENT_NAME = os.environ.get("DEPLOYMENT_NAME")
MODEL_NAME = os.environ.get("MODEL_NAME")

embedding = OpenAIEmbeddings(
    deployment= DEPLOYMENT_NAME,        # your name for the model deployment (e.g. "my-ml-model")
    model= MODEL_NAME,                  # name of the specific ML model (e.g. "text-embedding-ada-002" )
    openai_api_base= OPENAI_ENDPOINT,
    openai_api_type= "azure",           # you need this if you're using Azure Open AI service
    openai_api_key= OPENAI_KEY,
    openai_api_version= "2023-05-15",
    chunk_size=16                       # current limit with Azure OpenAI service. This will likely increase in the future.
    )


# ----------Set up Redis Vector Store--------------
index_name = "movieindex"

REDIS_ENDPOINT = os.environ.get("REDIS_ENDPOINT") # must include port at the end. e.g. "redisdemo.eastus.redisenterprise.cache.azure.net:10000"
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

# create a connection string for the Redis Vector Store. Uses Redis-py format: https://redis-py.readthedocs.io/en/stable/connections.html#redis.Redis.from_url
# This example assumes TLS is enabled. If not, use "redis://" instead of "rediss://
redis_url = "rediss://:" + REDIS_PASSWORD + "@"+ REDIS_ENDPOINT

# You'll need to pass in the schema of your Redis Vector Store. You can generate this yaml file when you generate the embeddings and vector store.
vectorstore = RedisVectorStore.from_existing_index(
    embedding=embedding,
    redis_url=redis_url,
    index_name=index_name,
    schema="redis_schema.yaml"
)

# ----------Configure dataframe display configuration--------------

df = pd.DataFrame()

column_configuration = {
    "Title": st.column_config.TextColumn(
        "Title", help="The name of the movie", max_chars=100
    ),
    "Score": st.column_config.NumberColumn(
        "Score", help="Cosine simiuarity score"
    ),
    "Director": st.column_config.TextColumn(
        "Director", help="The name of the director(s)", max_chars=100
    ),
    "Cast": st.column_config.TextColumn(
        "Cast", help="The top billed cast", max_chars=100
    ),
    "Genre": st.column_config.TextColumn(
        "Genre", help="Movie genre(s)", max_chars=50
    ),
    "Wikipage": st.column_config.LinkColumn(
        "Wikipage", help="Wikipedia link"
    ),
    "year": st.column_config.TextColumn(
        "Year", help="Year of release", max_chars=50
    ),
   "origin": st.column_config.TextColumn(
        "Country", help="Country of origin", max_chars=50
    ),
}

# by default, the vectorstore returns cosine distance. This function converts it to a similarity score
def convertosimilarity(score):
    return 1 - score


# ----------Streamlit app----------

st.title('Movie Recommendation App 🎞️🍿')

with st.form('main_form'):
    # Text box for query input
    query = st.text_input("What kind of movie are you looking for?")
    
    # Slider for number of results
    num_results = st.slider("Number of results:", min_value=1, max_value=10, value=5)
    
    # Expandable section for additional filters
    with st.expander("Additional filters"):
        
        movie_year = st.slider("Year of release:", min_value=1970, max_value=2017, value=(1970, 2017))
        
        genreoptions = ('all', 'action', 'drama', 'animated', 'thriller', 'romance', 'family', 'horror', 'science fiction', 'documentary', 'western')
        genre = st.selectbox(label='Movie genre', options = genreoptions)

    # Submit button
    submitted = st.form_submit_button('Search')

    if submitted:
        
        # filter results based on filter parameters
        is_genre = RedisText("Genre") == genre
        is_year = (RedisNum("year") >= movie_year[0]) & (RedisNum("year") <= movie_year[1])

        # if genre is 'all', only filter on year
        if genre == 'all':
            is_filter = is_year
        else:
            is_filter = is_genre & is_year

        # perform vector search
        results = vectorstore.similarity_search_with_score(query, k=num_results, filter=is_filter)
  
        topanswer = results[0][0].metadata['Title']
        topwikipage = results[0][0].metadata['Wiki Page']
        topscore = results[0][1]

        # get movie poster image URL
        posterquery = topanswer + " movie poster"
        url = bing_image_urls(posterquery, limit=1)[0]

        # display top result
        st.header("Your top result:")
        st.divider()
        st.subheader(topanswer)
        st.image(url, width=200)
        st.write("Wikipedia page: " + topwikipage)
        st.write("Score: " + str(convertosimilarity(topscore)))

        # add the cosine similarity score to dataframe
        scorelist = []

        for movie, score in results:
            df.loc[len(df.index), list(movie.metadata.keys())] = list(movie.metadata.values())
            scorelist.append(convertosimilarity(score))

        df.insert(0, 'Score', scorelist)

        # drop columns that are not needed
        df = df.drop(columns=['id', 'n_tokens'])

        # display all results using a dataframe
        st.divider()
        st.write("All results:")
        st.dataframe(df, hide_index=True, column_config=column_configuration)
    


