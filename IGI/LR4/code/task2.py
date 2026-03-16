from zipfile import ZipFile
import re
from validation import Validation

filename = "task2.txt"
filename_result = "task2_result.txt"
zipname = "task2.zip"
data = ""
data_replace = ""
is_guid = False
count_3_len = 0
words_with_equal_vowels_consonants = []
sorted_words = []
count_sentence = 0

def read_file(filename):
    with open(filename, encoding="utf-8") as fh:
        return fh.read()

data = read_file(filename)


def replace_space(text):
    char_replace = Validation.inputStr("Enter symbol to replace space: ")
    return re.sub(r"\s", char_replace, text)

data_replace = replace_space(data)
print(data_replace)

# for match in re.findall(r'([^.!?…]+)[.!?…]+(?:\s|$)', data):
#     is_guid.append(re.findall(r'[\(\{\[]?[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}[\)\}\]]?', match, re.IGNORECASE))

def check_guid(text):
    if(re.match(r'\s*[\(\{\[]?[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}[\)\}\]]?\s*[.!?…]+(?:\s|$)', text, re.IGNORECASE)):
        return True
    return False


is_guid = check_guid(data)
print(is_guid)

def get_count_3_len(text):
    return len(re.findall(r"\b(\w{3})\b", text))

count_3_len = get_count_3_len(data)
print(count_3_len)

def find_words_with_equal_vowels_consonants(text):
    vowels = r'аеёиоуыэюяaeiouy'
    consonants = r'бвгджзйклмнпрстфхцчшщbcdfghjklmnpqrstvwxz'
    
    words = re.findall(r'\b[а-яa-z]+\b', text, re.IGNORECASE)
    
    result = []
    for idx, word in enumerate(words, 1):
        word_lower = word.lower()
        
        vowel_count = len(re.findall(f'[{vowels}]', word_lower))
        consonant_count = len(re.findall(f'[{consonants}]', word_lower))
        
        if vowel_count == consonant_count and (vowel_count + consonant_count) > 0:
            result.append((idx, word))
    
    return result

words_with_equal_vowels_consonants = find_words_with_equal_vowels_consonants(data)
print(words_with_equal_vowels_consonants)

def sort_words(text):
    return sorted(re.findall(r"\b\w+\b", text, re.IGNORECASE), key=len, reverse=True)

sorted_words = sort_words(data)
print(sorted_words)

def get_count_sentence(text):
    return len(re.findall(r'([^.!?…]+)[.!?…]+(?:\s|$)', text))

count_sentence = get_count_sentence(data)
print(count_sentence)



# result = "Test Result: " + data

# with open(filename_result, "w", encoding="utf-8") as fh:
#     print(result, file=fh)

# with ZipFile(zipname, "w") as zip:
#     zip.write(filename_result)

# with ZipFile(zipname, "r") as zip:
#     print(zip.getinfo(filename_result))

