import pandas as pd
import numpy as np

import functools  # for partial parametres

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn

import re, math
from collections import Counter

WORD = re.compile(r'\w+')


# СХО ЖЕСТЬ ПРЕДЛОЖЕНИЙ С ИСПОЛЬЗОВАНИЕМ WORDNET --------------------------------

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


# -------------------------------------------------------------------------------
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(sentence1)  # pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(sentence2)  # pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # ----

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        curr_arr = [x for x in [synset.path_similarity(ss) for ss in synsets2] if x is not None]
        curr_arr.append(0)
        #         print(curr_arr)

        best_score = max(curr_arr)

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    score /= count
    return score


# ТЕХНИЧЕСКИЕ ТЕГИ -------------------------------------------------------------

technical_tags = pd.read_csv('../DB/most_popular_stack_overflow.csv')
technical_tags = set(technical_tags['TagName'])
technical_tags = {x for x in technical_tags if x == x}

technical_tags_dict = {}
technical_tags_ind_dict = {}

index = 0
for x in technical_tags:
    technical_tags_dict[x] = index
    technical_tags_ind_dict[index] = x
    index += 1

# СИНОНИМИЧНЫЙ РЯД ЗАМЕН ДЛЯ ТЕГОВ ТЕХНОЛОГИЙ ----------------------------------

technical_tags_syn = pd.read_csv('../DB/synonyms_for_stackoverflow.csv')
technical_tags_syn.head()

technical_tags_syn_dict = dict(zip(technical_tags_syn.SOurceTagName, technical_tags_syn.TargetTagName))
# technical_tags_syn.set_index('SOurceTagName')['TargetTagName'].to_dict('index')
technical_tags_syn_dict


def technical_tags_syn_try_replace(x):
    if x in technical_tags_syn_dict.keys():
        return technical_tags_syn_dict[x]
    else:
        return x


# Подобие семантической сети тегов технологий ----------------------------------

small_stackoverflow = pd.read_csv('../DB/Small_stackoverflow.csv')
small_stackoverflow = small_stackoverflow['Tags']
small_stackoverflow.head()

semantic_technologies = pd.DataFrame(index=technical_tags, columns=technical_tags)
semantic_technologies = semantic_technologies.fillna(0)
semantic_technologies.head()

for line in small_stackoverflow:
    currlist = line[1:-1].split('><')
    for x in currlist:
        for y in currlist:
            if ((x in technical_tags) and (y in technical_tags)):
                semantic_technologies.set_value(x, y, semantic_technologies.at[x, y] + 1)

semantic_tech_axis_sum0 = semantic_technologies.sum(axis=0)
semantic_tech_axis_sum1 = semantic_technologies.sum(axis=1)
# semantic_technologies.tail()
semantic_tech_axis_sum1.head()

for index, row in semantic_technologies.iterrows():
    #     print(type(index))
    semantic_technologies.loc[index] = semantic_technologies.loc[index] / \
                                       (np.minimum(semantic_tech_axis_sum1[index], semantic_tech_axis_sum0))
    semantic_technologies.loc[index, index] = -1.0
semantic_technologies.fillna(0, inplace=True)


# ------------------------------------------------------------------------------
# ОБЩАЯ СТРУКТУРА --------------------------------------------------------------

def geo_distance_metrics(geo1, geo2):
    return abs(geo1 - geo2)


def geo_close_enough(geo1, geo2):
    return True #geo_distance_metrics(geo1, geo2) < 3000


def closest_people(data, index):
    person = data.iloc[index]

    # print("Out req person:", person)

    stud_lambd1 = lambda x: \
        (geo_close_enough(person.geo, x.geo) or False) and \
        x.user_role == 'mentor'

    ment_lambd1 = lambda x: \
        (geo_close_enough(person.geo, x.geo) or False) and \
        x.user_role == 'student'

    if person.user_role == 'student':
        closest_people = data[data.apply(stud_lambd1, axis=1)]
        return closest_people
    elif person.user_role == 'mentor':
        closest_people = data[data.apply(ment_lambd1, axis=1)]
        return closest_people


# soft cosine dist -------------------------------------------------------------

def tech_tag_sim(w1, w2):
    if (w1 == w2):
        return 1.0
    elif (w1 in technical_tags and w2 in technical_tags):
        return semantic_technologies.loc[w1, w2]
    else:
        return 0.0


def get_cosine_soft(vec1, vec2):
    # print('vec', vec1, vec2)

    S1 = 0
    S2 = 0
    S3 = 0
    for x in vec1:
        for y in vec2:
            S1 += tech_tag_sim(x, y)
    for x in vec1:
        for y in vec1:
            S2 += tech_tag_sim(x, y)
    for x in vec2:
        for y in vec2:
            S3 += tech_tag_sim(x, y)

    S2 = S2 ** 0.5
    S3 = S3 ** 0.5

    if (S2 * S3 > 0):
        return S1 / (S2 * S3)
    else:
        return 0.0


# проверка человека ------------------------------------------------------------

def check_person(person, x):
    w0 = 0
    w1 = 1
    xskills = [technical_tags_syn_try_replace(i) for i in x.skills_tags.split(',')]  # x.skills_tags.replace(",", " ")
    xintro = x.intro_phrase_tags.split(',')  # x.intro_phrase_tags.replace(",", " ")#

    personskills = [technical_tags_syn_try_replace(i) for i in
                    person.skills_tags.split(',')]  # person.skills_tags.replace(",", " ")
    personintro = person.intro_phrase_tags.split(',')  # person.intro_phrase_tags.replace(",", " ")#

    x_alltags = xskills + xintro
    person_alltags = personskills + personintro

    xtechnical = [x for x in x_alltags if x in technical_tags]
    persontechnical = [x for x in person_alltags if x in technical_tags]
    xhuman = [x for x in x_alltags if not (x in technical_tags)]
    personhuman = [x for x in person_alltags if (not x in technical_tags)]

    return w0 * sentence_similarity(xhuman, personhuman) + \
           w1 * get_cosine_soft(list_to_vector(xtechnical), list_to_vector(persontechnical))


def process_req(data, index):
    print("TAIAIIAIIAA", type(index), '=', index)
    print("DATA = ", data)
    person = data.iloc[int(index)]

    closest1 = closest_people(data, index)

    print('CLOSESTCLOSEST', closest1)

    sLength = len(closest1['id'])
    if (not closest1.empty):
        closest1['tag_score'] = closest1.apply(functools.partial(check_person, person), axis=1)
    else:
        return None
    return closest1.sort_values(by=['tag_score'], ascending=False)

def process_by_id(data, id):
    print(data['id'])
    print(id == data['id'])

    index = np.argwhere(id == data['id']).ravel()[0]
    return process_req(data, index)