from openai import OpenAI
import pickle
import os
from typing import Tuple, List

client = OpenAI()


def read_embedding(sentence: str) -> Tuple[str, List[float]]:
    """
    Reads the embedding for a given sentence.

    Args:
        sentence (str): The sentence for which the embedding is to be read.

    Returns:
        tuple[str, list[float]]: A tuple containing the sentence and its embedding.

    """
    if f"{sentence}.pkl" not in os.listdir("embeddings"):
        return None

    try:
        with open(f'embeddings/{sentence}.pkl', 'rb') as f:
            loaded_embedding = pickle.load(f)
    except Exception as e:
        print(e)
        return (sentence, None)

    return (sentence, loaded_embedding.data[0].embedding)


def generate_embedding(model_used: str = "text-embedding-3-large", sentence: str = "The doctor called his friend", save_to_file: bool = True, force_recompute: bool = False) -> Tuple[str, List[float]]:
    """
    Generate an embedding for a given sentence using a specified model.

    Args:
        model_used (str): The name of the model to be used for generating the embedding. Default is "text-embedding-3-large".
        sentence (str): The input sentence for which the embedding needs to be generated. Default is "The doctor called his friend".
        save_to_file (bool): Whether to save the generated embedding to a file. Default is True.
        force_recompute (bool): Whether to force recomputation of the embedding even if it already exists in the "embeddings" directory. Default is False.

    Returns:
        tuple[str, list[float]]: A tuple containing the input sentence and the generated embedding as a list of floats.

    """
    if f"{sentence}.pkl" in os.listdir("embeddings") and not force_recompute:
        return read_embedding(sentence)

    generated_embedding = client.embeddings.create(
        model=model_used, input=[sentence])

    if save_to_file:
        with open(f"embeddings/{sentence}.pkl", 'wb') as f:
            pickle.dump(generated_embedding, f)

    return (sentence, generated_embedding.data[0].embedding)


if __name__ == '__main__':
    generate_embedding(
        sentence="The doctor called his friend", save_to_file=True)
