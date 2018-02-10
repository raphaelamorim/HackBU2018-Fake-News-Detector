from textstat.textstat import textstat
import language_check
import nltk


def count_partsofspeech(article_contents: str) -> dict:
    """
    Returns the number of adjectives in a given string.

    @param article_contents, a string containing a news article
    @return pos_dict, which contains the parts of speech breakdown of an article
    """
    pos_dict = {}
    text = nltk.word_tokenize(article_contents)

    for word in nltk.pos_tag(text):
        if word[1] in pos_dict:
            pos_dict[word[1]] += 1

        else:
            pos_dict[word[1]] = 1

    return pos_dict


def get_text_characteristics(article_contents: str) -> dict:
    """
    Takes an article's contents and analyzes its complexity using numerous reading scores and methods. Also calculates
    other factors such as the number of typos.

    @param article_contents, a string which contains the contents of an article
    @return language_analysis_dict, a dictionary which contains
    """
    tool = language_check.LanguageTool('en-US')
    language_analysis_dict = {
        "flesch_reading": textstat.flesch_reading_ease(article_contents),
        "smog": textstat.smog_index(article_contents),
        "flesch_kincaid": textstat.flesch_kincaid_grade(article_contents),
        "coleman_liau": textstat.coleman_liau_index(article_contents),
        "ari": textstat.automated_readability_index(article_contents),
        "dale_chall": textstat.dale_chall_readability_score(article_contents),
        "difficult_words": textstat.difficult_words(article_contents),
        "linsear_write": textstat.linsear_write_formula(article_contents),
        "gunning_fog": textstat.gunning_fog(article_contents),
        "text_standard": textstat.text_standard(article_contents),
        "lexicon_count": textstat.lexicon_count(article_contents),
        "language_check_typos": len(tool.check(article_contents)),
        "typos_to_words": len(tool.check(article_contents)) / textstat.lexicon_count(article_contents),
    }

    return language_analysis_dict
