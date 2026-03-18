"""
Brief purpose: Module for Task 1. Works with dictionaries, CSV, and Pickle serialization.
Lab number and title: Lab 4 - Working with files, classes, serializers, regular expressions, and standard libraries
Version: 1.0
Developer: Romanov Nikolay Viktorovich
Date: 15.03.2026
"""

import csv
import pickle
from validation import Validation


class Students:
    """Class representing a collection of students and their grades."""
    
    __default = {
        "Nikolay": [8, 8, 10],
        "Vladislav": [4, 10, 8],
        "Sergey":[9, 2, 2],
        "Maksim": [8, 10, 9],
        "Ivan":[5, 6, 4]
    }

    @classmethod
    def default(cls):
        """Class method to return default students data."""
        return cls.__default
        
    def __init__(self):
        """Magic method: constructor to initialize dynamic attributes."""
        self.__students = Students.default()
        
    @property
    def students(self):
        """Getter for students dictionary (Requirement 4)."""
        return self.__students
        
    @students.setter
    def students(self, dict_obj):
        """Setter for students dictionary (Requirement 4)."""
        self.__students = dict_obj
        
    @property
    def grades_type(self):
        """Getter returning the number of subjects per student."""
        return len(next(iter(self.__students.values())))


class TaskStorage:
    """Static class for storing configuration and runtime data."""
    filename_csv = "task1.csv"
    filename_txt = "task1.txt"
    study = Students()
    excellent_grade = 8
    satisfactory_grade = 4
    grades_count = study.grades_type * len(study.students)
    
    satisfactory_grades_count = 0
    excellent_grades_count = 0
    failing_students = []
    excellent_students =[]

    @classmethod
    def clear(cls):
        """Class method to clear lists and counters before new operations."""
        cls.satisfactory_grades_count = 0
        cls.excellent_grades_count = 0
        cls.failing_students =[]
        cls.excellent_students =[]


class CSVService:
    """Service class for CSV operations."""
    
    @staticmethod
    def serialization():
        """Serializes dictionary data into a CSV file."""
        TaskStorage.clear()
        with open(TaskStorage.filename_csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["name", "rus", "phys", "math"], quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for name, grades in sorted(TaskStorage.study.students.items()):
                writer.writerow(dict(name=name, rus=grades[0], phys=grades[1], math=grades[2]))
                
    @staticmethod
    def deserialization():
        """Deserializes CSV file and calculates statistics."""
        with open(TaskStorage.filename_csv, 'r', encoding="utf-8", newline="") as fh:
            reader = list(csv.DictReader(fh))

            for student in reader:
                student_grades = [int(student['rus']), int(student['phys']), int(student['math'])]
                is_excellent = True
                is_failing = False

                for grade in student_grades:
                    if grade >= TaskStorage.excellent_grade:
                        TaskStorage.excellent_grades_count += 1
                        TaskStorage.satisfactory_grades_count += 1
                    elif grade >= TaskStorage.satisfactory_grade:
                        is_excellent = False
                        TaskStorage.satisfactory_grades_count += 1
                    else:
                        is_excellent = False
                        is_failing = True

                if is_excellent:
                    TaskStorage.excellent_students.append(student)
                elif is_failing:
                    TaskStorage.failing_students.append(student)


class PickleService:
    """Service class for Pickle operations."""
    
    @staticmethod
    def serialization():
        """Serializes dictionary data into a binary file using Pickle."""
        TaskStorage.clear()
        with open(TaskStorage.filename_txt, "wb") as fh:
            pickle.dump(TaskStorage.study.students, fh)
            
    @staticmethod
    def deserialization():
        """Deserializes Pickle file and calculates statistics."""
        with open(TaskStorage.filename_txt, 'rb') as fh:
            reader = pickle.load(fh)

            for student_name, grades in reader.items():
                is_excellent = True
                is_failing = False

                for grade in grades:
                    if grade >= TaskStorage.excellent_grade:
                        TaskStorage.excellent_grades_count += 1
                        TaskStorage.satisfactory_grades_count += 1
                    elif grade >= TaskStorage.satisfactory_grade:
                        is_excellent = False
                        TaskStorage.satisfactory_grades_count += 1
                    else:
                        is_excellent = False
                        is_failing = True

                if is_excellent:
                    TaskStorage.excellent_students.append({student_name: grades})
                elif is_failing:
                    TaskStorage.failing_students.append({student_name: grades})


class ConsoleService:
    """Service for displaying data in a user-friendly format."""
    
    @staticmethod
    def printStatisticsPerformance():
        """Prints the percentage of satisfactory performance."""
        perc = TaskStorage.satisfactory_grades_count * 100 / TaskStorage.grades_count
        print(f"Overall performance (satisfactory+): {perc:.1f}%")

    @staticmethod
    def printQualityPerformance():
        """Prints the percentage of excellent performance."""
        perc = TaskStorage.excellent_grades_count * 100 / TaskStorage.grades_count
        print(f"Quality performance (excellent): {perc:.1f}%")

    @staticmethod
    def printExcellentStudents():
        """Prints the list of excellent students."""
        print(f"Excellent students: {TaskStorage.excellent_students}")

    @staticmethod
    def printFailingStudents():
        """Prints the list of failing students."""
        print(f"Failing students: {TaskStorage.failing_students}")


class SearchMixin:
    """Mixin class to add formatted print capabilities (Requirement 4: Mixin)."""
    def print_result(self, result):
        if result:
            print(f"[Search Success] Found: {result}")
        else:
            print("[Search Failed] Student not found.")


class BaseSearch(SearchMixin):
    """Base class for searching students. Demonstrates Inheritance."""
    
    def __init__(self, filename, name):
        """Initializes protected dynamic attributes."""
        self._filename = filename
        self._name = name
        
    def findStudent(self):
        """Abstract method to be overridden (Polymorphism)."""
        raise NotImplementedError("This method must be overridden in subclasses.")
        
    def __str__(self):
        """Magic method (Requirement 4) to return string representation."""
        return str(self.findStudent())


class CSVSearch(BaseSearch):
    """Class to search within CSV files. Inherits from BaseSearch."""
    
    def __init__(self, filename, name):
        super().__init__(filename, name)
        
    def findStudent(self):
        """Polymorphism: overriding the base method for CSV specific logic."""
        with open(self._filename, "r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for student in reader:
                if student["name"] == self._name:
                    return student
        return None


class PickleSearch(BaseSearch):
    """Class to search within Pickle files. Inherits from BaseSearch."""
    
    def __init__(self, filename, name):
        super().__init__(filename, name)
        
    def findStudent(self):
        """Polymorphism: overriding the base method for Pickle specific logic."""
        with open(self._filename, "rb") as fh:
            reader = pickle.load(fh)
            if not reader.get(self._name):
                return None
            return {self._name: reader.get(self._name)}


class SearchService:
    """Service to prompt user and initiate search."""
    
    @staticmethod
    def searchCSV():
        """Prompts user and searches via CSV."""
        name = Validation.inputStr("Enter student name to search in CSV: ")
        search_obj = CSVSearch(TaskStorage.filename_csv, name)
        search_obj.print_result(search_obj.findStudent()) # Using Mixin method

    @staticmethod
    def searchPickle():
        """Prompts user and searches via Pickle."""
        name = Validation.inputStr("Enter student name to search in Pickle: ")
        search_obj = PickleSearch(TaskStorage.filename_txt, name)
        search_obj.print_result(search_obj.findStudent()) # Using Mixin method


class Service:
    """Main presentation layer coordinating Task 1 logic."""
    
    @staticmethod
    def presentation():
        """Runs the demonstration of CSV and Pickle processing."""
        
        print("\n--- [ CSV PROCESSING ] ---")
        CSVService.serialization()
        CSVService.deserialization()
        
        ConsoleService.printStatisticsPerformance()
        ConsoleService.printQualityPerformance()
        ConsoleService.printExcellentStudents()
        ConsoleService.printFailingStudents()
        
        SearchService.searchCSV()

        print("\n--- [ PICKLE PROCESSING ] ---")
        PickleService.serialization()
        PickleService.deserialization()

        ConsoleService.printStatisticsPerformance()
        ConsoleService.printQualityPerformance()
        ConsoleService.printExcellentStudents()
        ConsoleService.printFailingStudents()

        SearchService.searchPickle()