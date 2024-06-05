from dataset import *
from embeddings import *

male_sentences = generate_sentences(attributes='male')
female_sentences = generate_sentences(attributes='female')
neutral_sentences = generate_sentences(attributes='neutral')

for sentence in male_sentences:
    generate_embedding(sentence=sentence, save_to_file=True)

for sentence in female_sentences:
    generate_embedding(sentence=sentence, save_to_file=True)

for sentence in neutral_sentences:
    generate_embedding(sentence=sentence, save_to_file=True)


tuples = generate_tuples_for_comparison()

for triplet in tuples:
    ml, fl, nl = triplet
    _, ml_embedding = generate_embedding(sentence=ml)
    _, fl_embedding = generate_embedding(sentence=fl)
    _, nl_embedding = generate_embedding(sentence=nl)
    print(f"Male:    {ml}, Embedding: {len(ml_embedding)}")
    print(f"Female:  {fl}, Embedding: {len(fl_embedding)}")
    print(f"Neutral: {nl}, Embedding: {len(nl_embedding)}")
    print(f"{'---' * 20}\n")
