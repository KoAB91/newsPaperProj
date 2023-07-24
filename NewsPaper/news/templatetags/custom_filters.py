from django import template

register = template.Library()

OBSCENE_WORDS = [
    'кино', 'музыке', 'сайт'
]


@register.filter()
def censor(value):

    if not isinstance(value, str):
        return value

    all_words = value.split(' ')
    censored_words = []
    for word in all_words:
        if word.lower() in OBSCENE_WORDS:
            word = word[0] + '*' * (len(word) - 1)
        censored_words.append(word)

    return ' '.join(censored_words)
