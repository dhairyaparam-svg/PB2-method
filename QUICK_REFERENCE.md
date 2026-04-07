# PB2 Natural Frequency Analysis - Quick Reference Guide

## Installation (5 minutes)

### Windows
1. Open Command Prompt in the folder
2. Double-click `setup.bat`
3. Wait for installation to complete

### macOS/Linux
1. Open Terminal
2. Run: `chmod +x setup.sh && ./setup.sh`
3. Wait for installation

---

## Quick Start

### Option 1: Interactive Mode
```bash
python pb2_natural_frequency.py
```
- Draw shapes, select options interactively
- Get instant visualization

### Option 2: Run Examples
```bash
python examples.py
```
- Pre-built shapes (hexagon, pentagon, etc.)
- Material comparisons
- No user input needed

### Option 3: Use as Python Module
```python
from pb2_natural_frequency import PB2NaturalFrequency, ShapeLoader

# Create shape
loader = ShapeLoader()
vertices = loader.create_regular_polygon(6, 1.0)

# Analyze
analyzer = PB2NaturalFrequency(vertices)
frequencies = analyzer.calculate_natural_frequencies()

# Display
for i, f in enumerate(frequencies[:5]):
    print(f"Mode {i+1}: {f:.4f} rad/s")
```

---

## Three Ways to Input Shapes

### 1. Draw Interactively
- Menu option: **1**
- Click to add vertices
- Press Enter to finish
- Works for any shape

### 2. Regular Polygons
- Menu option: **2**
- Enter number of sides (3-12+)
- Enter side length
- Instant regular shapes

### 3. Import from DXF
- Menu option: **3**
- Provide DXF file path
- CAD-designed geometries
- Complex shapes supported

---

## Material Properties Presets

### Steel (Structural)
```
D = 210 GPa
ν = 0.30
ρ = 7850 kg/m³
```

### Aluminum (Aerospace)
```
D = 70 GPa
ν = 0.33
ρ = 2700 kg/m³
```

### Composite (Carbon Fiber)
```
D = 30 GPa
ν = 0.25
ρ = 1600 kg/m³
```

### Glass Fiber Reinforced Plastic
```
D = 10 GPa
ν = 0.28
ρ = 1850 kg/m³
```

---

## Output Interpretation

### Natural Frequencies
- **Units:** rad/s (radians per second)
- **Conversion to Hz:** freq_Hz = freq_rad_s / (2π)
- **Mode 1:** Lowest frequency, simplest shape
- **Mode 2+:** Higher frequencies, more complex vibration patterns

### Example Output:
```
Mode 1: 15.234567 rad/s → 2.42 Hz
Mode 2: 42.123456 rad/s → 6.71 Hz
Mode 3: 78.234567 rad/s → 12.45 Hz
```

---

## Common Tasks

### Compare Different Materials
```python
materials = {
    'Steel': {'D': 210e9, 'rho': 7850},
    'Aluminum': {'D': 70e9, 'rho': 2700},
}

for name, props in materials.items():
    analyzer = PB2NaturalFrequency(vertices, **props)
    freq = analyzer.calculate_natural_frequencies()
    print(f"{name}: {freq[0]:.2f} rad/s")
```

### Compare Different Shapes
```python
shapes = {
    'Triangle': 3,
    'Square': 4,
    'Pentagon': 5,
    'Hexagon': 6,
}

loader = ShapeLoader()
for name, sides in shapes.items():
    v = loader.create_regular_polygon(sides)
    analyzer = PB2NaturalFrequency(v)
    freq = analyzer.calculate_natural_frequencies()
    print(f"{name}: {freq[0]:.2f} rad/s")
```

### Export Results
```python
import numpy as np

frequencies = analyzer.calculate_natural_frequencies()
np.savetxt('frequencies.csv', frequencies, delimiter=',', 
           header='Mode,Frequency(rad/s)', 
           fmt='%d,%f')
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'numpy'"
**Solution:** Run setup script again
```bash
# Windows
setup.bat

# macOS/Linux
./setup.sh
```

### Error: "No polylines found in DXF file"
**Solution:** 
- Verify DXF contains closed polyline
- Export from CAD without dissociation
- Try simpler DXF file first

### Error: "Need at least 3 vertices"
**Solution:**
- Click at least 3 points when drawing
- Check DXF file validity

### Slow computation
**Solution:**
- Simplify geometry (fewer vertices)
- Use regular polygons (faster)
- Reduce basis functions (not recommended)

---

## Keyboard Shortcuts (Drawing Mode)

| Key | Action |
|-----|--------|
| Left Click | Add vertex |
| Right Click | Finish drawing |
| Enter | Finish drawing |
| Scroll | Zoom (may vary by system) |

---

## File Descriptions

| File | Purpose |
|------|---------|
| `pb2_natural_frequency.py` | Main program |
| `examples.py` | Pre-built examples |
| `README.md` | Full documentation |
| `requirements.txt` | Python dependencies |
| `setup.bat` | Windows installer |
| `setup.sh` | macOS/Linux installer |

---

## Performance Benchmark

| Shape | Vertices | Computation Time |
|-------|----------|------------------|
| Triangle | 3 | ~0.5s |
| Square | 4 | ~0.7s |
| Hexagon | 6 | ~1.2s |
| Octagon | 8 | ~1.8s |
| Complex | 20+ | ~5-10s |

---

## Tips & Best Practices

✓ **Do:**
- Start with simple shapes (triangle, square, hexagon)
- Verify DXF files are closed polygons
- Use consistent unit systems
- Test with examples first

✗ **Don't:**
- Use overlapping vertices
- Leave shapes open (unclosed)
- Mix unit systems (mm vs inches)
- Use extremely complex shapes (>100 vertices initially)

---

## Physics Background

### Rayleigh-Ritz Method
- Energy-based approach
- Assumes trial displacement field
- Minimizes total energy functional
- Converges to exact solution

### PB2 Boundary Constraint
- Ensures zero displacement on edges
- Polynomial form: product of edge equations squared
- Allows arbitrary geometries
- Computationally efficient

### Natural Frequency
- Frequency at which structure oscillates freely
- Depends on: geometry, material, boundary conditions
- Important for: vibration analysis, modal analysis, resonance prevention

---

## Next Steps

1. **Learn the Basics:**
   - Run examples.py
   - Try different regular polygons
   - Observe frequency trends

2. **Explore Custom Shapes:**
   - Use interactive drawing
   - Import DXF files
   - Analyze real geometries

3. **Compare Materials:**
   - Vary D, ν, ρ
   - See how parameters affect frequencies
   - Build intuition

4. **Advanced Applications:**
   - Design optimization
   - Resonance avoidance
   - Vibration isolation
   - Modal analysis

---

## References & Resources

### Theory
- Rao, S.S. (2017) - "Vibration of Continuous Systems"
- Leissa, A.W. (1973) - "Vibration of Plates"

### Software
- SymPy: https://www.sympy.org
- SciPy: https://www.scipy.org
- NumPy: https://numpy.org
- Matplotlib: https://matplotlib.org

### CAD Tools for DXF Export
- LibreCAD (Free)
- Inventor (Commercial)
- AutoCAD (Commercial)
- SolidWorks (Commercial)

---

## Version Info

**Software:** PB2 Natural Frequency Analysis v1.0  
**Release Date:** April 1, 2026  
**Python Required:** 3.8+  
**Original MATLAB Author:** Dhairya D. Dosi (Aug 2023)  
**Python Port:** 2026

---

**Questions?** See README.md for comprehensive documentation.
