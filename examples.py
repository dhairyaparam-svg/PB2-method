"""
Example Scripts for PB2 Natural Frequency Analysis
Demonstrates usage without interactive menu
"""

from pb2_natural_frequency import (PB2NaturalFrequency, ShapeLoader, 
                                   VisualizationTools)
import matplotlib.pyplot as plt
import numpy as np


def example_1_hexagon():
    """Example 1: Regular Hexagon"""
    print("\n" + "="*60)
    print("Example 1: Regular Hexagon Analysis")
    print("="*60)
    
    # Create hexagon
    loader = ShapeLoader()
    vertices = loader.create_regular_polygon(n_sides=6, side_length=1.0)
    
    print(f"Created regular hexagon with side length: 1.0")
    print(f"Number of vertices: {len(vertices)}")
    
    # Analyze with default material properties
    analyzer = PB2NaturalFrequency(
        vertices=vertices,
        D=1.0,
        nu=0.3,
        rho=1.0,
        thickness=1.0,
        verbose=True
    )
    
    frequencies = analyzer.calculate_natural_frequencies()
    
    # Display results
    print("\nNatural Frequencies (rad/s):")
    for i, freq in enumerate(frequencies[:6]):
        print(f"  Mode {i+1}: {freq:.6f}")
    
    # Plot
    VisualizationTools.plot_shape(vertices, "Hexagon Shape")
    VisualizationTools.plot_frequencies(frequencies, "Hexagon Natural Frequencies")
    plt.show()


def example_2_pentagon():
    """Example 2: Regular Pentagon"""
    print("\n" + "="*60)
    print("Example 2: Regular Pentagon Analysis")
    print("="*60)
    
    loader = ShapeLoader()
    vertices = loader.create_regular_polygon(n_sides=5, side_length=1.5)
    
    print(f"Created regular pentagon with side length: 1.5")
    
    analyzer = PB2NaturalFrequency(vertices, verbose=True)
    frequencies = analyzer.calculate_natural_frequencies()
    
    print("\nNatural Frequencies (rad/s):")
    for i, freq in enumerate(frequencies[:6]):
        print(f"  Mode {i+1}: {freq:.6f}")
    
    VisualizationTools.plot_shape(vertices, "Pentagon Shape")
    VisualizationTools.plot_frequencies(frequencies, "Pentagon Natural Frequencies")
    plt.show()


def example_3_octagon():
    """Example 3: Regular Octagon"""
    print("\n" + "="*60)
    print("Example 3: Regular Octagon Analysis")
    print("="*60)
    
    loader = ShapeLoader()
    vertices = loader.create_regular_polygon(n_sides=8, side_length=1.0)
    
    print(f"Created regular octagon with side length: 1.0")
    
    analyzer = PB2NaturalFrequency(vertices, verbose=True)
    frequencies = analyzer.calculate_natural_frequencies()
    
    print("\nNatural Frequencies (rad/s):")
    for i, freq in enumerate(frequencies[:6]):
        print(f"  Mode {i+1}: {freq:.6f}")
    
    VisualizationTools.plot_shape(vertices, "Octagon Shape")
    VisualizationTools.plot_frequencies(frequencies, "Octagon Natural Frequencies")
    plt.show()


def example_4_triangle():
    """Example 4: Equilateral Triangle"""
    print("\n" + "="*60)
    print("Example 4: Equilateral Triangle Analysis")
    print("="*60)
    
    loader = ShapeLoader()
    vertices = loader.create_regular_polygon(n_sides=3, side_length=1.0)
    
    print(f"Created equilateral triangle with side length: 1.0")
    
    analyzer = PB2NaturalFrequency(vertices, verbose=True)
    frequencies = analyzer.calculate_natural_frequencies()
    
    print("\nNatural Frequencies (rad/s):")
    for i, freq in enumerate(frequencies[:6]):
        print(f"  Mode {i+1}: {freq:.6f}")
    
    VisualizationTools.plot_shape(vertices, "Triangle Shape")
    VisualizationTools.plot_frequencies(frequencies, "Triangle Natural Frequencies")
    plt.show()


def example_5_square():
    """Example 5: Square"""
    print("\n" + "="*60)
    print("Example 5: Square Analysis")
    print("="*60)
    
    loader = ShapeLoader()
    vertices = loader.create_regular_polygon(n_sides=4, side_length=1.0)
    
    print(f"Created square with side length: 1.0")
    
    analyzer = PB2NaturalFrequency(vertices, verbose=True)
    frequencies = analyzer.calculate_natural_frequency()
    
    print("\nNatural Frequencies (rad/s):")
    for i, freq in enumerate(frequencies[:6]):
        print(f"  Mode {i+1}: {freq:.6f}")
    
    VisualizationTools.plot_shape(vertices, "Square Shape")
    VisualizationTools.plot_frequencies(frequencies, "Square Natural Frequencies")
    plt.show()


def example_6_custom_polygon():
    """Example 6: Custom Polygon (User-defined vertices)"""
    print("\n" + "="*60)
    print("Example 6: Custom Polygon Analysis")
    print("="*60)
    
    # Define a custom irregular polygon (vertices as x,y coordinates)
    vertices = np.array([
        [0.0,  1.0],   # Top
        [0.95, 0.31],  # Right-upper
        [0.59, -0.81], # Right-lower
        [-0.59, -0.81],# Left-lower
        [-0.95, 0.31], # Left-upper
    ])
    
    print("Created custom polygon with vertices:")
    for i, v in enumerate(vertices):
        print(f"  Vertex {i+1}: ({v[0]:.2f}, {v[1]:.2f})")
    
    analyzer = PB2NaturalFrequency(vertices, verbose=True)
    frequencies = analyzer.calculate_natural_frequencies()
    
    print("\nNatural Frequencies (rad/s):")
    for i, freq in enumerate(frequencies[:6]):
        print(f"  Mode {i+1}: {freq:.6f}")
    
    VisualizationTools.plot_shape(vertices, "Custom Polygon Shape")
    VisualizationTools.plot_frequencies(frequencies, "Custom Polygon Natural Frequencies")
    plt.show()


def example_7_material_comparison():
    """Example 7: Material Comparison - Hexagon with different materials"""
    print("\n" + "="*60)
    print("Example 7: Material Comparison")
    print("="*60)
    
    loader = ShapeLoader()
    vertices = loader.create_regular_polygon(n_sides=6, side_length=1.0)
    
    materials = {
        'Steel': {'D': 210e9, 'nu': 0.3, 'rho': 7850},
        'Aluminum': {'D': 70e9, 'nu': 0.33, 'rho': 2700},
        'Composite': {'D': 30e9, 'nu': 0.25, 'rho': 1600},
    }
    
    results = {}
    
    for material_name, props in materials.items():
        print(f"\nAnalyzing {material_name}...")
        analyzer = PB2NaturalFrequency(
            vertices,
            D=props['D'],
            nu=props['nu'],
            rho=props['rho'],
            verbose=False
        )
        frequencies = analyzer.calculate_natural_frequencies()
        results[material_name] = frequencies
    
    # Compare results
    print("\n" + "="*60)
    print("Comparison - First 3 Modes:")
    print("="*60)
    print(f"{'Material':<15} {'Mode 1':<15} {'Mode 2':<15} {'Mode 3':<15}")
    print("-" * 60)
    for material_name, frequencies in results.items():
        mode1 = frequencies[0] if len(frequencies) > 0 else 0
        mode2 = frequencies[1] if len(frequencies) > 1 else 0
        mode3 = frequencies[2] if len(frequencies) > 2 else 0
        print(f"{material_name:<15} {mode1:<15.4e} {mode2:<15.4e} {mode3:<15.4e}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("  PB2 Natural Frequency Analysis - Example Suite")
    print("="*60)
    print("\nSelect an example to run:")
    print("  1. Regular Hexagon")
    print("  2. Regular Pentagon")
    print("  3. Regular Octagon")
    print("  4. Equilateral Triangle")
    print("  5. Square")
    print("  6. Custom Polygon")
    print("  7. Material Comparison")
    print("  8. Run All Examples")
    print("  9. Exit")
    
    choice = input("\nEnter choice (1-9): ").strip()
    
    examples = {
        '1': example_1_hexagon,
        '2': example_2_pentagon,
        '3': example_3_octagon,
        '4': example_4_triangle,
        '5': example_5_square,
        '6': example_6_custom_polygon,
        '7': example_7_material_comparison,
    }
    
    if choice == '8':
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"Error: {e}")
    elif choice != '9':
        print("Invalid choice")


if __name__ == "__main__":
    main()
