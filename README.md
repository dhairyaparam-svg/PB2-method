# PB2 Natural Frequency Analysis for Arbitrary Shapes

Python implementation of the Generalized Rayleigh-Ritz Method (PB2) for calculating natural frequencies of plates with arbitrary closed geometries.

## Features

✅ **Interactive Shape Drawing** - Click to draw arbitrary closed shapes  
✅ **Regular Polygon Support** - Generate regular polygons (hexagon, pentagon, etc.)  
✅ **DXF Import** - Load closed shapes from CAD DXF files  
✅ **Rayleigh-Ritz Method** - PB2 method for natural frequency calculation  
✅ **Visualization** - Plot shapes and natural frequency results  
✅ **Material Parameters** - Customize flexural rigidity, Poisson's ratio, density, thickness  

## Installation

### 1. Install Python (3.8 or higher)

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install numpy scipy matplotlib sympy ezdxf
```

## Usage

### Option 1: Web Application (Recommended)

The modern web-based interface is the easiest way to use PB2 analysis.

**Windows:**
```bash
double-click run_web.bat
```

**macOS/Linux:**
```bash
chmod +x run_web.sh
./run_web.sh
```

Then open your browser to: **http://localhost:5000**

**Features:**
- 🎨 Interactive canvas for drawing shapes
- 📐 Regular polygon generator with presets
- 📁 DXF file upload and import
- 📊 Real-time visualization
- ⚙️ Material property presets
- 📈 Beautiful charts and graphs

### Option 2: Command Line Interface

For users who prefer terminal-based analysis:

```bash
python pb2_natural_frequency.py
```

### Option 3: Python Scripts

Pre-built and custom example scripts:

```bash
python examples.py
```

---

## Mode 1: Interactive Shape Drawing

**Instructions:**
- Click on the canvas to add vertices
- Press **Enter** or **Right-click** to finish drawing
- Close the figure window to proceed

**Example:** Click to create a hexagon, triangle, or any custom shape.

---

## Mode 2: Regular Polygon

**Inputs:**
- Number of sides (e.g., 6 for hexagon, 5 for pentagon, 8 for octagon)
- Side length (default: 1.0)

**Example:** Create a regular hexagon:
```
Number of sides: 6
Side length: 1.0
```

---

## Mode 3: DXF File Import

**Inputs:**
- Full path to DXF file

**Example:**
```
Enter DXF file path: C:\Users\YourName\shape.dxf
```

**Requirements for DXF:**
- Must contain a closed POLYLINE or LWPOLYLINE
- File must be readable by ezdxf library

---

## Material Properties

After selecting a shape, configure material parameters:

```
=== Material Properties ===
Flexural rigidity (D) [default: 1.0]: 1.0
Poisson's ratio (ν) [default: 0.3]: 0.3
Density (ρ) [default: 1.0]: 1.0
Plate thickness [default: 1.0]: 1.0
```

**Standard Values:**
| Material | D | ν | ρ |
|----------|---|---|---|
| Steel | 210 GPa | 0.3 | 7850 kg/m³ |
| Aluminum | 70 GPa | 0.33 | 2700 kg/m³ |
| Composite | 10-50 GPa | 0.2-0.3 | 1500-1700 |

---

## Output

### Results Display

The program outputs the first 5 natural frequencies:

```
=== Results ===
Natural Frequencies (rad/s):
  Mode 1: 15.234567 rad/s
  Mode 2: 42.123456 rad/s
  Mode 3: 78.234567 rad/s
  Mode 4: 124.567890 rad/s
  Mode 5: 189.234567 rad/s
```

### Visualizations

- **Shape Plot:** Display of the input geometry
- **Frequency Plot:** Bar chart of natural frequencies

---

## Python API Usage

### Use as a Module

```python
from pb2_natural_frequency import PB2NaturalFrequency, ShapeLoader, VisualizationTools
import numpy as np

# Load or create vertices (N x 2 array)
loader = ShapeLoader()
vertices = loader.create_regular_polygon(n_sides=6, side_length=1.0)

# Create analyzer
analyzer = PB2NaturalFrequency(
    vertices=vertices,
    D=1.0,                # Flexural rigidity
    nu=0.3,              # Poisson's ratio
    rho=1.0,             # Density
    thickness=1.0,       # Plate thickness
    n_basis=9,           # Number of basis functions
    verbose=True
)

# Calculate natural frequencies
frequencies = analyzer.calculate_natural_frequencies()

# Visualize
VisualizationTools.plot_shape(vertices, title="My Shape")
VisualizationTools.plot_frequencies(frequencies)

import matplotlib.pyplot as plt
plt.show()

# Display results
for i, freq in enumerate(frequencies[:5]):
    print(f"Mode {i+1}: {freq:.6f} rad/s")
```

---

## Example Scripts

### Example 1: Hexagon Analysis

```python
from pb2_natural_frequency import PB2NaturalFrequency, ShapeLoader

# Create regular hexagon
loader = ShapeLoader()
vertices = loader.create_regular_polygon(n_sides=6, side_length=2.0)

# Analyze
analyzer = PB2NaturalFrequency(vertices, D=1.0, nu=0.3, rho=1.0)
frequencies = analyzer.calculate_natural_frequencies()

print("Hexagon Natural Frequencies:")
for i, f in enumerate(frequencies[:5]):
    print(f"  Mode {i+1}: {f:.4f} rad/s")
```

### Example 2: Custom Shape from DXF

```python
from pb2_natural_frequency import ShapeLoader, PB2NaturalFrequency

loader = ShapeLoader()
vertices = loader.load_from_dxf("my_shape.dxf")

if vertices is not None:
    analyzer = PB2NaturalFrequency(vertices, nu=0.3)
    frequencies = analyzer.calculate_natural_frequencies()
```

---

## Method Details

### PB2 Method (Generalized Rayleigh-Ritz)

The method follows these steps:

1. **Boundary Constraint:** Create a polynomial that is zero on all edges:
   ```
   w_boundary = ∏(edge_equation²)
   ```

2. **Trial Function:** Displacement field:
   ```
   w = w_boundary × (A₀ + A₁x² + A₂y² + ... + A₈x⁴y⁴)
   ```

3. **Energy Formulation:**
   - Strain Energy: `U = (D/2)∫∫ κ² dA`
   - Kinetic Energy: `T = (0.5)ρd ∫∫ w² dA`
   
   Where: `κ² = (w_xx + w_yy)² - 2(1-ν)(w_xx·w_yy - w_xy²)`

4. **Eigenvalue Problem:**
   - Solve `[K]{A} = ω²[M]{A}`
   - Extract natural frequencies: `ωₙ = √(λₙ)`

---

## Troubleshooting

### Issue: "No polylines found in DXF file"
- **Solution:** Ensure your DXF contains a POLYLINE or LWPOLYLINE entity
- Export from CAD as DXF format

### Issue: "Need at least 3 vertices"
- **Solution:** Draw at least 3 points to define a closed shape

### Issue: "Error solving eigenvalue problem"
- **Solution:** 
  - Check that all vertices are valid numbers
  - Try with simpler geometry first
  - Ensure material parameters are positive

### Issue: Low computation speed
- **Solution:** 
  - For complex shapes, reduce the number of basis functions
  - Simplify the DXF geometry (fewer vertices)

---

## Limitations & Future Improvements

### Current Limitations
- Numerical integration accuracy depends on polygon complexity
- Maximum ~100 vertices recommended for real-time performance
- Assumes uniform plate thickness
- No damping included
- 2D analysis only

### Planned Improvements
- [ ] 3D shell element support
- [ ] Damping analysis
- [ ] Mode shape visualization
- [ ] Frequency response functions (FRF)
- [ ] Export results to CSV/Excel
- [ ] Comparison with FEM solutions
- [ ] GPU acceleration for large problems

---

## References

1. **Original MATLAB Code:** PB2 Method for Regular Polygons
   - Author: Dhairya D. Dosi, Aug 2023
   - Method: Generalized Rayleigh-Ritz

2. **Rayleigh-Ritz Method:**
   - Rao, S.S. (2017). "Vibration of Continuous Systems"
   - Leissa, A.W. (1973). "Vibration of Plates"

3. **DXF Import:**
   - ezdxf: https://pypi.org/project/ezdxf/

---

## License

This code is based on the MATLAB implementation by Dhairya D. Dosi and has been adapted for Python.

---

## Contact & Support

For issues or questions:
- Review the troubleshooting section
- Check input geometry validity
- Verify material parameters

---

## Version History

- **v1.0** (2026-04-01): Initial Python release
  - Interactive shape drawing
  - DXF import capability
  - PB2 method implementation
  - Natural frequency calculation
