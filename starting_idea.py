# You first need to install the OpenAI Python package
# pip install openai
# You also need to have an API key from OpenAI to use this package -> We have to figure this out
from openai import OpenAI

# This constructor uses the API key from the environment variable OPENAI_API_KEY
# Help can be found at https://platform.openai.com/docs/quickstart
client = OpenAI()

# This is the first example from the OpenAI documentation
# We are using the text-embedding-3-large model
# The input is a sentence and the output is the embedding of the sentence
embedding = client.embeddings.create(
    model = "text-embedding-3-large",
    input = "The doctor called his friend."
)

# We don't have the API key yet, so we can't run this code
print(embedding)