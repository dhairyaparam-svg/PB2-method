# PB2 Natural Frequency Analysis Suite

Welcome! This package provides multiple ways to analyze natural frequencies of plate geometries using the PB2 method.

## 🚀 Quick Start (Choose One)

### 1️⃣ **WEB APPLICATION** (Recommended - Most User-Friendly)

Open a terminal/command prompt in this folder and run:

**Windows:**
```bash
run_web.bat
```

**macOS/Linux:**
```bash
./run_web.sh
```

Then open your browser to: **http://localhost:5000**

✨ Features:
- 🎨 Interactive canvas drawing
- 📐 Instant polygon generation
- 📁 Drag-and-drop DXF import
- 📊 Live visualization
- ⚙️ Material presets

---

### 2️⃣ **COMMAND LINE** (Classic Interface)

Run in terminal:
```bash
python pb2_natural_frequency.py
```

📋 Options:
1. Draw shape interactively
2. Generate regular polygon
3. Import from DXF file
4. Exit

---

### 3️⃣ **PYTHON SCRIPTS** (Batch Processing)

Run examples:
```bash
python examples.py
```

🔬 Pre-built examples:
- Regular shapes (triangle through 16-gon)
- Material comparison
- Custom polygons

---

## 📋 Installation

### Prerequisites
- **Python 3.8 or higher**
- **Internet connection** (first-time setup only)

### Setup

#### Option A: Automatic (Recommended)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

#### Option B: Manual
```bash
pip install -r requirements.txt
```

---

## 📚 Documentation

### Web Application
👉 **Read:** [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)
- Detailed web interface guide
- Workflow examples
- Troubleshooting

### Quick Reference
👉 **Read:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Common tasks
- Material presets
- Performance tips

### Full Documentation
👉 **Read:** [README.md](README.md)
- Complete feature list
- Physics background
- API reference

---

## 🎯 Choose Your Path

### 👤 I'm a Casual User
→ **Use the Web App** (`run_web.bat` or `run_web.sh`)
- No technical knowledge needed
- Visual interface
- Click and go

### 💻 I'm Comfortable with Code
→ **Use Command Line** (`python pb2_natural_frequency.py`)
- Text-based interface
- Step-by-step guidance
- Works on any system

### 🔬 I'm Doing Batch Analysis
→ **Use Python Scripts** (`python examples.py`)
- Automate analysis
- Process multiple files
- Integrate into workflows

### 👨‍💻 I'm a Developer
→ **Use the API** (See [README.md](README.md))
- HTTP REST endpoints
- Custom integration
- Programmatic access

---

## 🌟 Key Features

✅ **Three Shape Input Methods**
- Interactive drawing on canvas
- Regular polygon generation
- CAD DXF file import

✅ **Material Properties**
- Stock presets (Steel, Aluminum, Composite, GFRP)
- Custom material input
- Full parameter control

✅ **Analysis Engine**
- Generalized Rayleigh-Ritz method
- 9 basis functions
- Eigenvalue computation
- Robust numerical methods

✅ **Visualization**
- Shape plots
- Frequency response charts
- Real-time updates

✅ **Export Results**
- View in browser
- Save as images
- Display in terminal

---

## 🔧 File Structure

```
PB2 method/
├── 📄 README.md                 # Full documentation
├── 📄 QUICK_REFERENCE.md       # Quick tips & tricks
├── 📄 WEB_APP_GUIDE.md         # Web interface manual
├── 📄 START_HERE.md            # This file
│
├── 🌐 WEB APPLICATION
│   ├── app.py                  # Flask server
│   ├── run_web.bat             # Windows launcher
│   ├── run_web.sh              # macOS/Linux launcher
│   └── templates/
│       └── index.html          # Web interface
│
├── 💻 COMMAND LINE
│   ├── pb2_natural_frequency.py  # Main CLI program
│   ├── examples.py             # Example scripts
│   └── requirements.txt        # Dependencies
│
└── 🛠️ SETUP
    ├── setup.bat               # Windows setup
    └── setup.sh                # macOS/Linux setup
```

---

## ✅ Verify Installation

### Check Python
```bash
python --version
```
Must show Python 3.8+

### Check Dependencies
```bash
pip list | grep -E "numpy|scipy|flask"
```
Should show installed packages

### Test Web App
```bash
python app.py
```
Should show: "Running on http://127.0.0.1:5000"

---

## 🆘 Troubleshooting

### "Python not found"
→ Install Python from [python.org](https://www.python.org/)

### "ModuleNotFoundError"
→ Run: `pip install -r requirements.txt`

### "Port 5000 in use"
→ Edit `app.py` and change port number, or close other apps

### Web app won't load
→ Make sure Flask installed: `pip install flask flask-cors`

### Slow computation
→ Try simpler geometry (fewer vertices)

---

## 📞 Getting Help

1. **Review Documentation**
   - [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) - Web usage
   - [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick tips
   - [README.md](README.md) - Complete guide

2. **Check Troubleshooting**
   - Each guide has a troubleshooting section
   - Common issues with solutions

3. **Test with Examples**
   - Use `python examples.py`
   - Start with simple shapes (triangle, hexagon)

4. **Verify Setup**
   - Run: `pip install --upgrade -r requirements.txt`
   - Restart the application

---

## 📊 System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows, macOS, Linux |
| **Python** | 3.8 or higher |
| **RAM** | 512 MB minimum |
| **Storage** | 100 MB free space |
| **Browser** | Chrome, Firefox, Safari, Edge |
| **Network** | Localhost only (no internet needed) |

---

## 🎓 Physics Background

### What is Natural Frequency?
Frequency at which a structure oscillates freely after being disturbed. Important for:
- Vibration analysis
- Resonance avoidance
- Modal analysis
- Structural design

### What is PB2 Method?
Generalized Rayleigh-Ritz method that:
- Works for arbitrary geometries
- Uses boundary constraint polynomials
- Provides fast, accurate results
- Requires no mesh generation

### Rayleigh-Ritz Approach
Minimizes total energy functional:
- Strain energy (bending)
- Kinetic energy (mass)
- Eigenvalue problem gives frequencies

---

## 📈 Workflow Examples

### Example 1: Quick Hexagon Analysis
```
1. Run: run_web.bat
2. Browser opens to http://localhost:5000
3. Click "Regular Polygon" tab
4. Select Hexagon preset
5. Click "Results & Analysis" tab
6. Click "Run Analysis"
7. View frequency results
```
⏱️ Total time: ~30 seconds

### Example 2: Analyze CAD Design
```
1. Export design as DXF from CAD
2. Run: run_web.bat
3. Go to "Import DXF" tab
4. Drag your .dxf file
5. Select material from presets
6. Click "Run Analysis"
7. View results
```
⏱️ Total time: ~1 minute

### Example 3: Compare Materials
```
1. Load a shape (any method)
2. Switch material presets one-by-one
3. Run analysis for each
4. Note frequency differences
5. Export/save results
```
⏱️ Total time: ~2-3 minutes

---

## 🚀 Next Steps

1. **Choose your interface** (Web, CLI, or Scripts)
2. **Run the installer** (`setup.bat` or `setup.sh`)
3. **Launch the application**
4. **Read the relevant guide** (WEB_APP_GUIDE.md, QUICK_REFERENCE.md, or README.md)
5. **Start analyzing shapes!**

---

## 📝 Version Info

**Software:** PB2 Natural Frequency Analysis Suite  
**Version:** 1.0  
**Release Date:** April 1, 2026  
**Python:** 3.8+  
**Framework:** Flask 2.0+ (web), SymPy 1.9+ (analysis)  

**Based on:** MATLAB implementation by Dhairya D. Dosi (Aug 2023)  
**Python Port:** 2026

---

## 🎉 Ready to Begin?

### 🌐 Web App (Easiest)
```bash
run_web.bat          # Windows
./run_web.sh         # macOS/Linux
```

### 💻 Command Line
```bash
python pb2_natural_frequency.py
```

### 🔬 Examples
```bash
python examples.py
```

---

**Enjoy analyzing! Questions? Check the guides. 🚀**
