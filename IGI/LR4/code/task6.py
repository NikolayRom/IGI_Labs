"""
Brief purpose: Module for Task 6. Data analysis using Pandas (Series, DataFrame, Statistics).
Lab number and title: Lab 4 - Working with files, classes, serializers, regular expressions, and standard libraries
Version: 1.0
Developer: Romanov Nikolay Viktorovich
Date: 18.03.2026
"""

import os
import pandas as pd
from abc import ABC, abstractmethod

try:
    from IPython.display import display
except ImportError:
    display = print


class PandasDemoMixin:
    """Mixin class to demonstrate basic Pandas features (Part A General)."""
    
    def demonstrate_series_features(self):
        """Demonstrates Series creation, display, .loc, and .iloc operations."""
        print("\n--- [ PART A: PANDAS CAPABILITIES DEMONSTRATION ] ---")
        
        # Creating a Series
        data_list =[404, 502, 200]
        index_labels = ['Not Found', 'Bad Gateway', 'OK']
        my_series = pd.Series(data_list, index=index_labels, name="HTTP_Codes")
        
        print("\n[Created Series object]:")
        # The display function
        display(my_series)
        
        # Access via .loc and .iloc
        print("\n[Accessing elements in Series]:")
        print(f"Using .loc['Bad Gateway'] (by label): {my_series.loc['Bad Gateway']}")
        print(f"Using .iloc[0] (by index 0): {my_series.iloc[0]}")


class BaseDataAnalyzer(ABC):
    """Abstract base class for Data Analysis. Demonstrates OOP and ABC."""
    
    def __init__(self, filepath):
        self._filepath = filepath
        self._df = None
        
    @property
    def dataframe(self):
        """Property getter for the loaded dataframe."""
        return self._df
        
    @abstractmethod
    def load_data(self):
        """Abstract method to load data from the source."""
        pass


class CyberSecurityAnalyzer(BaseDataAnalyzer, PandasDemoMixin):
    """Class handling the Cyber Security Dataset logic. Demonstrates Inheritance and Mixins."""
    
    def __init__(self, filepath):
        super().__init__(filepath)

    def load_data(self):
        """Polymorphism: Overrides load_data to read CSV specifically."""
        if os.path.exists(self._filepath):
            self._df = pd.read_csv(self._filepath)
            print(f"\n[Success] Dataset '{self._filepath}' loaded successfully. Rows: {len(self._df)}")
        else:
            print(f"\n[Error] File '{self._filepath}' not found! Make sure it is located next to the script.")
            self._df = pd.DataFrame() # Fallback to empty dataframe

    def part_a_individual(self):
        """
        Executes Part A Individual Task:
        Create empty DataFrame, add 3 columns, add 2 rows from the dataset.
        """
        print("\n--- [ PART A (Individual task): EMPTY DATAFRAME ] ---")
        
        # Creating an empty DataFrame and Adding 3 columns
        empty_df = pd.DataFrame(columns=['attack_type', 'severity', 'duration'])
        
        print("\n[Empty DataFrame created with specified columns]:")
        display(empty_df)
        
        # Adding 2 data rows from the loaded dataset
        if self._df is not None and not self._df.empty and len(self._df) >= 2:
            row1 = self._df.iloc[0]
            row2 = self._df.iloc[1]
            
            # Extract the required columns: Attack Type, Severity Level, Packet Length
            empty_df.loc[0] =[row1['Attack Type'], row1['Severity Level'], row1['Packet Length']]
            empty_df.loc[1] = [row2['Attack Type'], row2['Severity Level'], row2['Packet Length']]
            
            print("\n[DataFrame after adding 2 rows from the Kaggle dataset]:")
            display(empty_df)
        else:
            print("\n[Warning] Main dataset is not loaded. Cannot add rows.")

    def part_b_general(self):
        """Executes Part B General Task: DataFrame information and basic stats."""
        print("\n--- [ PART B (General task): DATAFRAME INFORMATION ] ---")
        if self._df is None or self._df.empty:
            print("No data for analysis.")
            return

        print("\n[DataFrame information (.info())]:")
        self._df.info()
        
        print("\n[Basic statistics for numerical columns (.describe())]:")
        display(self._df.describe())

    def part_b_individual(self):
        """
        Executes Part B Individual Task:
        Ratio of average duration (Packet Length) of MAX severity ("High") vs MIN severity ("Low").
        """
        print("\n--- [ PART B (Individual task): STATISTICAL ANALYSIS ] ---")
        if self._df is None or self._df.empty:
            print("No data for analysis.")
            return
            
        try:            
            # Extract data using boolean indexing and calculate the mean
            mean_duration_max = self._df[self._df['Severity Level'] == 'High']['Packet Length'].mean()
            mean_duration_min = self._df[self._df['Severity Level'] == 'Low']['Packet Length'].mean()
            
            print(f"Max severity ('High') -> Average 'Packet Length': {mean_duration_max:.2f}")
            print(f"Min severity ('Low')  -> Average 'Packet Length': {mean_duration_min:.2f}")
            
            if pd.isna(mean_duration_max) or pd.isna(mean_duration_min):
                print("Data is missing for one of the severity levels in the dataset.")
                return

            if mean_duration_min == 0:
                print("Error: Average duration of minimal attacks is 0 (Division by zero).")
            else:
                ratio = mean_duration_max / mean_duration_min
                # Round to 2 decimal places
                print(f"\n[RESULT]: The average metric of max severity attacks is {round(ratio, 2)} times greater than the min severity attacks.")
                      
        except KeyError as e:
            print(f"Error: Required column {e} not found in the dataset.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


class Service:
    """Main presentation layer coordinating Task 6 logic."""
    
    @staticmethod
    def presentation():
        print("\n" + "="*50)
        print(f"{'TASK 6: PANDAS & KAGGLE DATASET':^50}")
        print("="*50)
        
        # Name of the downloaded dataset
        filepath = "cybersecurity_attacks.csv"
        
        analyzer = CyberSecurityAnalyzer(filepath)
        analyzer.load_data()
        
        # Execute Part A
        analyzer.demonstrate_series_features()
        analyzer.part_a_individual()
        
        # Execute Part B
        analyzer.part_b_general()
        analyzer.part_b_individual()
        
        print("\n" + "="*50)