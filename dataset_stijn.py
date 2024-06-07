from collections import defaultdict
import itertools
import random
import pandas as pd
import numpy as np
from embeddings import generate_embedding, generate_embedding_bulk, visualize_embeddings

# Set random seed
random.seed(42)


### Use baby names dataset for choosing female, male and neutral names that are used in sentences

def load_names_from_baby_names():
    
    # CSV file with columns "year","name","percent","sex", get the top 1000 names for "boy" and "girl"
    f = "baby-names.csv"
    
    # Load all data from the file
    data = pd.read_csv(f)
    # Sum each row for name and sex
    data = data.groupby( ["name", "sex"] ).sum().reset_index()
    # Sort by percent
    data = data.sort_values(by='percent', ascending=False)

    males = data[data["sex"] == "boy"]
    females = data[data["sex"] == "girl"]


    intersect = pd.merge(males, females, on=["name"], how="inner")
    # Filter intersect where 1.3 > percent_x/percent_y > 0.7
    intersect = intersect[(intersect["percent_x"]/intersect["percent_y"] > 0.80) & (intersect["percent_x"]/intersect["percent_y"] < 1.2)]

    # Assert that the sum of intersects percentages are 95% similar
    assert abs(intersect["percent_x"].sum() - intersect["percent_y"].sum()) / len(intersect) < 0.05
    males_subset = males[:20]
    females_subset = females[:20]
    intersect_subset = intersect[:min(20,len(intersect))]

    # Return array of top 1000 names
    man_array = males_subset["name"].values
    female_array = females_subset["name"].values
    nonbinary_array = intersect_subset["name"].values
    return (man_array,female_array, nonbinary_array)


### Load occupations from occupations.csv, this is some list of occupations I found online. I simplify to single word occupations.

def load_occupations():
    f = "inc_occ_gender.csv"
    # Has format Occupation,All_workers,All_weekly,M_workers,M_weekly,F_workers,F_weekly
    data = pd.read_csv(f)
    # Remove data where Occupation is all caps
    data = data[~data["Occupation"].str.isupper()]
    # Sort by All_workers and get top 100
    data = data.sort_values(by='All_workers', ascending=False)
    data = data[:100]

    # Add a collumn that has M_workers/F_workers
    data["ratio"] = data["M_workers"] / data["F_workers"]
    # Sort by ratio
    data = data.sort_values(by='ratio', ascending=False)

    # Get top occupations for both genders
    top_m = data[:10]["Occupation"].values
    top_f = data[-10:]["Occupation"].values

    return (top_m,top_f)
    


(MALE_NAMES,FEMALE_NAMES,NEUTRAL_NAMES) = load_names_from_baby_names()

(MALE_OCUPATIONS,FEMALE_OCCUPATIONS) = load_occupations()
print(MALE_OCUPATIONS,FEMALE_OCCUPATIONS)
SENTENCE_TEMPLATES = [
    "{name} is a {attribute}",
    # "{name} is someone's {attribute}",
    "{name} works as a {attribute}",
    "{name} retired from being a {attribute}",
]

def generate_sentences(names, attributes = pd.concat([pd.Series(MALE_OCUPATIONS),pd.Series(FEMALE_OCCUPATIONS)])):
    sentences = {}
    # Create all possible combinations of attribute, noun and sentence template
    triplets = list(itertools.product(attributes, names, SENTENCE_TEMPLATES))

    for (a, n, st) in triplets:
        sentence = st.format(name=n, attribute=a)
        sentences[(a,n,st)] = sentence

    return sentences


### Generate sentences and create a dataframe that has all sentences

neutral_sentence_dict = generate_sentences(names=NEUTRAL_NAMES)
male_sentence_dict = generate_sentences(names=MALE_NAMES)
female_sentence_dict = generate_sentences(names=FEMALE_NAMES)

pd_neutral = pd.DataFrame([(k[0],k[1],k[2],v,"X") for k,v in neutral_sentence_dict.items()], columns=["attribute","name","sentence_template","sentence", "group"])
pd_f = pd.DataFrame([(k[0],k[1],k[2],v,"F") for k, v in female_sentence_dict.items()], columns=["attribute","name","sentence_template","sentence", "group"])
pd_m = pd.DataFrame([(k[0],k[1],k[2],v,"M") for k, v in male_sentence_dict.items()], columns=["attribute","name","sentence_template","sentence", "group"])

pd_all = pd.concat([pd_neutral,pd_f,pd_m])

# Add index to pd_all
pd_all = pd_all.reset_index()

# Write pd_all to csv
pd_all.to_csv("dataset_pd_all.csv")

# Print total sentence tokens
total_sentence_tokens = pd_all["sentence"].apply(lambda x: len(x.split(" "))).sum()
print(f"Total sentence tokens(make sure this is not too much for OpenAI): {total_sentence_tokens}")

# Have user confirm that he wants to continue 
input("Press Enter to continue...")

### Acquire embeddings for all sentences, code can use some cleaning up

# Create dictionary copy of pd_all
pd_all_to_dict = pd_all.to_dict(orient="index")

distinct_attributes = pd_all["attribute"].unique()
distinct_groups = pd_all["group"].unique()

for a in distinct_attributes:
    for g in distinct_groups:
        print(f"Attribute: {a}, Group: {g}")
        data_a_g = pd_all[(pd_all["attribute"] == a) & (pd_all["group"] == g)]
        
        embedding_str_pairs = generate_embedding_bulk(sentences=data_a_g["sentence"].values,save_to_file=True)
        assert len(embedding_str_pairs) == len(data_a_g)
        for ((i, row),(sentence, embedding)) in zip(data_a_g.iterrows(),embedding_str_pairs):
            assert row["sentence"] == sentence              

            # Store array in pd_all_to_dict
            pd_all_to_dict[i]["embedding"] = np.array(embedding)

### Statistics on embeddings

def get_cosine_similarity(a,avg_a_g):
    cos_x_f = np.dot(avg_a_g[("X",a)],avg_a_g[("F",a)]) / (np.linalg.norm(avg_a_g[("X",a)]) * np.linalg.norm(avg_a_g[("F",a)]))
    cos_x_m = np.dot(avg_a_g[("X",a)],avg_a_g[("M",a)]) / (np.linalg.norm(avg_a_g[("X",a)]) * np.linalg.norm(avg_a_g[("M",a)]))
    print(f"Attribute: {a}, Cosine similarity between X and F: {cos_x_f}, Cosine similarity between X and M: {cos_x_m}")

    return (cos_x_f,cos_x_m)

average_embedding_a_g = defaultdict(list)
for (i,row) in pd_all_to_dict.items():
    embedding = row["embedding"]
    average_embedding_a_g[(row["group"],row["attribute"])].append(embedding)

average_embedding_a_g = {k: np.mean(v,axis=0).squeeze() for k,v in average_embedding_a_g.items()}
print(f"Average embeddings per group: {average_embedding_a_g}")

cosine_similarities = {}
for a in distinct_attributes:
    (cos_x_f,cos_x_m) =get_cosine_similarity(a,average_embedding_a_g)
    cosine_similarities[a] = (cos_x_f,cos_x_m)

# Plot
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))  # Increase the width of the chart

ax.barh(list(cosine_similarities.keys()), [v[0] for v in cosine_similarities.values()], color='b', alpha=0.5, label='X-F')
ax.barh(list(cosine_similarities.keys()), [v[1] for v in cosine_similarities.values()], color='r', alpha=0.5, label='X-M')
ax.legend()

# Adjust the layout to prevent labels from falling off
plt.tight_layout()

plt.savefig("cosine_similarities.png")


def get_mean_cosine_difference(w, A, B):

    cosines_w_A = [np.dot(w,a) / (np.linalg.norm(w) * np.linalg.norm(a)) for a in A]
    cosines_w_B = [np.dot(w,b) / (np.linalg.norm(w) * np.linalg.norm(b)) for b in B]
    mean_cosine_A = np.mean(cosines_w_A)
    mean_cosine_B = np.mean(cosines_w_B)
    return mean_cosine_A - mean_cosine_B


def get_WEAT_score(X,Y,A,B): # This is still not the good metric!
    mean_cosines_for_X = [get_mean_cosine_difference(x,A,B) for x in X]
    mean_cosines_for_Y = [get_mean_cosine_difference(y,A,B) for y in Y]
    return np.mean(mean_cosines_for_X) - np.mean(mean_cosines_for_Y)

GROUP_F = [emb["embedding"] for emb in pd_all_to_dict.values() if emb["group"] == "F"]
GROUP_M = [emb["embedding"] for emb in pd_all_to_dict.values() if emb["group"] == "M"]
GROUP_OCC_F = [emb["embedding"] for emb in pd_all_to_dict.values() if emb["attribute"] in FEMALE_OCCUPATIONS]
GROUP_OCC_M = [emb["embedding"] for emb in pd_all_to_dict.values() if emb["attribute"] in MALE_OCUPATIONS]

print(get_WEAT_score(GROUP_F,GROUP_M,GROUP_OCC_F,GROUP_OCC_M))

    






        



