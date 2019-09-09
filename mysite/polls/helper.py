import yaml


def load_yaml_blacklist():
    '''
    loads list into a set and returns
    '''
    with open('polls/blacklist.yaml', 'r') as f:
        try:
            blacklist = set(yaml.safe_load(f)['blacklisted-words'])
        except yaml.YAMLError as e:
            print(e)

    return blacklist


def language_check(sentence):
    '''
    language_check gets passed a sentence. the function will
    strip casing, remove common punctuation, and checks the word
    with the blacklisted words in the yaml file
    returns: (True, coarse_word) OR (False, None)
    '''
    blacklist = load_yaml_blacklist()
    punctuation = '?!.\'"'
    for word in sentence.split():
        for punct in punctuation:
            word = word.replace(punct, '')
        if word.lower() in blacklist:
            return True, word.lower()
    return False, None