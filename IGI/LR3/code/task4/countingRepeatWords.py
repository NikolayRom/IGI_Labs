def countingRepeatWords(list_str):
    repeat_words = []

    lower_words = list(map(lambda c: c.lower(), list_str))

    for s in lower_words:
        if lower_words.count(s) != 1:
            if repeat_words.count(s) != 0:
                continue
            repeat_words.append(s)

    return repeat_words