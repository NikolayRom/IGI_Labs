"""
Purpose: Task 4 - String analysis without regular expressions
Lab number: 3
Lab title: Standard data types, collections, functions, modules
Version: 1.0
Developer: Romanov Nikolai Viktorovich
Date: 08.03.2026
"""

def get_cleaned_words(text):
    """
    Splits text into words and removes punctuation marks (, .)
    from the edges of each word without using regex.
    """
    raw_words = text.split()
    cleaned_words =[]
    
    for word in raw_words:
        # Strip punctuation from edges only, preserving internal hyphens
        clean_word = word.strip('.,')
        if clean_word:
            cleaned_words.append(clean_word)
            
    return cleaned_words

def get_even_length_words(words):
    """
    Returns a list of words that have an even number of characters.
    """
    return[word for word in words if len(word) % 2 == 0]

def find_shortest_word(words, start_char='a'):
    """
    Finds the shortest word starting with a specific character (case-insensitive).
    """
    matching_words =[word for word in words if word.lower().startswith(start_char.lower())]
    
    if not matching_words:
        return None
        
    return min(matching_words, key=len)

def get_repeating_words(words):
    """
    Returns a list of words that appear more than once in the text (case-insensitive).
    """
    # Using sets for O(n) average time complexity when finding duplicates
    lower_words =[word.lower() for word in words]
    repeats = set()
    seen = set()
    
    for word in lower_words:
        if word in seen:
            repeats.add(word)
        else:
            seen.add(word)
            
    return list(repeats)

def print_task4_results(total_words, even_words, shortest_a_word, repeat_words):
    """
    Prints the results of Task 4 in a formatted and user-friendly way.
    """
    print("\n" + "=" * 60)
    print(f"{'TASK 4 RESULTS':^60}")
    print("=" * 60)
    
    print(f"a) Total words in text: {total_words}")
    print(f"   Words with even length ({len(even_words)}):")
    print(f"   {', '.join(even_words)}\n")
    
    print(f"b) Shortest word starting with 'a':")
    if shortest_a_word:
        print(f"   -> '{shortest_a_word}'\n")
    else:
        print("   -> No such words found.\n")
        
    print(f"c) Repeating words ({len(repeat_words)}):")
    print(f"   {', '.join(repeat_words)}")
    print("=" * 60 + "\n")

def task4():
    """
    Main business function for Task 4.
    Initializes the hardcoded string and orchestrates the sub-tasks.
    """
    print("\n--- Task 4: Text Analysis ---")
    
    text = (
        "So she was considering in her own mind, as well as she could, "
        "for the hot day made her feel very sleepy and stupid, whether "
        "the pleasure of making a daisy-chain would be worth the trouble "
        "of getting up and picking the daisies, when suddenly a White Rabbit "
        "with pink eyes ran close by her."
    )
    
    print(f"Analyzing text:\n\"{text}\"\n")
    
    words = get_cleaned_words(text)
    
    total_count = len(words)
    even_words = get_even_length_words(words)
    
    shortest_a = find_shortest_word(words, 'a')
    
    repeating = get_repeating_words(words)
    
    print_task4_results(total_count, even_words, shortest_a, repeating)