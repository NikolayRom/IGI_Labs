import csv
import pickle


class Students:
    __default = {
        "Nikolay": [8, 8, 10],
        "Vladislav": [4, 10, 8],
        "Sergey": [9, 2, 2],
        "Maksim": [8, 10, 9],
        "Ivan": [5, 6, 4]
    }

    @classmethod
    def default(cls):
        return cls.__default
    def __init__(self):
        self.__students = Students.default()
    @property
    def students(self):
        return self.__students
    @students.setter
    def students(self, dict_obj):
        self.__students = dict_obj
    @property
    def grades_type(self):
        return len(next(iter(self.__students.values())))


class TaskStorage:
    filename_csv = "task1.csv"
    filename_txt = "task1.txt"
    study = Students()
    excellent_grade = 8
    satisfactory_grade = 4
    grades_count = study.grades_type * len(study.students)
    satisfactory_grades_count = 0
    excellent_grades_count = 0
    failing_students = []
    excellent_students = []
    @classmethod
    def clear(cls):
        cls.satisfactory_grades_count = 0
        cls.excellent_grades_count = 0
        cls.failing_students = []
        cls.excellent_students = []


class CSVService:
    @staticmethod
    def serialization():
        TaskStorage.clear()
        with open(TaskStorage.filename_csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["name", "rus", "phys", "math"], quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for name, grades in sorted(TaskStorage.study.students.items()):
                writer.writerow(dict(name = name, rus = grades[0], phys = grades[1], math = grades[2]))
    @staticmethod
    def deserialization():
        with open(TaskStorage.filename_csv, 'r', encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            reader = list(reader)

            for student in reader:
                student_grades = [int(student['rus']), int(student['phys']), int(student['math'])]
                is_excellent_student = True
                is_failing_student = False

                for grade in student_grades:
                    if grade >= TaskStorage.excellent_grade:
                        TaskStorage.excellent_grades_count += 1
                        TaskStorage.satisfactory_grades_count += 1
                    elif grade >= TaskStorage.satisfactory_grade:
                        is_excellent_student = False
                        TaskStorage.satisfactory_grades_count += 1
                    else:
                        is_excellent_student = False
                        is_failing_student = True

                if is_excellent_student:
                    TaskStorage.excellent_students.append(student)
                elif is_failing_student:
                    TaskStorage.failing_students.append(student)


class ConsoleService:
    @staticmethod
    def printStatisticsPerformance():
        print(TaskStorage.satisfactory_grades_count * 100 / TaskStorage.grades_count)
    @staticmethod
    def printQualityPerformance():
        print(TaskStorage.excellent_grades_count * 100 / TaskStorage.grades_count)
    @staticmethod
    def printExcellentStudents():
        print(TaskStorage.excellent_students)
    @staticmethod
    def printFailingStudents():
        print(TaskStorage.failing_students)


class SearchService:
    @staticmethod
    def searchCVS():
        print(CSVSearch(TaskStorage.filename_csv, input("Enter name: ")))
    @staticmethod
    def searchPickle():
        print(PickleSearch(TaskStorage.filename_txt, input("Enter name: ")))


class CSVSearch:
    def __init__(self, filename, name):
        self.__filename = filename
        self.__name = name
    def findStudent(self):
        with open(self.__filename, "r") as fh:
            reader = csv.DictReader(fh)
            for student in reader:
                if(student["name"] == self.__name):
                    return student
    def __str__(self):
        return str(self.findStudent())


class PickleService:
    @staticmethod
    def serialization():
        TaskStorage.clear()
        with open(TaskStorage.filename_txt, "wb") as fh:
            pickle.dump(TaskStorage.study.students, fh)
    @staticmethod
    def deserialization():
        with open(TaskStorage.filename_txt, 'rb') as fh:
            reader = pickle.load(fh)

            for student in reader.keys():
                is_excellent_student = True
                is_failing_student = False

                for grade in reader.get(student):
                    if grade >= TaskStorage.excellent_grade:
                        TaskStorage.excellent_grades_count += 1
                        TaskStorage.satisfactory_grades_count += 1
                    elif grade >= TaskStorage.satisfactory_grade:
                        is_excellent_student = False
                        TaskStorage.satisfactory_grades_count += 1
                    else:
                        is_excellent_student = False
                        is_failing_student = True

                if is_excellent_student:
                    TaskStorage.excellent_students.append({student: reader.get(student)})
                elif is_failing_student:
                    TaskStorage.failing_students.append({student: reader.get(student)})


class PickleSearch:
    def __init__(self, filename, name):
        self.__filename = filename
        self.__name = name
    def findStudent(self):
        with open(self.__filename, "rb") as fh:
            reader = pickle.load(fh)
            if not reader.get(self.__name):
                return None
            return {self.__name: reader.get(self.__name)}
    def __str__(self):
        return str(self.findStudent())


class Service():
    @staticmethod
    def presentation():
        CSVService.serialization()
        CSVService.deserialization()
        
        ConsoleService.printStatisticsPerformance()
        ConsoleService.printQualityPerformance()
        ConsoleService.printExcellentStudents()
        ConsoleService.printFailingStudents()

        SearchService.searchCVS()

        PickleService.serialization()
        PickleService.deserialization()

        ConsoleService.printStatisticsPerformance()
        ConsoleService.printQualityPerformance()
        ConsoleService.printExcellentStudents()
        ConsoleService.printFailingStudents()

        SearchService.searchPickle()


Service.presentation()