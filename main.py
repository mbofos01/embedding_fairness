from dataset import *
from embeddings import *

tuples = generate_tuples_for_comparison()
labels = []
embeddings = []

for triplet in tuples:
    ml, fl, nl = triplet
    _, ml_embedding = generate_embedding(sentence=ml, save_to_file=True)
    _, fl_embedding = generate_embedding(sentence=fl, save_to_file=True)
    _, nl_embedding = generate_embedding(sentence=nl, save_to_file=True)
    print(f"Male:    {ml}, Embedding: {len(ml_embedding)}")
    print(f"Female:  {fl}, Embedding: {len(fl_embedding)}")
    print(f"Neutral: {nl}, Embedding: {len(nl_embedding)}")
    print(f"{'---' * 30}\n")

    embeddings.extend([ml_embedding, fl_embedding, nl_embedding])
    labels.extend(['Male', 'Female', 'Neutral'])

    visualize_embeddings(embeddings=[ml_embedding, fl_embedding, nl_embedding], labels=['Male', 'Female', 'Neutral'],
                         sentence=f"{nl}", show_plot=False, save_plot=True)


visualize_embeddings(embeddings=embeddings, labels=labels,
                     sentence=f"All Sentences", show_plot=True, save_plot=True)
