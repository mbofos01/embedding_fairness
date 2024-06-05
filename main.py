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