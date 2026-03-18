"""
Brief purpose: Module for Task 4. OOP implementation of geometric figures (Rhombus) with drawing capabilities.
Lab number and title: Lab 4 - Working with files, classes, serializers, regular expressions, and standard libraries
Version: 1.0
Developer: Romanov Nikolay Viktorovich
Date: 17.03.2026
"""

import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from abc import ABC, abstractmethod
from validation import Validation


class FigureColor:
    """Class to encapsulate the color of a figure using properties."""
    def __init__(self, color):
        self._color = color
        
    @property
    def color(self):
        """Getter for the color property."""
        return self._color
        
    @color.setter
    def color(self, new_color):
        """Setter for the color property."""
        self._color = new_color


class GeometricFigure(ABC):
    """Abstract base class for all geometric figures."""
    
    @abstractmethod
    def calculate_area(self):
        """Abstract method to calculate the area of the figure."""
        pass


class Rhombus(GeometricFigure):
    """Class representing a Rhombus. Inherits from GeometricFigure."""
    
    # Class attribute for the figure name
    _figure_name = "Ромб"
    
    @classmethod
    def get_figure_name(cls):
        """Class method returning the name of the figure."""
        return cls._figure_name

    def __init__(self, a, r_angle, color):
        """
        Constructor for Rhombus.
        :param a: side length
        :param r_angle: obtuse angle in degrees (90 < R < 180)
        :param color: string representing color
        """
        self.a = a
        self.r_angle = r_angle
        # Creating FigureColor object inside the constructor
        self._color_obj = FigureColor(color)
        
    @property
    def color(self):
        """Property to access the color from the internal FigureColor object."""
        return self._color_obj.color

    def calculate_area(self):
        """
        Overrides the abstract method.
        Calculates area of a rhombus: Area = a^2 * sin(angle).
        Uses math module to convert degrees to radians and calculate sine.
        """
        radians = math.radians(self.r_angle)
        return (self.a ** 2) * math.sin(radians)

    def get_info(self):
        """Returns formatted string with basic parameters, color, and area."""
        area = self.calculate_area()
        # Using the .format() method 
        return "{0} {1} цвета со стороной {2} и тупым углом {3}°. Площадь: {4:.2f}".format(
            self.get_figure_name(),
            self.color,
            self.a,
            self.r_angle,
            area
        )


class PlotService:
    """Service to handle drawing and saving the figure using Matplotlib."""
    
    @staticmethod
    def draw_rhombus(rhombus_obj, label_text):
        """Calculates vertices of the rhombus and draws it on a plot."""
        print("\nGenerating drawing...")
        
        # Calculate the acute angle for drawing purposes
        acute_angle_deg = 180 - rhombus_obj.r_angle
        alpha_rad = math.radians(acute_angle_deg)
        a = rhombus_obj.a
        
        # Calculate vertices (Bottom-Left, Bottom-Right, Top-Right, Top-Left)
        # Assuming bottom-left starts at (0,0) and bottom edge lies on X axis
        x0, y0 = 0, 0
        x1, y1 = a, 0
        x2, y2 = a + a * math.cos(alpha_rad), a * math.sin(alpha_rad)
        x3, y3 = a * math.cos(alpha_rad), a * math.sin(alpha_rad)
        
        vertices = [[x0, y0],[x1, y1], [x2, y2], [x3, y3]]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create and add the polygon
        polygon = Polygon(vertices, closed=True, facecolor=rhombus_obj.color, edgecolor='black', linewidth=2)
        ax.add_patch(polygon)
        
        # Configure axes limits to ensure the figure is centered and visible
        ax.set_xlim(-0.5 * a, 2.5 * a)
        ax.set_ylim(-0.5 * a, 1.5 * a)
        ax.set_aspect('equal') 
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Add the custom text label in the center of the rhombus
        center_x = (x0 + x1 + x2 + x3) / 4
        center_y = (y0 + y1 + y2 + y3) / 4
        ax.text(center_x, center_y, label_text, ha='center', va='center', 
                fontsize=12, fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, edgecolor='black'))
                
        # Set title using the formatted info string
        plt.title(rhombus_obj.get_info())
        
        # Output to file and screen
        filename = "task4_rhombus.png"
        plt.savefig(filename)
        print(f"Figure successfully saved to '{filename}'.")
        plt.show()


class Service:
    """Main presentation layer coordinating Task 4 logic."""
    
    @staticmethod
    def get_valid_side():
        """Validates that the side length is positive."""
        return Validation.inputFigureSide("Enter rhombus side length (a > 0): ")

    @staticmethod
    def get_valid_angle():
        """Validates that the angle is strictly obtuse (between 90 and 180 degrees)."""
        return Validation.inputFigureAngle("Enter obtuse angle in degrees (90 < R < 180): ")

    @staticmethod
    def get_valid_color():
        """Validates if the entered string is a recognizable color in Matplotlib."""
        return Validation.inputFigureColor("Enter color (e.g., 'red', 'blue', 'green', 'magenta', '#FF5733'): ")

    @staticmethod
    def presentation():
        print("\n---[ TASK 4: GEOMETRIC FIGURES (RHOMBUS) ] ---")
        
        # User input with strict correctness validation
        side_a = Service.get_valid_side()
        
        angle_r = Service.get_valid_angle()
        
        color = Service.get_valid_color()
        
        label_text = Validation.inputStr("Enter a text label for the figure: ")
        
        # Construct object
        my_rhombus = Rhombus(side_a, angle_r, color)
        
        # Print info
        print("\nFigure Info:")
        print(my_rhombus.get_info())
        
        # Draw, label, color, output to screen and file
        PlotService.draw_rhombus(my_rhombus, label_text)