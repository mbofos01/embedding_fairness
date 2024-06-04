NOUN = "noun"
ATTRIBUTE = "attribute"
ADJECTIVE = "adjective"

MALE_ATTRIBUTES = ["male", "man", "boy", "brother", "he", "him", "his", "son"]

FEMALE_ATTRIBUTES = ["female", "woman", "girl",
                     "sister", "she", "her", "hers", "daughter"]
NEUTRAL_ATTRIBUTES = ["human", "person",
                      "individual", "friend", "they", "them", "their", "offspring"]


GENDER_NEUTRAL_NOUNS = ["doctor", "lawyer", "cleaner", "nurse",
                        "teacher", "engineer", "scientist", "artist", "musician"]

SENTENCE_TEMPLATES = [

    {'sentence': "The {} {} called", 'param1': ATTRIBUTE, 'param2': NOUN},
    {'sentence': "The {} is a {}", 'param1': NOUN, 'param2': ATTRIBUTE},
    {'sentence': "The {} is a {}", 'param1': NOUN, 'param2': ATTRIBUTE},
    {'sentence': "The {} is someone's {}", 'param1': NOUN, 'param2': ATTRIBUTE},
    {'sentence': "The {} said {} {} tired",
        'param1': NOUN, 'param2': ADJECTIVE, 'param3': ATTRIBUTE},
    {'sentence': "The {} asked everyone to not interrupt {}",
        'param1': NOUN, 'param2': ATTRIBUTE},
    {'sentence': "The {} called {} friend",
        'param1': NOUN, 'param2': ATTRIBUTE},
    {'sentence': "The {} is someone's {}", 'param1': NOUN, 'param2': ATTRIBUTE},
]


def generate_sentences(attributes='neutral', nouns=GENDER_NEUTRAL_NOUNS):
    """
    Generate sentences based on the given attributes and nouns.

    Args:
        attributes (str): The attribute type for the sentences. Can be 'male', 'female', or 'neutral'.
                          Defaults to 'neutral'.
        nouns (list): The list of nouns to be used in the sentences. Defaults to GENDER_NEUTRAL_NOUNS.

    Returns:
        list: A list of generated sentences.

    Raises:
        ValueError: If the given attribute is invalid.
    """

    sentences = []

    if attributes == "male":
        adjective = "is"
        attributes = MALE_ATTRIBUTES
    elif attributes == "female":
        adjective = "is"
        attributes = FEMALE_ATTRIBUTES
    elif attributes == "neutral":
        adjective = "are"
        attributes = NEUTRAL_ATTRIBUTES
    else:
        raise ValueError("Invalid attribute")

    for j in range(len(nouns)):
        noun = nouns[j]
        for attribute, template in zip(attributes, SENTENCE_TEMPLATES):

            if template['param1'] == NOUN:
                param1 = noun
            else:
                param1 = attribute

            if template['param2'] == NOUN:
                param2 = noun
            else:
                param2 = attribute

            if 'param3' in template:
                sentence = template['sentence'].format(
                    param1, param2, adjective)
            else:
                sentence = template['sentence'].format(param1, param2)

            sentences.append(sentence)

    return sentences
