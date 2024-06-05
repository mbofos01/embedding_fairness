'''
Helper variables to identify the parts of the sentence
'''
NOUN = "noun"
ATTRIBUTE = "attribute"
ADJECTIVE = "adjective"
IS = "is"
ARE = "are"

'''
The following three lists must be parallel to each other
i.e. the attribute at index i in each list must refer to the same attribute
for example as we can see below, the attribute at index 0
male ~ female ~ human
when adding an attribute to one list, make sure to add it to the other two lists as well
'''
MALE_ATTRIBUTES = ["male", "man", "boy", "brother", "he", "him", "his", "son"]

FEMALE_ATTRIBUTES = ["female", "woman", "girl",
                     "sister", "she", "her", "hers", "daughter"]

NEUTRAL_ATTRIBUTES = ["human", "person",
                      "individual", "sibling", "they", "them", "their", "offspring"]

'''
These nous were taken from the caliskan et al. paper
'''
GENDER_NEUTRAL_NOUNS = ["doctor", "lawyer", "cleaner", "nurse",
                        "teacher", "engineer", "scientist", "artist", "musician"]

'''
The following sentence templates are influenced by the caliskan et al. paper
sentence: template for the sentence
param1: the first parameter in the sentence
param2: the second parameter in the sentence
param3: the third parameter in the sentence
attribute_index_used: the index of the attribute to be used in the sentence
'''
SENTENCE_TEMPLATES = [

    {'sentence': "The {} {} called", 'param1': ATTRIBUTE,
        'param2': NOUN, 'attribute_index_used': 0},
    {'sentence': "The {} is a {}", 'param1': NOUN,
        'param2': ATTRIBUTE, 'attribute_index_used': 1},
    {'sentence': "The {} is a {}", 'param1': NOUN,
        'param2': ATTRIBUTE, 'attribute_index_used': 2},
    {'sentence': "The {} is someone's {}", 'param1': NOUN,
        'param2': ATTRIBUTE, 'attribute_index_used': 3},
    {'sentence': "The {} said {} {} tired",
        'param1': NOUN, 'param2': ATTRIBUTE, 'param3': ADJECTIVE, 'attribute_index_used': 4},
    {'sentence': "The {} asked everyone to not interrupt {}",
        'param1': NOUN, 'param2': ATTRIBUTE, 'attribute_index_used': 5},
    {'sentence': "The {} called {} friend",
        'param1': NOUN, 'param2': ATTRIBUTE, 'attribute_index_used': 6},
    {'sentence': "The {} is someone's {}", 'param1': NOUN,
        'param2': ATTRIBUTE, 'attribute_index_used': 7},
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
        for template in SENTENCE_TEMPLATES:
            attribute = attributes[template['attribute_index_used']]

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
        for template in SENTENCE_TEMPLATES:
            male_attr = MALE_ATTRIBUTES[template['attribute_index_used']]
            female_attr = FEMALE_ATTRIBUTES[template['attribute_index_used']]
            neutral_attr = NEUTRAL_ATTRIBUTES[template['attribute_index_used']]
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
