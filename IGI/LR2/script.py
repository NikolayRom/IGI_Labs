import sys
import os
sys.path.append('/app/geometric_lib')

from circle import area as circle_area, perimeter as circle_perimeter
from square import area as square_area, perimeter as square_perimeter

radius = int(os.getenv('RADIUS', '5'))
side = int(os.getenv('SIDE', '4'))

print("\n=================================================")
print(f"\nCircle (radius={radius}):")
print(f"  Area: {circle_area(radius):.2f}")
print(f"  Perimeter: {circle_perimeter(radius):.2f}")
print(f"\nSquare (side={side}):")
print(f"  Area: {square_area(side)}")
print(f"  Perimeter: {square_perimeter(side)}")
