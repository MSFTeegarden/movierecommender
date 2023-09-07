# Movie Recommender App

## Overview
This repo contains an example demonstrated at [Azure Python Day 2023](https://learn.microsoft.com/en-us/events/learn-events/azuredevelopers-pythonday/) in the **How to build a practical AI app with Python, Redis, and OpenAI** session. 

`app.py` contains the main Streamlit application 
`langchain.ipynb` is a juptyer notebook walking through the process of ingesting the data into pandas, filtering it, generating embeddings, loading into Redis, and performing search queries. You might want to start here :)

## Prerequsites
- An Azure OpenAI Service instance, with the text-embedding-ada-002 (version 2) model deployed
  - You may need to apply for access if access is still being restricted. 
- An Azure Cache for Redis instance
  - You must use an Enterprise tier instance (e.g. E5, E10, etc.)
  - You must provision the instance using the `Enterprise` cluster policy and with the `RediSearch` module installed.
- If running locally, you must configure the environment variables for the OpenAI key, models, and endpoints, plus the Redis key and endpoint.
- If deploying through a container, you must configure the environement variables in the Dockerfile.

The _Movie Recommender_ application (e.g. `app.py`) expects that the Redis instance already has embeddings loaded and a search index established. You may want to run the jupyter notebook first so this is set up.

## Deploying to Azure
[az-containerapp-up](https://learn.microsoft.com/en-us/cli/azure/containerapp?view=azure-cli-latest#az-containerapp-up) is an extremely convenient way to deploy to an Azure Container App instance. All you need is the dockerfile and an Azure subscription!

## Questions
This repo is a work in progress. If you have questions, please feel free to email azurecachepm@microsoft.com

## License Details
`wiki_movie_plots_1970to2017.csv` (c) by JustinR

Original data source: [Wikipedia Movie Plots - Kaggle](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots)

Data was modified to filter for only entries from 1970 or later, and take only films from America, Australia, Canada, and Britain. 

`wiki_movie_plots_1970to2017.csv` is licensed under a
Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

All other work is licensed under the MIT license. 
