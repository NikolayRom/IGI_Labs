"""
Brief purpose: Module for Task 2. Text analysis using Regular Expressions, File I/O, and Zip archives.
Lab number and title: Lab 4 - Working with files, classes, serializers, regular expressions, and standard libraries
Version: 1.0
Developer: Romanov Nikolay Viktorovich
Date: 16.03.2026
"""

import os
import re
from zipfile import ZipFile
from validation import Validation

class TaskStorage:
    """Static class for storing file paths and configuration data."""
    filename = "task2.txt"
    filename_result = "task2_result.txt"
    zipname = "task2.zip"
    data = ""

class BaseFileHandler:
    """Base class demonstrating OOP inheritance for file management."""
    
    def __init__(self, filename):
        """Initializes the base file handler using a protected attribute."""
        self._filename = filename

    def get_info(self):
        """Abstract method to demonstrate polymorphism in subclasses."""
        raise NotImplementedError("Method get_info() must be overridden.")


class FileManager(BaseFileHandler):
    """Class for reading and writing text files. Inherits from BaseFileHandler."""
    
    def __init__(self, filename):
        super().__init__(filename) 

    def read_file(self):
        """Reads text from the file."""
        if not os.path.exists(self._filename):
            print(f"Error: File '{self._filename}' not found.")
            return ""
        with open(self._filename, "r", encoding="utf-8") as fh:
            return fh.read()

    def write_results(self, results_dict):
        """Writes analysis results to the file."""
        with open(self._filename, "w", encoding="utf-8") as fh:
            for key, value in results_dict.items():
                fh.write(f"{key}: {value}\n")

    def get_info(self):
        """Polymorphism: Overrides base method to return text file size."""
        size = os.path.getsize(self._filename) if os.path.exists(self._filename) else 0
        return f"[FileManager Info] File '{self._filename}' is {size} bytes."


class ZipManager(BaseFileHandler):
    """Class for creating and managing zip archives. Inherits from BaseFileHandler."""
    
    def __init__(self, zipname):
        super().__init__(zipname) 
    
    def create_zip(self, file_to_zip):
        """Archives the specified file into a ZIP archive."""
        if os.path.exists(file_to_zip):
            with ZipFile(self._filename, "w") as zipf:
                zipf.write(file_to_zip)
                print(f"File '{file_to_zip}' successfully archived to '{self._filename}'.")

    # Detailed info about the first file in archive
    def get_info(self):
        """Polymorphism: Overrides base method to return archive contents."""
        if not os.path.exists(self._filename):
            return f"[ZipManager Info] Archive '{self._filename}' does not exist."
            
        with ZipFile(self._filename, "r") as zipf:
            files_in_zip = zipf.namelist()
            if files_in_zip:
                info = zipf.getinfo(files_in_zip[0])
                return (f"[ZipManager Info] Archive contains: {files_in_zip}. "
                        f"\nFile '{info.filename}' compressed size: {info.compress_size} bytes.")
            return "[ZipManager Info] Archive is empty."


class IndividualTaskService:
    """Service for handling individual variant tasks using regex."""
    
    @staticmethod
    def replace_space(text):
        char_replace = Validation.inputStr("Enter symbol to replace spaces in text: ")
        return re.sub(r"\s", char_replace, text)
        
    @staticmethod
    def check_guid(text):
        """Checks if the text contains a valid GUID."""
        pattern = r'[\(\{\[]?[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}[\)\}\]]?'
        return bool(re.search(pattern, text))
        
    @staticmethod
    def get_count_3_len(text):
        """Returns the number of 3-letter words."""
        return len(re.findall(r"\b[a-zA-Zа-яА-ЯёЁ]{3}\b", text))
        
    @staticmethod
    def find_words_with_equal_vowels_consonants(text):
        """Finds words where the number of vowels equals consonants."""
        vowels = r'аеёиоуыэюяaeiouy'
        consonants = r'бвгджзйклмнпрстфхцчшщbcdfghjklmnpqrstvwxz'
        
        words = re.findall(r'\b[а-яА-Яa-zA-ZёЁ]+\b', text)
        result =[]
        
        for idx, word in enumerate(words, 1):
            word_lower = word.lower()
            vowel_count = len(re.findall(f'[{vowels}]', word_lower))
            consonant_count = len(re.findall(f'[{consonants}]', word_lower))
            
            if vowel_count == consonant_count and vowel_count > 0:
                result.append(f"{idx}: {word}")
        
        return result
        
    @staticmethod
    def sort_words(text):
        """Sorts all words in the text by length in descending order."""
        words = re.findall(r"\b[a-zA-Zа-яА-ЯёЁ]+\b", text)
        return sorted(words, key=len, reverse=True)


class CommonTaskService:
    """Service for handling common analysis tasks using regex."""
    
    @staticmethod
    def get_count_sentence(text):
        """Counts the total number of sentences."""
        return len(re.findall(r'([^.!?…]+)[.!?…]+', text))
        
    @staticmethod
    def get_exclamatory_count(text):
        """Counts exclamatory sentences (!)."""
        return len(re.findall(r'([^.!?…]+)[!]+', text))
        
    @staticmethod
    def get_declarative_count(text):
        """Counts declarative sentences (.)."""
        return len(re.findall(r'([^.!?…]+)[.]+', text))
        
    @staticmethod
    def get_interrogative_count(text):
        """Counts interrogative sentences (?)."""
        return len(re.findall(r'([^.!?…]+)[?]+', text))
        
    @staticmethod
    def get_average_len_sentence(text):
        """Calculates average sentence length in words."""
        sentences = re.findall(r'([^.!?…]+)[.!?…]+', text)
        if not sentences: return 0
        
        total_words = sum(len(re.findall(r"\b[a-zA-Zа-яА-ЯёЁ]+\b", s)) for s in sentences)
        return total_words / len(sentences)
        
    @staticmethod
    def get_average_len_word(text):
        """Calculates average word length in characters."""
        words = re.findall(r"\b[a-zA-Zа-яА-ЯёЁ]+\b", text)
        if not words: return 0
        
        total_chars = sum(len(word) for word in words)
        return total_chars / len(words)
        
    @staticmethod
    def get_count_emoji(text):
        """Counts specific emojis like :-), ;-[[, :] """
        return len(re.findall(r'[;:][-]*(?:\(+|\)+|\[+|\]+)', text))


class Service:
    """Main presentation layer coordinating Task 2 logic."""
    
    @staticmethod
    def presentation():
        """Executes text analysis, prints results, and saves them to archive."""
        print("\n--- [ TEXT ANALYSIS (TASK 2) ] ---")
        
        reader = FileManager(TaskStorage.filename)
        TaskStorage.data = reader.read_file()
        
        if not TaskStorage.data:
            return

        # Replace text based on user input
        replaced_text = IndividualTaskService.replace_space(TaskStorage.data)
        print("\n[Preview of Text with Replaced Spaces]:")
        print(replaced_text[:100] + "...\n") 

        # Gathering all statistics
        results = {
            "Contains GUID": IndividualTaskService.check_guid(TaskStorage.data),
            "Count of 3-letter words": IndividualTaskService.get_count_3_len(TaskStorage.data),
            "Words with equal vowels/consonants": IndividualTaskService.find_words_with_equal_vowels_consonants(TaskStorage.data),
            "Total sentences": CommonTaskService.get_count_sentence(TaskStorage.data),
            "Declarative sentences": CommonTaskService.get_declarative_count(TaskStorage.data),
            "Interrogative sentences": CommonTaskService.get_interrogative_count(TaskStorage.data),
            "Exclamatory sentences": CommonTaskService.get_exclamatory_count(TaskStorage.data),
            "Average sentence length (words)": round(CommonTaskService.get_average_len_sentence(TaskStorage.data), 2),
            "Average word length (chars)": round(CommonTaskService.get_average_len_word(TaskStorage.data), 2),
            "Count of emojis": CommonTaskService.get_count_emoji(TaskStorage.data),
            "Sorted words by length (preview)": IndividualTaskService.sort_words(TaskStorage.data)
        }

        # Print results
        for key, value in results.items():
            print(f"{key:.<40}: {value}")

        # Save results to text file
        writer = FileManager(TaskStorage.filename_result)
        writer.write_results(results)
        print("\n" + writer.get_info()) 
        
        # Archive the result file
        zipper = ZipManager(TaskStorage.zipname)
        zipper.create_zip(TaskStorage.filename_result)
        print(zipper.get_info()) 