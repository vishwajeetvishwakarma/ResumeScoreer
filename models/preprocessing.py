import spacy
import pandas as pd
import numpy as np
from spacy.pipeline import EntityRuler
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
import jsonlines
import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz

nltk.download(['stopwords', 'wordnet' , "omw-1.4"])

# importing Modules
from variables import Variables

word_lemetizer = spacy.load('en_core_web_lg', disable=['parser', 'ner'])
nlp = spacy.load("en_core_web_lg")
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(Variables.SKILL_PATH)

stopwords = stopwords.words("english")


def get_skills(text):
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            subset.append(ent.text)
    myset.append(subset)
    return subset


def unique_skills(x):
    return list(set(x))


def clean_and_lemetize_words(text):
    """
    This Function takes a text string and performs lemmatization on it and remove stop words
    :param text:
    :return: text
    """
    text = re.sub(
        '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',
        " ",
        text,
    )
    text = text.lower()
    doc = word_lemetizer(text)
    text = " ".join([token.lemma_ for token in doc])
    return text


# def get_synonyms(word):
#     synonyms = set()
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())
#     return synonyms


def fuzzy_match(skill1, skill2, threshold=80):
    return fuzz.token_set_ratio(skill1, skill2) >= threshold

def matched_skills(resume_text, company_desc):
    """
    This Function will take resume text and company requirement text and from that it will return how many sills of that persone is matching with skills that are need to comapny
    :param resume_text:
    :param company_desc:
    :return: Total Person Skill, Total Company Requirement Skill, Total Matched Skills , All Person Skills, All Company Requirement
    """
    person_skills = get_skills(resume_text)
    company_skills = get_skills(company_desc)

    person_skills = unique_skills(person_skills)
    company_skills = unique_skills(company_skills)

    total_matched = 0
    for person_skill in person_skills:
        for company_skill in company_skills:
            if fuzzy_match(person_skill, company_skill):
                total_matched += 1
                break # Skip to the next person_skill if a match is found

    return len(person_skills), len(company_skills), total_matched, person_skills, company_skills


# def matched_skills(resume_text, company_desc):
#     """
#     This Function will take  resume text and company requirement text and from that it will return how many sills of that persone is matching with skills that are need to comapny
#     :param resume_text:
#     :param company_desc:
#     :return: Total Person Skill, Total Company Requirement Skill, Total Matched Skills , All Person Skills, All Company Requirement
#     """
#     person_skills = get_skills(resume_text)
#     company_skills = get_skills(company_desc)
#
#     person_skills = unique_skills(person_skills)
#     company_skills = unique_skills(company_skills)
#
#     expanded_person_skills = set()
#     expanded_company_skills = set()
#
#     for skill in person_skills:
#         expanded_person_skills.update(get_synonyms(skill))
#
#     for skill in company_skills:
#         expanded_company_skills.update(get_synonyms(skill))
#
#     total_matched = 0
#     for i in expanded_person_skills:
#         if i in expanded_company_skills:
#             total_matched += 1
#     return len(person_skills), len(company_skills), total_matched, person_skills, company_skills, len(expanded_person_skills), len(expanded_company_skills)