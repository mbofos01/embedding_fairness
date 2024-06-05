NOUN = "noun"
ATTRIBUTE = "attribute"
ADJECTIVE = "adjective"
IS = "is"
ARE = "are"

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
        'param1': NOUN, 'param2': ATTRIBUTE, 'param3': ADJECTIVE},
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
        adjective = IS
        attributes = MALE_ATTRIBUTES
    elif attributes == "female":
        adjective = IS
        attributes = FEMALE_ATTRIBUTES
    elif attributes == "neutral":
        adjective = ARE
        attributes = NEUTRAL_ATTRIBUTES
    else:
        raise ValueError("Invalid attribute")

    for j in range(len(nouns)):
        noun = nouns[j]
        for attribute, template in zip(attributes, SENTENCE_TEMPLATES):

            if template['param1'] == NOUN:
                param1 = noun
            elif template['param1'] == ATTRIBUTE:
                param1 = attribute
            elif template['param1'] == ADJECTIVE:
                param1 = adjective

            if template['param2'] == NOUN:
                param2 = noun
            elif template['param2'] == ATTRIBUTE:
                param2 = attribute
            elif template['param2'] == ADJECTIVE:
                param2 = adjective

            if 'param3' in template:
                if template['param3'] == NOUN:
                    param3 = noun
                elif template['param3'] == ATTRIBUTE:
                    param3 = attribute
                elif template['param3'] == ADJECTIVE:
                    param3 = adjective

            if 'param3' in template:
                sentence = template['sentence'].format(
                    param1, param2, param3)
            else:
                sentence = template['sentence'].format(param1, param2)

            sentences.append(sentence)

    return sentences


def generate_tuples_for_comparison(nouns=GENDER_NEUTRAL_NOUNS):
    """
    Generate tuples of sentences for comparison.

    Args:
        nouns (list): The list of nouns to be used in the sentences

    Returns:
        list: A list of tuples of sentences for comparison

    """
    tuples = []

    for noun in nouns:
        for male_attr, female_attr, neutral_attr, template in zip(MALE_ATTRIBUTES, FEMALE_ATTRIBUTES, NEUTRAL_ATTRIBUTES, SENTENCE_TEMPLATES):
            temp = []
            for attribute in [male_attr, female_attr, neutral_attr]:
                if attribute is not neutral_attr:
                    adjective = IS
                else:
                    adjective = ARE

                if template['param1'] == NOUN:
                    param1 = noun
                elif template['param1'] == ATTRIBUTE:
                    param1 = attribute
                elif template['param1'] == ADJECTIVE:
                    param1 = adjective

                if template['param2'] == NOUN:
                    param2 = noun
                elif template['param2'] == ATTRIBUTE:
                    param2 = attribute
                elif template['param2'] == ADJECTIVE:
                    param2 = adjective

                if 'param3' in template:
                    if template['param3'] == NOUN:
                        param3 = noun
                    elif template['param3'] == ATTRIBUTE:
                        param3 = attribute
                    elif template['param3'] == ADJECTIVE:
                        param3 = adjective


                if 'param3' in template:
                    sentence = template['sentence'].format(
                        param1, param2, param3)
                else:
                    sentence = template['sentence'].format(param1, param2)

                temp.append(sentence)

            tuples.append(tuple(temp))

    return tuples
