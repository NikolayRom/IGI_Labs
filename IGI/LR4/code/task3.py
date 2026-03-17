"""
Brief purpose: Module for Task 3. Taylor series calculation, statistics with NumPy, and plotting with Matplotlib.
Lab number and title: Lab 4 - Работа с файлами, классами, сериализаторами, регулярными выражениями и стандартными библиотеками
Version: 1.0
Developer: Романов Николай Викторович
Date: 15.03.2026
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from validation import Validation

class SeriesStatsMixin:
    """Mixin class providing statistical calculations using NumPy (Requirement 4)."""
    
    def calculate_statistics(self, sequence):
        """Calculates mean, median, mode, variance, and standard deviation."""
        data = np.array(sequence)
        
        # 1) Mean
        mean_val = np.mean(data)
        # 2) Median
        median_val = np.median(data)
        # 3) Mode
        values, counts = np.unique(data, return_counts=True)
        mode_val = values[np.argmax(counts)]
        # 4) Variance
        var_val = np.var(data)
        # 5) Standard Deviation
        std_val = np.std(data)
        
        return {
            "Mean": mean_val,
            "Median": median_val,
            "Mode": mode_val,
            "Variance": var_val,
            "Standard Deviation": std_val
        }


class BaseSeries(SeriesStatsMixin):
    """Base class for math series calculations. Demonstrates inheritance."""
    
    def __init__(self, x, eps):
        self._x = x
        self._eps = eps
        self._exact_value = self._calculate_exact()
        
    def _calculate_exact(self):
        """Abstract method for exact value calculation."""
        raise NotImplementedError("Must be overridden in subclasses.")


class LogTaylorSeries(BaseSeries):
    """Class specific to calculating ln(1+x) using Taylor Series."""
    
    def __init__(self, x, eps):
        super().__init__(x, eps)
        self.n = 0
        self.f_value = 0.0
        self.partial_sums =[]
        
    def _calculate_exact(self):
        """Polymorphism: exact value for ln(1+x)."""
        return math.log(1 + self._x)
        
    def _term(self, n):
        """Calculates the n-th term of the series."""
        return ((-1) ** (n - 1)) * (self._x ** n) / n
        
    def calculate_series(self):
        """Calculates the Taylor series and tracks partial sums."""
        max_iter = 500
        current_sum = 0.0
        
        for i in range(1, max_iter + 1):
            term = self._term(i)
            current_sum += term
            self.partial_sums.append(current_sum)
            
            if abs(term) <= self._eps:
                self.n = i
                self.f_value = current_sum
                break
        else:
            self.n = max_iter
            self.f_value = current_sum
            print(f"\nWarning: Max iterations ({max_iter}) reached.")

    def get_results(self):
        """Returns the series calculation results."""
        return self._x, self.n, self.f_value, self._exact_value, self._eps


class PlotService:
    """Service class to handle Matplotlib operations."""
    
    @staticmethod
    def draw_and_save_plot(target_x, target_n):
        """Draws the function and its Taylor approximation, saves to file."""
        print("\nGenerating and saving plot...")
        
        x_vals = np.linspace(-0.95, 0.95, 200)
        y_exact = np.log(1 + x_vals)
        
        # Calculate Taylor approximation for all x_vals up to target_n
        y_approx = np.zeros_like(x_vals)
        for i in range(1, target_n + 1):
            y_approx += ((-1) ** (i - 1)) * (x_vals ** i) / i

        plt.figure(figsize=(10, 6))
        
        # Plotting lines with different colors
        plt.plot(x_vals, y_exact, label='Math F(x) = ln(1+x)', color='blue', linewidth=2)
        plt.plot(x_vals, y_approx, label=f'Taylor Series (n={target_n})', color='red', linestyle='--')
        
        # Adding Coordinate axes and Grid
        plt.axhline(0, color='black',linewidth=1)
        plt.axvline(0, color='black',linewidth=1)
        plt.xlabel('Argument x')
        plt.ylabel('Function Value F(x)')
        plt.title('Taylor Series Approximation vs Exact Function')
        plt.grid(True)
        
        # Adding Legend
        plt.legend(loc="upper left")
        
        # Adding Text
        plt.text(-0.9, min(y_exact) * 0.8, "Approximation converges well\nfor |x| < 1", 
                 fontsize=10, bbox=dict(facecolor='lightyellow', alpha=0.7))
        
        # Adding Annotation pointing to the user's evaluated point
        target_y = math.log(1 + target_x)
        plt.annotate(f'Evaluated Point\n(x={target_x:.2f})', 
                     xy=(target_x, target_y), 
                     xytext=(target_x - 0.3, target_y + 0.5),
                     arrowprops=dict(facecolor='green', shrink=0.05))
        
        # Save to file
        filename = 'task3_plot.png'
        plt.savefig(filename)
        print(f"Plot successfully saved as '{filename}'.")
        
        # Display the plot
        plt.show()


class Service:
    """Main presentation layer coordinating Task 3 logic."""
    
    @staticmethod
    def print_table(x, n, f_val, exact_val, eps):
        """Prints formatted result table."""
        print('\n' + '-' * 75)
        print(f'| {"x":^10} | {"n":^5} | {"F(x)":^15} | {"Math F(x)":^15} | {"eps":^10} |')
        print('-' * 75)
        print(f'| {x:^10.4f} | {n:^5} | {f_val:^15.6f} | {exact_val:^15.6f} | {eps:^10.6f} |')
        print('-' * 75 + '\n')

    @staticmethod
    def presentation():
        print("\n---[ TASK 3: TAYLOR SERIES & STATISTICS ] ---")
        
        eps = Validation.inputEpsila("Enter epsilon (calculation accuracy, e.g., 0.001): ")
        x = Validation.inputArgumentX("Enter argument x (|x| < 1): ")
        
        # Calculation
        series_obj = LogTaylorSeries(x, eps)
        series_obj.calculate_series()
        
        # Display Table
        results = series_obj.get_results()
        Service.print_table(*results)
        
        # Sequence Statistics (NumPy)
        print("--- Statistics of Partial Sums Sequence ---")
        stats = series_obj.calculate_statistics(series_obj.partial_sums)
        for key, value in stats.items():
            print(f"{key}: {value:.6f}")
            
        # Matplotlib Plot
        PlotService.draw_and_save_plot(x, series_obj.n)