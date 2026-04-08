"""
PB2 Natural Frequency Analysis - Web Application
Flask backend for browser-based PB2 analysis
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import json
import io
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pb2_natural_frequency import PB2NaturalFrequency, ShapeLoader
import traceback

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    API endpoint for natural frequency analysis
    
    Expected JSON:
    {
        "vertices": [[x1, y1], [x2, y2], ...],
        "D": float,
        "nu": float,
        "rho": float,
        "thickness": float,
        "n_basis": int
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'vertices' not in data:
            return jsonify({'error': 'Missing vertices'}), 400
        
        vertices = np.array(data['vertices'])
        
        if len(vertices) < 3:
            return jsonify({'error': 'Need at least 3 vertices'}), 400
        
        # Get material properties
        D = float(data.get('D', 1.0))
        nu = float(data.get('nu', 0.3))
        rho = float(data.get('rho', 1.0))
        thickness = float(data.get('thickness', 1.0))
        n_basis = int(data.get('n_basis', 9))
        boundary_condition = data.get('boundary_condition', 'simply_supported')
        if boundary_condition not in ('simply_supported', 'fixed'):
            return jsonify({'error': "boundary_condition must be 'simply_supported' or 'fixed'"}), 400
        
        # Validate material properties
        if D <= 0 or rho <= 0 or thickness <= 0:
            return jsonify({'error': 'Material properties must be positive'}), 400
        
        if nu < 0 or nu >= 0.5:
            return jsonify({'error': 'Poisson\'s ratio must be between 0 and 0.5'}), 400
        
        # Run analysis
        analyzer = PB2NaturalFrequency(
            vertices=vertices,
            D=D,
            nu=nu,
            rho=rho,
            thickness=thickness,
            n_basis=n_basis,
            verbose=False
        )
        
        frequencies = analyzer.calculate_natural_frequencies()
        
        # Convert to list and ensure valid numbers
        frequencies = [float(f) for f in frequencies if np.isfinite(f)]
        frequencies.sort()
        
        if len(frequencies) == 0:
            return jsonify({'error': 'Could not compute frequencies'}), 500
        
        # Generate plots
        shape_plot = generate_shape_plot(vertices)
        freq_plot = generate_frequency_plot(frequencies)
        
        return jsonify({
            'success': True,
            'frequencies': frequencies,
            'shape_plot': shape_plot,
            'freq_plot': freq_plot,
            'n_vertices': len(vertices),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in analysis: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-polygon', methods=['POST'])
def generate_polygon():
    """Generate regular polygon"""
    try:
        data = request.get_json()
        n_sides = int(data.get('sides', 6))
        side_length = float(data.get('side_length', 1.0))
        
        if n_sides < 3 or n_sides > 100:
            return jsonify({'error': 'Number of sides must be between 3 and 100'}), 400
        
        loader = ShapeLoader()
        vertices = loader.create_regular_polygon(n_sides, side_length)
        
        return jsonify({
            'success': True,
            'vertices': vertices.tolist(),
            'description': f'Regular {n_sides}-gon with side length {side_length}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/load-dxf', methods=['POST'])
def load_dxf():
    """Load DXF file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.dxf'):
            return jsonify({'error': 'Only DXF files are supported'}), 400
        
        # Save temporary file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Load from DXF
        loader = ShapeLoader()
        vertices = loader.load_from_dxf(filepath)
        
        # Clean up
        os.remove(filepath)
        
        if vertices is None or len(vertices) == 0:
            return jsonify({'error': 'Could not load DXF or file is empty'}), 400
        
        return jsonify({
            'success': True,
            'vertices': vertices.tolist(),
            'description': f'DXF file with {len(vertices)} vertices',
            'n_vertices': len(vertices)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate-vertices', methods=['POST'])
def validate_vertices():
    """Validate polygon vertices"""
    try:
        data = request.get_json()
        vertices = np.array(data.get('vertices', []))
        
        if len(vertices) < 3:
            return jsonify({
                'valid': False,
                'message': 'Need at least 3 vertices'
            })
        
        # Check for duplicates
        unique_vertices = np.unique(vertices, axis=0)
        if len(unique_vertices) < len(vertices):
            return jsonify({
                'valid': False,
                'message': 'Duplicate vertices detected'
            })
        
        # Calculate area (shoelace formula)
        area = 0.5 * abs(sum(vertices[i][0] * vertices[(i+1) % len(vertices)][1] -
                            vertices[(i+1) % len(vertices)][0] * vertices[i][1]
                            for i in range(len(vertices))))
        
        return jsonify({
            'valid': True,
            'message': f'Valid polygon with {len(vertices)} vertices',
            'n_vertices': len(vertices),
            'area': float(area),
            'perimeter': float(sum(np.linalg.norm(vertices[(i+1) % len(vertices)] - vertices[i])
                                    for i in range(len(vertices))))
        })
    
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': str(e)
        }), 500


def generate_shape_plot(vertices):
    """Generate shape plot as base64 image"""
    try:
        fig, ax = plt.subplots(figsize=(8, 8))
        
        vertices_plot = np.vstack([vertices, vertices[0]])
        
        ax.plot(vertices_plot[:, 0], vertices_plot[:, 1], 'b-o', 
                linewidth=2, markersize=6)
        ax.fill(vertices_plot[:, 0], vertices_plot[:, 1], alpha=0.3)
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Input Shape')
        
        # Convert to base64
        img_io = io.BytesIO()
        fig.savefig(img_io, format='png', dpi=80, bbox_inches='tight')
        img_io.seek(0)
        
        import base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{img_base64}"
    
    except Exception as e:
        print(f"Error generating shape plot: {e}")
        return None


def generate_frequency_plot(frequencies):
    """Generate frequency bar chart as base64 image"""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        modes = np.arange(1, len(frequencies) + 1)
        bars = ax.bar(modes, frequencies, width=0.6, color='steelblue', 
                     alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('Mode Number')
        ax.set_ylabel('Natural Frequency (rad/s)')
        ax.set_title('Natural Frequencies - PB2 Method')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add values on bars
        for i, freq in enumerate(frequencies):
            ax.text(i+1, freq, f'{freq:.2f}', ha='center', va='bottom', fontsize=8)
        
        # Convert to base64
        img_io = io.BytesIO()
        fig.savefig(img_io, format='png', dpi=80, bbox_inches='tight')
        img_io.seek(0)
        
        import base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{img_base64}"
    
    except Exception as e:
        print(f"Error generating frequency plot: {e}")
        return None


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  PB2 Natural Frequency Analysis - Web Application")
    print("="*60)
    print("\nWeb server starting...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
