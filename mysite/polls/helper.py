import yaml

BLACKLISTED_WORDS = 'polls/blacklist.yaml'
FORTUNE = 'polls/import_data.yaml'


def load_yaml_blacklist():
    '''
    loads list into a set and returns
    '''
    with open(BLACKLISTED_WORDS, 'r') as f:
        try:
            blacklist = set(yaml.safe_load(f)['blacklisted-words'])
        except yaml.YAMLError as e:
            print(e)

    return blacklist


def load_yaml_fortune():
    '''
    loads fortune 100 list into a set and returns
    '''
    with open(FORTUNE, 'r') as f:
        try:
            fortune_list = yaml.safe_load(f)['fortune-100-companies']
        except yaml.YAMLError as e:
            print(e)

    return fortune_list


def language_check(sentence):
    '''
    language_check gets passed a sentence. the function will
    strip casing, remove common punctuation, and checks the word
    with the blacklisted words in the yaml file
    returns: (True, coarse_word) OR (False, None)
    '''
    blacklist = load_yaml_blacklist()
    sentence = sentence.translate({ord(i): None for i in '?!.\'"'})\
        .lower().split()
    for word in sentence:
        if word in blacklist:
            return True, word
    return False, None
