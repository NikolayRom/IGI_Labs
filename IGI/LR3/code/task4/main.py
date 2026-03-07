from countingWords import countingWords
from countingEvenWords import countingEvenWords
from countingRepeatWords import countingRepeatWords

str = "So she was considering in her own mind, " \
        "as well as she could, for the hot day made her feel very sleepy and stupid, " \
        "whether the pleasure of making a daisy-chain would be worth the trouble " \
        "of getting up and picking the daisies, when suddenly a White Rabbit " \
        "with pink eyes ran close by her."

list_str = countingWords(str)
print(len(list_str))

even_words = countingEvenWords(list_str)
print(even_words)
 
print(sorted(list(filter(lambda s: s[0] == 'a', list_str)), key=lambda c: len(c))[0])

repeat_words = countingRepeatWords(list_str)
print(repeat_words)