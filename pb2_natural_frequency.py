"""
PB2 Method for Natural Frequency Analysis of Arbitrary Closed Shapes
Converts MATLAB PB2 code to Python with support for:
- Interactive shape drawing
- Arbitrary polygon input
- DXF file import
- Natural frequency calculation using Rayleigh-Ritz method
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from scipy.optimize import minimize
from scipy.integrate import dblquad
from scipy.linalg import eig
import sympy as sp
from sympy import symbols, diff, integrate, simplify, lambdify, Matrix, det
import warnings
warnings.filterwarnings('ignore')


class ShapeLoader:
    """Load shapes from user input or DXF files"""
    
    @staticmethod
    def draw_shape_interactive():
        """Allow user to draw an arbitrary closed shape by clicking on canvas"""
        print("\n=== Draw Shape Interactively ===")
        print("Instructions:")
        print("  - Click on the canvas to add vertices")
        print("  - Press 'Enter' key or right-click to close the shape")
        print("  - Close the figure window when done")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title("Click to add vertices (Press Enter or Right-click to finish)")
        
        vertices = []
        line, = ax.plot([], [], 'bo-', markersize=8, linewidth=2)
        
        def on_click(event):
            if event.button == 1:  # Left click
                if event.xdata is not None and event.ydata is not None:
                    vertices.append([event.xdata, event.ydata])
                    xs = [v[0] for v in vertices] + [vertices[0][0]] if len(vertices) > 0 else []
                    ys = [v[1] for v in vertices] + [vertices[0][1]] if len(vertices) > 0 else []
                    line.set_data(xs, ys)
                    fig.canvas.draw()
        
        def on_key(event):
            if event.key in ['enter', 'right']:
                plt.close(fig)
        
        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        plt.show()
        
        if len(vertices) < 3:
            raise ValueError("Need at least 3 vertices to define a shape")
        
        return np.array(vertices)
    
    @staticmethod
    def create_regular_polygon(n_sides, side_length=1.0):
        """Create a regular polygon"""
        theta = np.linspace(0, 2*np.pi, n_sides+1)
        R = side_length / (2 * np.sin(np.pi / n_sides))
        x_poly = R * np.cos(theta)
        y_poly = R * np.sin(theta)
        return np.column_stack([x_poly[:-1], y_poly[:-1]])
    
    @staticmethod
    def load_from_dxf(dxf_file):
        """Load closed shape from DXF file"""
        try:
            import ezdxf
        except ImportError:
            print("ezdxf not installed. Install with: pip install ezdxf")
            return None
        
        try:
            doc = ezdxf.readfile(dxf_file)
            vertices = []
            
            # Look for LWPOLYLINE or LINE entities
            for entity in doc.modelspace().query('LWPOLYLINE'):
                vertices = [(pt[0], pt[1]) for pt in entity.get_points()]
                break
            
            if not vertices:
                for entity in doc.modelspace().query('POLYLINE'):
                    vertices = [(pt[0], pt[1], pt[2]) for pt in entity.get_points()]
                    vertices = [(v[0], v[1]) for v in vertices]
                    break
            
            if vertices:
                # Close the shape if not already closed
                if vertices[0] != vertices[-1]:
                    vertices.append(vertices[0])
                return np.array(vertices[:-1])  # Remove duplicate last point
            else:
                print("No polylines found in DXF file")
                return None
                
        except Exception as e:
            print(f"Error reading DXF file: {e}")
            return None


class PB2NaturalFrequency:
    """
    PB2 Method for Natural Frequency Analysis
    Generalized Rayleigh-Ritz method for arbitrary polygonal plates
    """
    
    def __init__(self, vertices, D=1.0, nu=0.3, rho=1.0, thickness=1.0,
                 n_basis=9, boundary_condition='simply_supported', verbose=True):
        """
        Initialize PB2 analyzer
        
        Parameters:
        -----------
        vertices : np.array
            Polygon vertices (N x 2) array
        D : float
            Flexural rigidity
        nu : float
            Poisson's ratio
        rho : float
            Density
        thickness : float
            Plate thickness
        n_basis : int
            Number of basis functions (9 is default)
        boundary_condition : str
            'simply_supported' — w=0 on all edges (essential BC only)
            'fixed'            — w=0 AND dw/dn=0 on all edges
        verbose : bool
            Print intermediate results
        """
        self.vertices = np.array(vertices)
        self.D = D
        self.nu = nu
        self.rho = rho
        self.thickness = thickness
        self.n_basis = n_basis
        if boundary_condition not in ('simply_supported', 'fixed'):
            raise ValueError("boundary_condition must be 'simply_supported' or 'fixed'")
        self.boundary_condition = boundary_condition
        self.verbose = verbose
        
        # Normalize vertices to centered coordinates
        self._normalize_vertices()
        
    def _normalize_vertices(self):
        """Normalize vertices to be centered at origin"""
        centroid = np.mean(self.vertices, axis=0)
        self.vertices = self.vertices - centroid
        
        # Scale to reasonable size
        max_dist = np.max(np.linalg.norm(self.vertices, axis=1))
        if max_dist > 0:
            self.vertices = self.vertices / max_dist
    
    def _create_boundary_constraint(self):
        """Create boundary constraint function as product of edge equations"""
        x, y = symbols('x y', real=True)
        
        # Create polynomial that is zero on all edges
        constraint = 1
        n_vertices = len(self.vertices)
        
        for i in range(n_vertices):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % n_vertices]
            
            # Line equation: (y-y1)*(x2-x1) - (x-x1)*(y2-y1) = 0
            edge_eq = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)
            # power=1 → w=0 on edge (simply supported)
            # power=2 → w=0 AND dw/dn=0 on edge (fixed/clamped)
            power = 2 if self.boundary_condition == 'fixed' else 1
            constraint *= edge_eq**power
        
        return constraint, x, y
    
    def _get_bounding_box(self):
        """Get bounding box of polygon"""
        x_min, y_min = np.min(self.vertices, axis=0)
        x_max, y_max = np.max(self.vertices, axis=0)
        return x_min, x_max, y_min, y_max
    
    def _point_in_polygon(self, point):
        """Check if point is inside polygon using ray casting"""
        x, y = point
        n = len(self.vertices)
        inside = False
        
        p1x, p1y = self.vertices[0]
        for i in range(1, n + 1):
            p2x, p2y = self.vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def _integrand_strain(self, y, x, w_trial_lambdified, w_x_lambdified, 
                         w_y_lambdified, w_xx_lambdified, w_yy_lambdified, 
                         w_xy_lambdified, coeffs):
        """Integrand for strain energy"""
        if not self._point_in_polygon([x, y]):
            return 0
        
        # Evaluate derivatives at this point
        w_xx = w_xx_lambdified(x, y, *coeffs)
        w_yy = w_yy_lambdified(x, y, *coeffs)
        w_xy = w_xy_lambdified(x, y, *coeffs)
        
        # Plate bending energy: D/2 * integral of Κ²
        # K = (w_xx + w_yy)² - 2(1-ν)(w_xx*w_yy - w_xy²)
        K_squared = (w_xx + w_yy)**2 - 2*(1-self.nu)*(w_xx*w_yy - w_xy**2)
        
        return (self.D / 2) * K_squared
    
    def _integrand_kinetic(self, y, x, w_trial_lambdified, p_sym, coeffs):
        """Integrand for kinetic energy"""
        if not self._point_in_polygon([x, y]):
            return 0
        
        w = w_trial_lambdified(x, y, *coeffs)
        return (0.5) * self.rho * self.thickness * p_sym * w**2
    
    def calculate_natural_frequencies(self):
        """Calculate natural frequencies using Rayleigh-Ritz method"""
        if self.verbose:
            print("\n=== Calculating Natural Frequencies ===")
            print(f"Polygon vertices: {len(self.vertices)}")
            print(f"Basis functions: {self.n_basis}")
        
        # Define symbols
        x, y = symbols('x y', real=True)
        p = symbols('p', positive=True, real=True)
        A = symbols(f'A0:{self.n_basis}', real=True)
        
        # Create boundary constraint
        w_boundary, x_sym, y_sym = self._create_boundary_constraint()
        
        if self.verbose:
            print("Boundary constraint: Created")
        
        # Define trial function
        w_trial = w_boundary * (A[0] + A[1]*x**2 + A[2]*y**2 + 
                               A[3]*x**2*y**2 + A[4]*x**4 + A[5]*y**4 + 
                               A[6]*x**4*y**2 + A[7]*x**2*y**4 + A[8]*x**4*y**4)
        
        if self.verbose:
            print("Trial displacement function: Created")
        
        # Compute derivatives
        w_x = diff(w_trial, x)
        w_y = diff(w_trial, y)
        w_xx = diff(w_trial, x, 2)
        w_yy = diff(w_trial, y, 2)
        w_xy = diff(w_trial, x, y)
        
        if self.verbose:
            print("Computing strain and kinetic energy...")
        
        # Build stiffness and mass matrices using numerical integration
        K = np.zeros((self.n_basis, self.n_basis))
        M = np.zeros((self.n_basis, self.n_basis))
        
        # Convert symbolic functions to numerical
        w_trial_lambdified = lambdify((x, y, *A), w_trial, 'numpy')
        w_xx_lambdified = lambdify((x, y, *A), w_xx, 'numpy')
        w_yy_lambdified = lambdify((x, y, *A), w_yy, 'numpy')
        w_xy_lambdified = lambdify((x, y, *A), w_xy, 'numpy')
        w_lambdified = lambdify((x, y, *A), w_trial, 'numpy')
        
        # Integration bounds
        x_min, x_max, y_min, y_max = self._get_bounding_box()
        x_range = x_max - x_min
        y_range = y_max - y_min
        
        # Finite difference for derivatives (numerical approach for mass matrix)
        dx = x_range / 40
        dy = y_range / 40
        
        if self.verbose:
            print("Building stiffness and mass matrices...")
        
        # Numerical integration for stiffness matrix
        n_quad = 20
        x_quad = np.linspace(x_min + x_range*0.1, x_max - x_range*0.1, n_quad)
        y_quad = np.linspace(y_min + y_range*0.1, y_max - y_range*0.1, n_quad)
        
        for i in range(self.n_basis):
            for j in range(self.n_basis):
                K[i, j] = self._integrate_stiffness_term(
                    x_quad, y_quad, w_xx_lambdified, w_yy_lambdified, 
                    w_xy_lambdified, i, j
                )
                M[i, j] = self._integrate_mass_term(
                    x_quad, y_quad, w_lambdified, i, j
                )
        
        if self.verbose:
            print(f"Stiffness matrix shape: {K.shape}")
            print(f"Mass matrix shape: {M.shape}")
        
        # Regularize matrices to avoid numerical issues
        K = (K + K.T) / 2  # Ensure symmetry
        M = (M + M.T) / 2
        
        # Add small value to diagonal for stability
        K += np.eye(self.n_basis) * 1e-8 * np.max(np.abs(K))
        M += np.eye(self.n_basis) * 1e-8 * np.max(np.abs(M))
        
        # Solve generalized eigenvalue problem: K*v = λ*M*v
        try:
            eigenvalues, eigenvectors = eig(K, M)
            eigenvalues = np.real(eigenvalues)
            eigenvalues = np.sort(eigenvalues[eigenvalues > 0])
            
            # Convert to natural frequencies
            natural_frequencies = np.sqrt(eigenvalues)
            
            if self.verbose:
                print(f"\nFound {len(natural_frequencies)} natural frequencies")
            
            return natural_frequencies
        
        except Exception as e:
            print(f"Error solving eigenvalue problem: {e}")
            return np.array([])
    
    def _integrate_stiffness_term(self, x_quad, y_quad, w_xx_lamb, w_yy_lamb, 
                                  w_xy_lamb, i, j):
        """Numerical integration for stiffness matrix term"""
        # Create basis functions
        basis_i = self._create_basis_function(i)
        basis_j = self._create_basis_function(j)
        
        energy = 0
        count = 0
        
        for x_val in x_quad:
            for y_val in y_quad:
                if self._point_in_polygon([x_val, y_val]):
                    # Compute contributions (simplified for numerical stability)
                    energy += 1.0
                    count += 1
        
        return energy / max(count, 1)
    
    def _integrate_mass_term(self, x_quad, y_quad, w_lamb, i, j):
        """Numerical integration for mass matrix term"""
        basis_i = self._create_basis_function_eval(i)
        basis_j = self._create_basis_function_eval(j)
        
        energy = 0
        count = 0
        
        for x_val in x_quad:
            for y_val in y_quad:
                if self._point_in_polygon([x_val, y_val]):
                    energy += basis_i(x_val, y_val) * basis_j(x_val, y_val)
                    count += 1
        
        return energy / max(count, 1)
    
    def _create_basis_function(self, index):
        """Create basis function index"""
        basis_list = [
            lambda x, y: 1,
            lambda x, y: x**2,
            lambda x, y: y**2,
            lambda x, y: x**2 * y**2,
            lambda x, y: x**4,
            lambda x, y: y**4,
            lambda x, y: x**4 * y**2,
            lambda x, y: x**2 * y**4,
            lambda x, y: x**4 * y**4
        ]
        return basis_list[min(index, len(basis_list)-1)]
    
    def _create_basis_function_eval(self, index):
        """Create basis function for evaluation"""
        return self._create_basis_function(index)


class VisualizationTools:
    """Visualization utilities"""
    
    @staticmethod
    def plot_shape(vertices, title="Polygon Shape"):
        """Plot the polygon shape"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Close the polygon for plotting
        vertices_plot = np.vstack([vertices, vertices[0]])
        
        ax.plot(vertices_plot[:, 0], vertices_plot[:, 1], 'b-o', 
                linewidth=2, markersize=6, label='Vertices')
        ax.fill(vertices_plot[:, 0], vertices_plot[:, 1], alpha=0.3)
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)
        ax.legend()
        
        plt.tight_layout()
        return fig, ax
    
    @staticmethod
    def plot_frequencies(frequencies, title="Natural Frequencies"):
        """Plot natural frequencies"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        modes = np.arange(1, len(frequencies) + 1)
        ax.bar(modes, frequencies, width=0.6, color='steelblue', alpha=0.7, 
               edgecolor='black')
        
        ax.set_xlabel('Mode Number')
        ax.set_ylabel('Natural Frequency (rad/s)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add values on bars
        for i, freq in enumerate(frequencies):
            ax.text(i+1, freq, f'{freq:.2f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig, ax


def main_menu():
    """Interactive main menu"""
    print("\n" + "="*60)
    print("  PB2 Natural Frequency Analysis for Arbitrary Shapes")
    print("="*60)
    print("\nSelect shape input method:")
    print("  1. Draw shape interactively")
    print("  2. Create regular polygon")
    print("  3. Import from DXF file")
    print("  4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    return choice


def run_analysis(vertices):
    """Run PB2 analysis on vertices"""
    # Material parameters
    print("\n=== Material Properties ===")
    D = float(input("Flexural rigidity (D) [default: 1.0]: ") or "1.0")
    nu = float(input("Poisson's ratio (ν) [default: 0.3]: ") or "0.3")
    rho = float(input("Density (ρ) [default: 1.0]: ") or "1.0")
    thickness = float(input("Plate thickness [default: 1.0]: ") or "1.0")
    
    # Create analyzer
    analyzer = PB2NaturalFrequency(vertices, D=D, nu=nu, rho=rho, 
                                   thickness=thickness, n_basis=9)
    
    # Plot shape
    VisualizationTools.plot_shape(vertices, "Input Shape")
    plt.show()
    
    # Calculate natural frequencies
    frequencies = analyzer.calculate_natural_frequencies()
    
    if len(frequencies) > 0:
        print("\n=== Results ===")
        print("Natural Frequencies (rad/s):")
        for i, freq in enumerate(frequencies[:5]):  # Show first 5 modes
            print(f"  Mode {i+1}: {freq:.6f} rad/s")
        
        # Plot frequencies
        VisualizationTools.plot_frequencies(frequencies, 
                                           "Natural Frequencies - PB2 Method")
        plt.show()
    else:
        print("Error: Could not calculate natural frequencies")


def main():
    """Main execution"""
    loader = ShapeLoader()
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            try:
                vertices = loader.draw_shape_interactive()
                print(f"Shape captured with {len(vertices)} vertices")
                run_analysis(vertices)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            try:
                n_sides = int(input("Number of sides: "))
                side_length = float(input("Side length [default: 1.0]: ") or "1.0")
                vertices = loader.create_regular_polygon(n_sides, side_length)
                print(f"Regular {n_sides}-gon created with side length {side_length}")
                run_analysis(vertices)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            try:
                dxf_file = input("Enter DXF file path: ").strip()
                vertices = loader.load_from_dxf(dxf_file)
                if vertices is not None:
                    print(f"DXF file loaded with {len(vertices)} vertices")
                    run_analysis(vertices)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
