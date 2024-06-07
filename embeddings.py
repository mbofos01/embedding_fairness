import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
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
    # Check if loaded_embedding has property data
    if hasattr(loaded_embedding, "data"):
        loaded_embedding = loaded_embedding.data[0]
    return (sentence, loaded_embedding.embedding)


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

def generate_embedding_bulk(model_used: str = "text-embedding-3-large", sentences: List[str] = ["The doctor called his friend"], save_to_file: bool = True, force_recompute: bool = False) -> List[Tuple[str, List[float]]]:
    """
    """
    results = {}
    queue = set()
    for sentence in sentences:
        if f"{sentence}.pkl" in os.listdir("embeddings") and not force_recompute:
            results[sentence] = read_embedding(sentence)
        else:
            queue.add(sentence)
    print(f"From cache: {len(results)}, To compute: {len(queue)}")
    if len(queue) > 0:
        print(f"WARNING: Computing embeddings for sentences of length {len(queue)}. This costs $$.")
        generated_embeddings = client.embeddings.create(
            model=model_used, input=list(queue))
        for sentence, generated_embedding in zip(queue, generated_embeddings.data):
            results[sentence] = (sentence, generated_embedding.embedding)
            if save_to_file:
                with open(f"embeddings/{sentence}.pkl", 'wb') as f:
                    pickle.dump(generated_embedding, f)

    return [results[sentence] for sentence in sentences]


def visualize_embeddings(embeddings, labels, sentence, show_plot=True, save_plot=False):
    """
    Visualize the embeddings of a given sentence using t-SNE.

    Args:
        embeddings (list): A list of embeddings to be visualized.
        labels (list): A list of labels for the embeddings.
        sentence (str): The sentence for which the embeddings are to be visualized.
        show_plot (bool): Whether to show the plot. Default is True.
        save_plot (bool): Whether to save the plot. Default is False.

    """
    embeddings_array = np.array(embeddings)

    tsne = TSNE(n_components=2, random_state=1, n_iter=15000,
                perplexity=min(30, len(embeddings_array)-1), metric="cosine")

    embeddings_2d = tsne.fit_transform(embeddings_array)

    colors = ['lightcoral', 'lightgreen', 'skyblue', 'gold', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'lime', 'teal', 'navy', 'red', 'green', 'blue', 'yellow', 'magenta', 'black', 'darkred', 'darkgreen', 'darkblue', 'darkorange', 'darkviolet', 'darkcyan', 'darkmagenta', 'darkyellow', 'darkgray', 'darkolive', 'darkpink', 'darkbrown', 'darkteal', 'darknavy']
    for i, label in enumerate(set(labels)):
        plt.scatter(embeddings_2d[np.array(labels) == label, 0], embeddings_2d[np.array(labels) == label, 1],
                    label=label, color=colors[i], s=50)

    plt.legend(prop={'size': 10}, loc='best')

    plt.grid(True)

    plt.xlabel('Dimension 1', size=11)
    plt.ylabel('Dimension 2', size=11)
    plt.title(f"t-SNE plot of the embeddings of {sentence}", size=12)

    if save_plot:
        plt.savefig(f"pictures/tsne_plot_{sentence}.png")
    if show_plot:
        plt.show()

    plt.close()


if __name__ == '__main__':
    generate_embedding(
        sentence="The doctor called his friend", save_to_file=True)
