"""
PB2 Natural Frequency Analysis - Streamlit Web Application
"""

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import tempfile

from pb2_natural_frequency import PB2NaturalFrequency, ShapeLoader

st.set_page_config(
    page_title="PB2 Natural Frequency Analysis",
    page_icon="📐",
    layout="wide"
)

st.title("📐 PB2 Natural Frequency Analysis")
st.markdown(
    "Analyze natural frequencies of arbitrary polygonal plates using the "
    "**PB2 Rayleigh-Ritz method**."
)

# ──────────────────────────────────────────────────────────
# Sidebar – Material Properties
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Material Properties")

    PRESETS = {
        "Custom":    dict(D=1.0,    nu=0.30, rho=1.0,    h=1.0),
        "Steel":     dict(D=1000.0, nu=0.30, rho=7800.0, h=0.01),
        "Aluminum":  dict(D=400.0,  nu=0.33, rho=2700.0, h=0.01),
        "Titanium":  dict(D=800.0,  nu=0.34, rho=4500.0, h=0.01),
        "CFRP":      dict(D=1200.0, nu=0.30, rho=1600.0, h=0.005),
    }

    material = st.selectbox("Material Preset", list(PRESETS.keys()))
    p = PRESETS[material]

    D         = st.number_input("Flexural Rigidity D",   value=p["D"],  min_value=1e-6, format="%.4f")
    nu        = st.number_input("Poisson's Ratio ν",     value=p["nu"], min_value=0.0,  max_value=0.499, format="%.4f")
    rho       = st.number_input("Density ρ  (kg/m³)",    value=p["rho"],min_value=1e-6, format="%.4f")
    thickness = st.number_input("Thickness h (m)",       value=p["h"],  min_value=1e-6, format="%.6f")
    n_basis   = st.slider("Basis Functions (n_basis)", min_value=4, max_value=20, value=9)

    st.markdown("---")
    st.header("🔩 Boundary Condition")
    bc_label = st.radio(
        "Edge Support Type",
        options=["Simply Supported", "Fixed (Clamped)"],
        index=0,
        help=(
            "**Simply Supported** — zero displacement on all edges (w = 0).\n\n"
            "**Fixed (Clamped)** — zero displacement AND zero slope on all edges "
            "(w = 0 and ∂w/∂n = 0)."
        ),
    )
    boundary_condition = "simply_supported" if bc_label == "Simply Supported" else "fixed"

    st.markdown("---")
    st.caption("Values must be positive. ν must be < 0.5.")
    st.caption("""
    <div style="text-align: center; margin-top: 0rem;">
        <p style="font-size: 0.85rem; color: #888;">
            <br>
            <b style="color: #555;">This tool determines the natrual frequencies for a plate of any arbitery shape for all the possible modes of vibration</b><br>
            For Custom set of parameters kindly refer to the Repository.
        </p>
    </div>
    <div style="text-align: center; margin-top: 0rem;">
        <img src="https://iitgn.ac.in/assets/img/logo.png" width="100" style="margin-bottom: 10px;">
        <p style="font-size: 0.85rem; color: #888;">
            Developed in<br>
            <b style="color: #555;">Center of Research Commercialization</b><br>
            Indian Institute of Technology Gandhinagar
        </p>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# Helper: shape + frequency plots
# ──────────────────────────────────────────────────────────

def make_shape_fig(vertices):
    fig, ax = plt.subplots(figsize=(5, 5))
    v = np.vstack([vertices, vertices[0]])
    ax.plot(v[:, 0], v[:, 1], "b-o", linewidth=2, markersize=6)
    ax.fill(v[:, 0], v[:, 1], alpha=0.25)
    for i, (x, y) in enumerate(vertices):
        ax.annotate(str(i + 1), (x, y), textcoords="offset points",
                    xytext=(6, 6), fontsize=8, color="navy")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Input Shape")
    return fig


def make_freq_fig(frequencies):
    fig, ax = plt.subplots(figsize=(8, 4))
    modes = np.arange(1, len(frequencies) + 1)
    bars = ax.bar(modes, frequencies, width=0.6, color="steelblue", alpha=0.75, edgecolor="black")
    ax.set_xlabel("Mode Number")
    ax.set_ylabel("Natural Frequency (rad/s)")
    ax.set_title("Natural Frequencies – PB2 Method")
    ax.grid(True, alpha=0.3, axis="y")
    for bar, freq in zip(bars, frequencies):
        ax.text(bar.get_x() + bar.get_width() / 2, freq, f"{freq:.3f}",
                ha="center", va="bottom", fontsize=8)
    return fig

# ──────────────────────────────────────────────────────────
# Shape Input Tabs
# ──────────────────────────────────────────────────────────

tab_poly, tab_dxf, tab_manual, tab_canvas = st.tabs([
    "🔷 Regular Polygon",
    "📁 Upload DXF",
    "✏️ Enter Vertices",
    "🖊️ Draw Shape",
])

# Persist vertices across reruns
if "vertices" not in st.session_state:
    st.session_state.vertices = None

# ── Tab 1: Regular Polygon ──────────────────────────────
with tab_poly:
    st.subheader("Generate a Regular Polygon")
    col1, col2 = st.columns(2)
    with col1:
        n_sides = st.number_input("Number of sides", min_value=3, max_value=100, value=6, step=1)
    with col2:
        side_length = st.number_input("Side length", min_value=1e-4, value=1.0, format="%.4f")

    if st.button("Generate Polygon", key="gen_poly"):
        loader = ShapeLoader()
        verts = loader.create_regular_polygon(int(n_sides), float(side_length))
        st.session_state.vertices = verts
        st.success(f"Generated regular {n_sides}-gon with side length {side_length:.4f}")

# ── Tab 2: DXF Upload ──────────────────────────────────
with tab_dxf:
    st.subheader("Load Shape from DXF File")
    uploaded = st.file_uploader("Choose a DXF file", type=["dxf"])
    if uploaded is not None:
        with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name
        try:
            loader = ShapeLoader()
            verts = loader.load_from_dxf(tmp_path)
            if verts is not None and len(verts) >= 3:
                st.session_state.vertices = verts
                st.success(f"Loaded {len(verts)} vertices from **{uploaded.name}**")
            else:
                st.error("Could not extract a valid polygon from the DXF file.")
        except Exception as e:
            st.error(f"DXF load error: {e}")
        finally:
            os.remove(tmp_path)

# ── Tab 3: Manual Vertex Entry ─────────────────────────
with tab_manual:
    st.subheader("Enter Vertices Manually")
    st.caption("Add rows to the table. Coordinates should form a closed, non-self-intersecting polygon.")

    import pandas as pd

    # Seed the editor with existing vertices or a default triangle
    if st.session_state.vertices is not None:
        init_df = pd.DataFrame(st.session_state.vertices, columns=["X", "Y"])
    else:
        init_df = pd.DataFrame({"X": [0.0, 1.0, 0.5], "Y": [0.0, 0.0, 0.866]})

    edited = st.data_editor(
        init_df,
        num_rows="dynamic",
        column_config={
            "X": st.column_config.NumberColumn("X", format="%.6f"),
            "Y": st.column_config.NumberColumn("Y", format="%.6f"),
        },
        width="stretch",
        key="vertex_editor",
    )

    if st.button("Use These Vertices", key="use_manual"):
        verts = edited.dropna().values
        if len(verts) < 3:
            st.error("Please enter at least 3 vertices.")
        else:
            st.session_state.vertices = verts
            st.success(f"Set {len(verts)} vertices from table.")

# ── Tab 4: Draw Shape (requires streamlit-drawable-canvas) ─
with tab_canvas:
    st.subheader("Draw Shape on Canvas")
    try:
        from streamlit_drawable_canvas import st_canvas

        st.caption(
            "**How to draw:** Click to place each vertex. "
            "Double-click to close the polygon."
        )

        CANVAS_SIZE = 500
        SCALE = 5.0  # canvas units → real units (1 px = 1/SCALE units)

        canvas_result = st_canvas(
            fill_color="rgba(122, 163, 204, 0.25)",
            stroke_width=2,
            stroke_color="#1a6bc4",
            background_color="#f7f9fb",
            height=CANVAS_SIZE,
            width=CANVAS_SIZE,
            drawing_mode="polygon",
            key="shape_canvas",
        )

        if st.button("Use Drawn Shape", key="use_canvas"):
            objects = (canvas_result.json_data or {}).get("objects", [])
            all_vertices = []
            for obj in objects:
                # streamlit-drawable-canvas returns polygon paths
                path = obj.get("path", [])
                pts = []
                for cmd in path:
                    if cmd[0] in ("M", "L") and len(cmd) >= 3:
                        # Convert from canvas px to real coordinates (origin = centre)
                        px = cmd[1] - CANVAS_SIZE / 2
                        py = -(cmd[2] - CANVAS_SIZE / 2)
                        pts.append([px / SCALE * 2, py / SCALE * 2])
                if len(pts) >= 3:
                    all_vertices.extend(pts)

            if len(all_vertices) >= 3:
                st.session_state.vertices = np.array(all_vertices)
                st.success(f"Captured {len(all_vertices)} vertices from canvas.")
            else:
                st.warning("Could not find a polygon on the canvas. Try drawing again.")

    except ImportError:
        st.info(
            "Install **streamlit-drawable-canvas** to enable the drawing tab:\n\n"
            "```\npip install streamlit-drawable-canvas\n```"
        )

# ──────────────────────────────────────────────────────────
# Preview current vertices
# ──────────────────────────────────────────────────────────
st.markdown("---")

vertices = st.session_state.vertices

if vertices is not None and len(vertices) >= 3:
    verts_arr = np.array(vertices)

    col_prev, col_tbl = st.columns([1, 1])
    with col_prev:
        st.subheader("Shape Preview")
        fig_shape = make_shape_fig(verts_arr)
        st.pyplot(fig_shape, width="stretch")
        plt.close(fig_shape)

    with col_tbl:
        st.subheader("Vertex Coordinates")
        import pandas as pd
        df_v = pd.DataFrame(verts_arr, columns=["X", "Y"])
        df_v.index += 1
        st.dataframe(df_v, width="stretch")

        # Quick geometry info
        area = 0.5 * abs(sum(
            verts_arr[i, 0] * verts_arr[(i + 1) % len(verts_arr), 1] -
            verts_arr[(i + 1) % len(verts_arr), 0] * verts_arr[i, 1]
            for i in range(len(verts_arr))
        ))
        perimeter = sum(
            np.linalg.norm(verts_arr[(i + 1) % len(verts_arr)] - verts_arr[i])
            for i in range(len(verts_arr))
        )
        st.metric("Area",      f"{area:.6f}")
        st.metric("Perimeter", f"{perimeter:.6f}")
        st.metric("Vertices",  len(verts_arr))

    # ── Analyze ───────────────────────────────────────────
    st.markdown("---")
    st.subheader("Run Analysis")

    if st.button("▶ Calculate Natural Frequencies", type="primary"):
        with st.spinner("Running PB2 analysis…"):
            try:
                analyzer = PB2NaturalFrequency(
                    vertices=verts_arr,
                    D=float(D),
                    nu=float(nu),
                    rho=float(rho),
                    thickness=float(thickness),
                    n_basis=int(n_basis),
                    boundary_condition=boundary_condition,
                    verbose=False,
                )
                freqs = analyzer.calculate_natural_frequencies()
                freqs = sorted([float(f) for f in freqs if np.isfinite(f)])

                if not freqs:
                    st.error("Could not compute any finite frequencies. Check your inputs.")
                else:
                    st.success(f"Analysis complete — {len(freqs)} modes computed.")

                    # Results layout
                    res_col1, res_col2 = st.columns([1, 1])

                    with res_col1:
                        st.subheader("Natural Frequencies Table")
                        import pandas as pd
                        df_f = pd.DataFrame({
                            "Mode": range(1, len(freqs) + 1),
                            "Frequency (rad/s)": [f"{f:.6f}" for f in freqs],
                            "Frequency (Hz)":    [f"{f / (2 * np.pi):.6f}" for f in freqs],
                        })
                        df_f = df_f.set_index("Mode")
                        st.dataframe(df_f, width="stretch")

                    with res_col2:
                        st.subheader("Frequency Bar Chart")
                        fig_freq = make_freq_fig(freqs)
                        st.pyplot(fig_freq, width="stretch")
                        plt.close(fig_freq)

            except Exception as e:
                import traceback
                st.error(f"Analysis failed: {e}")
                with st.expander("Full traceback"):
                    st.code(traceback.format_exc())
else:
    st.info("👆 Use one of the tabs above to define a shape, then run the analysis.")

# ============================================================================
# Footer
# ============================================================================

st.divider()
st.markdown("""
---
**PB2 Rayleigh–Ritz Method**
*Based on lectures on Approximate methods of Structural Analysis by Dr. K. bhaskar (2023)*

Built with: Passion | Creativity | Love | 

[🚁 Quadrotor Flight Guidance Simulator](https://dronenavigatorsmc.streamlit.app/) | [📋 Documentation](https://www.sciencedirect.com/science/article/abs/pii/014102969390017X) | [🐛 Report Issues](dhairya.param@iitgn.ac.in)
""")

# ============================================================================
# Footer
# ============================================================================

st.divider()
st.markdown("""
---
**PB2 Rayleigh–Ritz Method**
*Based on lectures on Approximate methods of Structural Analysis by Dr. K. bhaskar (2023)*

Built with: Passion | Creativity | Love | 

[🚁 Quadrotor Flight Guidance Simulator](https://dronenavigatorsmc.streamlit.app/) | [📋 Documentation](https://www.sciencedirect.com/science/article/abs/pii/014102969390017X) | [🐛 Report Issues](dhairya.param@iitgn.ac.in)
""")