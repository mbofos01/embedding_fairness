import pickle
import os
from typing import Tuple, List


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
        with open(f'embeddings/{sentence}.1pkl', 'rb') as f:
            loaded_embedding = pickle.load(f)
    except Exception as e:
        print(e)
        return (sentence, None)

    return (sentence, loaded_embedding.data[0].embedding)


if __name__ == '__main__':
    embedding = read_embedding("The doctor called his friend")
    print(embedding)
