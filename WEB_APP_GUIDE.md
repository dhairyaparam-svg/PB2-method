# PB2 Web Application - Getting Started Guide

## Quick Start (2 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Server

**Windows:**
```bash
run_web.bat
```

**macOS/Linux:**
```bash
chmod +x run_web.sh
./run_web.sh
```

### 3. Open in Browser
Navigate to: **http://localhost:5000**

---

## Web Interface Overview

### 🎨 Tab 1: Draw Shape
**Draw arbitrary closed shapes by clicking on the canvas**

- Click to add vertices
- Shift+Click to remove last vertex
- Click "Use This Shape" to proceed
- View vertex coordinates in real-time

**Tips:**
- Start in a corner
- Click roughly along the perimeter you want
- You need at least 3 points
- The shape is normalized automatically

### 📐 Tab 2: Regular Polygon
**Generate perfect regular polygons instantly**

- Select number of sides (3-100)
- Set side length
- Click buttons for quick shapes (Triangle, Square, Hexagon, etc.)
- Instant generation and analysis-ready

**Presets:**
- Triangle (3 sides)
- Square (4 sides)
- Pentagon (5 sides)
- Hexagon (6 sides)
- Octagon (8 sides)
- Decagon (10 sides)
- Dodecagon (12 sides)
- 16-gon (16 sides)

### 📁 Tab 3: Import DXF
**Load CAD designs from DXF files**

- Drag and drop DXF file or click to browse
- Supports POLYLINE and LWPOLYLINE
- Automatic normalization
- Ready for analysis

**DXF Requirements:**
- Must be a closed polyline
- File must be DXF format
- No size limit (auto-scaled)

### 📊 Tab 4: Results & Analysis
**Run full PB2 analysis with customizable parameters**

#### Material Properties
- **Flexural Rigidity (D):** Physical rigidity (Pa)
- **Poisson's Ratio (ν):** Material elasticity (0-0.49)
- **Density (ρ):** Mass per volume (kg/m³)
- **Thickness:** Plate thickness (m)

#### Material Presets
Click any preset to auto-fill material parameters:

| Material | D | ν | ρ |
|----------|---|---|---|
| 🏭 Steel | 210 GPa | 0.30 | 7850 kg/m³ |
| ✈️ Aluminum | 70 GPa | 0.33 | 2700 kg/m³ |
| 🎨 Composite | 30 GPa | 0.25 | 1600 kg/m³ |
| 🪟 GFRP | 10 GPa | 0.28 | 1850 kg/m³ |

#### Run Analysis
- Click "Run Analysis" button
- Results display in real-time
- View frequencies in rad/s and Hz
- See visualization and charts

---

## Understanding Results

### Natural Frequencies
- **Units:** rad/s (radians per second)
- **Conversion:** freq_Hz = freq_rad_s ÷ (2π)
- **Mode 1:** Lowest frequency (fundamental)
- **Mode 2+:** Higher modes (increasing complexity)

### Example Output:
```
Mode 1: 15.234567 rad/s → 2.42 Hz
Mode 2: 42.123456 rad/s → 6.71 Hz
Mode 3: 78.234567 rad/s → 12.45 Hz
```

### Visualizations:
1. **Shape Plot:** Your geometry (blue outline, filled area)
2. **Frequency Response:** Bar chart of all computed modes

---

## Common Workflows

### Workflow 1: Quick Hexagon Analysis
1. Click Tab: "Regular Polygon"
2. Select preset: "Hexagon"
3. Click Tab: "Results & Analysis"
4. Click "Run Analysis"
5. View results instantly

### Workflow 2: Import CAD Design
1. Click Tab: "Import DXF"
2. Drag your .dxf file onto the canvas
3. Click Tab: "Results & Analysis"
4. Select material from presets
5. Click "Run Analysis"
6. Analyze results

### Workflow 3: Custom Shape Analysis
1. Click Tab: "Draw Shape"
2. Click canvas to draw your geometry
3. Click "Use This Shape"
4. Adjust material properties
5. Click "Run Analysis"
6. Review visualizations

### Workflow 4: Material Comparison
1. Load a single shape (any method)
2. Switch material presets one by one
3. Run analysis for each material
4. Compare frequencies
5. Note differences in results

---

## Tips & Tricks

### Drawing Better Shapes
- Use steady, deliberate clicks
- Start from one corner and work around the perimeter
- Avoid very sharp angles (minimum ~15°)
- Keep the shape roughly convex when possible
- Use Shift+Click to correct mistakes

### File Upload Tips
- Ensure DXF has a single closed polyline
- Export from CAD without dissociation
- File size should be < 16MB
- Try simplifying complex geometries

### Material Properties
- Use presets when available
- For custom materials, reference material datasheets
- Ensure consistent unit systems
- Check Poisson's ratio is between 0 and 0.49

### Performance
- Simpler shapes (fewer vertices) = faster computation
- Regular polygons compute fastest
- Complex DXF files may take 5-10 seconds
- Web interface remains responsive during analysis

---

## Troubleshooting

### Issue: "Need at least 3 vertices"
**Solution:** Draw at least 3 points on the canvas

### Issue: "Could not compute frequencies"
**Solution:**
- Check material properties are positive
- Verify Poisson's ratio is < 0.5
- Try with a simpler shape
- Refresh the page

### Issue: DXF file not loading
**Solution:**
- Verify it's a valid DXF file
- Ensure it contains a closed polyline
- Try exporting from CAD differently
- Check file is under 16MB

### Issue: Server won't start
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Try different port
python app.py --port 5001

# Check Python version
python --version  # Must be 3.8+
```

### Issue: Slow computation
**Solution:**
- Simplify the geometry (fewer vertices)
- Use regular polygons instead of DXF
- Reduce plate thickness for faster processing
- Close other applications

---

## Keyboard Shortcuts (Drawing Mode)

| Key | Action |
|-----|--------|
| **Click** | Add vertex |
| **Shift+Click** | Undo last vertex |
| **Right-Click** | (Menu disabled) |
| **Clear Button** | Reset entire shape |

---

## API Reference for Developers

### Analyze Shape Endpoint
```
POST /api/analyze
Content-Type: application/json

{
    "vertices": [[x1, y1], [x2, y2], ...],
    "D": 1.0,
    "nu": 0.3,
    "rho": 1.0,
    "thickness": 1.0,
    "n_basis": 9
}

Response:
{
    "success": true,
    "frequencies": [15.23, 42.12, 78.23, ...],
    "shape_plot": "data:image/png;base64,...",
    "freq_plot": "data:image/png;base64,...",
    "n_vertices": 6,
    "timestamp": "2026-04-01T12:00:00"
}
```

### Generate Polygon Endpoint
```
POST /api/generate-polygon
{
    "sides": 6,
    "side_length": 1.0
}

Response:
{
    "success": true,
    "vertices": [[x1, y1], [x2, y2], ...],
    "description": "Regular 6-gon with side length 1.0"
}
```

### Load DXF Endpoint
```
POST /api/load-dxf
Content-Type: multipart/form-data

file: <binary DXF file>

Response:
{
    "success": true,
    "vertices": [[x1, y1], [x2, y2], ...],
    "description": "DXF file with 10 vertices",
    "n_vertices": 10
}
```

---

## Browser Compatibility

| Browser | v1.0 Support |
|---------|--------------|
| Chrome | ✅ Yes (recommended) |
| Firefox | ✅ Yes |
| Safari | ✅ Yes |
| Edge | ✅ Yes |
| IE 11 | ❌ No |

**Recommended:** Google Chrome or Firefox (latest version)

---

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| Python | 3.8+ |
| RAM | 512 MB |
| Storage | 100 MB |
| Network | localhost only |

---

## File Structure

```
PB2 method/
├── app.py                          # Flask web server
├── pb2_natural_frequency.py        # PB2 calculation engine
├── requirements.txt                # Python dependencies
├── run_web.bat                     # Windows launcher
├── run_web.sh                      # macOS/Linux launcher
├── templates/
│   └── index.html                  # Web interface
├── uploads/                        # Temporary DXF uploads
└── README.md                       # This file
```

---

## Performance Benchmarks

| Shape | Vertices | Time | Modes |
|-------|----------|------|-------|
| Triangle | 3 | ~0.5s | 9 |
| Square | 4 | ~0.7s | 9 |
| Hexagon | 6 | ~1.2s | 9 |
| Octagon | 8 | ~1.8s | 9 |
| Custom | 20 | ~3-5s | 9 |

*Approximate timings on modern hardware*

---

## Keyboard Navigation

| Key | Action |
|-----|--------|
| **Tab** | Navigate between elements |
| **Enter** | Submit form/click button |
| **Space** | Toggle button |
| **Escape** | Close modal (if any) |

---

## Data Privacy

- ✅ All computations run locally
- ✅ No data sent to external servers
- ✅ No cookies or tracking
- ✅ Temporary files auto-deleted
- ✅ Complete offline capability

---

## Advanced Usage

### Custom Shape via Python
```python
import requests
import json

data = {
    "vertices": [[0, 0], [1, 0], [0.5, 0.866]],
    "D": 1.0,
    "nu": 0.3,
    "rho": 1.0,
    "thickness": 1.0
}

response = requests.post('http://localhost:5000/api/analyze', json=data)
results = response.json()
print(f"Frequencies: {results['frequencies']}")
```

### Bulk Analysis
```bash
# Create a Python script to batch-process multiple DXF files
for dxf_file in *.dxf; do
    # Load DXF and run analysis
    # Save results to CSV
done
```

---

## Support & Issues

**For problems:**
1. Check the Troubleshooting section
2. Verify Python version: `python --version`
3. Reinstall dependencies: `pip install --upgrade -r requirements.txt`
4. Try with a simple shape (Triangle, Square, Hexagon)
5. Clear browser cache and restart server

---

## Version Info

**Current Version:** 1.0  
**Release Date:** April 1, 2026  
**Python Required:** 3.8+  
**Framework:** Flask 2.0+  

---

## License & Attribution

Based on MATLAB implementation by Dhairya D. Dosi (Aug 2023)  
Python web adaptation: 2026

---

**Ready to analyze? Open http://localhost:5000 in your browser! 🚀**
