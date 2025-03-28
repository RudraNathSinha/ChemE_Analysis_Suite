import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List

def create_bubble_plot(
    image: np.ndarray,
    circles: np.ndarray,
    scale: float,
    dimensions: tuple
) -> go.Figure:
    """Create interactive bubble visualization."""
    fig = go.Figure()
    
    # Add image
    fig.add_layout_image(
        dict(
            source=image,
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=dimensions[1],
            sizey=dimensions[0],
            sizing="stretch",
            layer="below"
        )
    )
    
    # Add detected bubbles
    if circles is not None:
        for circle in circles[0]:
            x, y, r = circle
            fig.add_shape(
                type="circle",
                xref="x",
                yref="y",
                x0=x-r,
                y0=y-r,
                x1=x+r,
                y1=y+r,
                line_color="red"
            )
    
    fig.update_layout(
        title="Detected Bubbles",
        xaxis=dict(range=[0, dimensions[1]]),
        yaxis=dict(range=[0, dimensions[0]], scaleanchor="x", scaleratio=1),
        width=800,
        height=800
    )
    
    return fig
