from dataset import *
from embeddings import *

male_sentences = generate_sentences(attributes='male', nouns=['doctor'])
female_sentences = generate_sentences(attributes='female', nouns=['doctor'])
neutral_sentences = generate_sentences(attributes='neutral', nouns=['doctor'])

# for sentence in male_sentences:
#     generate_embedding(sentence, save_to_file=True)

# for sentence in female_sentences:
#     generate_embedding(sentence, save_to_file=True)

# for sentence in neutral_sentences:
#     generate_embedding(sentence, save_to_file=True)


print(male_sentences)