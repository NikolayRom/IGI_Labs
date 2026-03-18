"""
Brief purpose: Module for Task 5. Exploring NumPy capabilities and sorting a random matrix.
Lab number and title: Lab 4 - Working with files, classes, serializers, regular expressions, and standard libraries
Version: 1.0
Developer: Romanov Nikolay Viktorovich
Date: 17.03.2026
"""

import numpy as np
from validation import Validation


class NumpyDemonstrationMixin:
    """
    Mixin class to demonstrate basic NumPy capabilities (General Task).
    Demonstrates array creation, indexing, slicing, and statistical operations.
    """
    
    def demonstrate_numpy_features(self, matrix):
        """Demonstrates general NumPy features requested in the assignment."""
        print("\n" + "="*50)
        print("---[ NUMPY CAPABILITIES DEMONSTRATION ] ---")
        
        # Creation: array() and values()
        sample_dict = {'x': 10, 'y': 20, 'z': 30}
        arr_from_values = np.array(list(sample_dict.values()))
        print(f"1. np.array() from dict values(): {arr_from_values}")
        
        # Specific arrays
        zeros_arr = np.zeros((2, 2), dtype=int)
        ones_arr = np.ones((2, 2), dtype=int)
        print(f"2. Specific arrays (zeros):\n{zeros_arr}\n(ones):\n{ones_arr}")
        
        # Indexing and slicing
        if matrix.shape[0] > 1 and matrix.shape[1] > 1:
            print(f"3. Indexing (element [0, 0]): {matrix[0, 0]}")
            print(f"   Slicing (first row): {matrix[0, :]}")
            print(f"   Slicing (last column): {matrix[:, -1]}")
            
        # Element-wise universal functions
        print("4. Element-wise operations (Matrix + 100):\n", matrix + 100)
        
        print("\n---[ MATH & STATS OPERATIONS DEMONSTRATION ] ---")
        # Demonstrating stats on the generated matrix
        print(f"1. Mean (np.mean): {np.mean(matrix):.2f}")
        print(f"2. Median (np.median): {np.median(matrix):.2f}")
        
        # Calculate correlation between the rows of the matrix
        correlation = np.corrcoef(matrix)
        print("3. Correlation coefficient (np.corrcoef) preview (first 2x2):\n", correlation[:2, :2])
        
        print(f"4. Variance (np.var): {np.var(matrix):.2f}")
        print(f"5. Standard Deviation (np.std): {np.std(matrix):.2f}")
        print("="*50 + "\n")


class BaseMatrix(NumpyDemonstrationMixin):
    """Base class handling the creation and storage of the random matrix."""
    
    def __init__(self, n, m):
        """Initializes dimensions and generates random matrix A[n, m]."""
        self._n = n
        self._m = m
        # Generating integer matrix using random generator
        self._matrix = np.random.randint(10, 100, size=(n, m))
        
    @property
    def matrix(self):
        """Property to access the encapsulated matrix."""
        return self._matrix
        
    def __str__(self):
        """String representation of the matrix."""
        return str(self._matrix)


class VariantMatrix(BaseMatrix):
    """Child class to execute the individual variant task."""
    
    def __init__(self, n, m):
        super().__init__(n, m)
        
    def get_sorted_by_last_column(self):
        """
        Sorts the matrix in descending order based on the last column.
        """
        # Get the last column
        last_col = self._matrix[:, -1]
        # Get sorted indices in ascending order, then reverse them [::-1] for descending
        sorted_indices = np.argsort(last_col)[::-1]
        # Return new matrix sliced by sorted indices
        return self._matrix[sorted_indices]
        
    def get_last_col_mean_standard(self):
        """Calculates the mean of the last column using standard NumPy function."""
        last_col = self._matrix[:, -1]
        mean_val = np.mean(last_col)
        return round(mean_val, 2)
        
    def get_last_col_mean_manual(self):
        """Calculates the mean of the last column using a manually programmed formula."""
        last_col = self._matrix[:, -1]
        
        total_sum = 0
        for value in last_col:
            total_sum += value
            
        mean_val = total_sum / len(last_col)
        return round(mean_val, 2)


class Service:
    """Main presentation layer coordinating Task 5 logic."""
    
    @staticmethod
    def get_valid_dimension(prompt):
        """Validates that matrix dimensions are at least 2."""
        return Validation.inputMatrixDimension(prompt)

    @staticmethod
    def presentation():
        print("\n---[ TASK 5: NUMPY MATRICES & OPERATIONS ] ---")
        
        # User input for Matrix size
        n = Service.get_valid_dimension("Enter number of rows (n >= 2): ")
        m = Service.get_valid_dimension("Enter number of columns (m >= 2): ")
        
        # Create the Variant Matrix Object
        task_matrix = VariantMatrix(n, m)
        
        # Demonstrate General NumPy Features 
        task_matrix.demonstrate_numpy_features(task_matrix.matrix)
        
        # --- Individual Task Demonstration ---
        print("--- [ INDIVIDUAL TASK RESULTS ] ---")
        print("1. Original Matrix A[n, m]:")
        print(task_matrix)
        
        sorted_mat = task_matrix.get_sorted_by_last_column()
        print("\n2. Matrix sorted in DESCENDING order of the LAST column:")
        print(sorted_mat)
        
        mean_std = task_matrix.get_last_col_mean_standard()
        mean_man = task_matrix.get_last_col_mean_manual()
        
        print("\n3. Average of the last column:")
        print(f"   -> Using standard function (np.mean): {mean_std}")
        print(f"   -> Using programmed formula (sum/len): {mean_man}")
        
        # Double check if both methods yield the same result
        if mean_std == mean_man:
            print("\n[SUCCESS] Both average calculation methods match!")