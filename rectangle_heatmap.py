import numpy as np
import plotly.graph_objects as go
from plotly.colors import sample_colorscale

def circular_heatmap(data, r_min=0.2, r_max=1.0):
    """
    Draw a circular heatmap with filled colored wedges.

    Parameters:
    - data: 2D numpy array of shape (rows, cols)
    - r_min: inner radius of innermost ring (default 0.2 to avoid center overlap)
    - r_max: outer radius of outermost ring (default 1.0)

    Returns:
    - Plotly Figure object
    """
    rows, cols = data.shape
    fig = go.Figure()

    # Normalize data for color scaling
    z_min, z_max = np.min(data), np.max(data)

    # Compute radii for each ring
    radii = np.linspace(r_min, r_max, rows + 1)  # rows+1 boundaries

    # Compute theta boundaries for each segment
    thetas = np.linspace(0, 2 * np.pi, cols + 1)

    # Colorscale
    colorscale = 'Viridis'

    # Draw each wedge as a filled polygon
    for i in range(rows):
        for j in range(cols):
            theta_start = thetas[j]
            theta_end = thetas[j+1]
            r_inner = radii[i]
            r_outer = radii[i+1]
            num_points = 30

            # Outer arc points
            outer_arc = [
                (
                    r_outer * np.cos(theta),
                    r_outer * np.sin(theta)
                )
                for theta in np.linspace(theta_start, theta_end, num_points)
            ]

            # Inner arc points (reversed)
            inner_arc = [
                (
                    r_inner * np.cos(theta),
                    r_inner * np.sin(theta)
                )
                for theta in np.linspace(theta_end, theta_start, num_points)
            ]

            polygon_points = outer_arc + inner_arc

            x_coords = [p[0] for p in polygon_points] + [polygon_points[0][0]]  # close polygon
            y_coords = [p[1] for p in polygon_points] + [polygon_points[0][1]]

            # Normalize value for colorscale sampling
            val_norm = (data[i, j] - z_min) / (z_max - z_min + 1e-9)
            color = sample_colorscale(colorscale, val_norm)[0]

            fig.add_trace(go.Scatter(
                x=x_coords,
                y=y_coords,
                fill='toself',
                fillcolor=color,
                line=dict(width=0),
                mode='lines',
                hoverinfo='text',
                text=f'Value: {data[i,j]:.3f}',
                showlegend=False,
            ))

    # Add invisible dummy scatter for colorbar
    flat_data = data.flatten()

    fig.add_trace(go.Scatter(
        x=[None]*len(flat_data),
        y=[None]*len(flat_data),
        mode='markers',
        marker=dict(
            colorscale=colorscale,
            color=flat_data,
            cmin=z_min,
            cmax=z_max,
            showscale=True,
            colorbar=dict(
                title='Value',
                thickness=20,
                len=0.8,
                y=0.5,
                yanchor='middle',
            ),
            size=0.1,    # very small markers
            opacity=0    # fully transparent
        ),
        hoverinfo='none',
        showlegend=False
    ))

    fig.update_layout(
        title='Circular Heatmap',
        xaxis=dict(scaleanchor='y', scaleratio=1, showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        width=600,
    )

    return fig
