def countingEvenWords(list_str):
    even_words = []
    for s in list_str:
        if len(s) % 2 == 0:
            even_words.append(s)
    return even_words