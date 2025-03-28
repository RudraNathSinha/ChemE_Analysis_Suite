import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import plotly.graph_objects as go
from datetime import datetime
import os
import io
from ..utils import bubble_detection

def image_to_bytes(image: Image.Image) -> bytes:
    img_bytes_io = io.BytesIO()
    image.save(img_bytes_io, format="PNG")
    return img_bytes_io.getvalue()

def get_saved_images():
    """Retrieve list of saved images."""
    if not os.path.exists('saved_images'):
        os.makedirs('saved_images')
    return [f for f in os.listdir('saved_images') if os.path.isfile(os.path.join('saved_images', f))]

def app():
    st.title("🔍 Bubble Analyzer Pro")

    # Initialize session states
    states = ['confirmed', 'analyze', 'selected_rank']
    for state in states:
        if (state not in st.session_state):
            st.session_state[state] = False if state != 'selected_rank' else 1

    # File uploader
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    # Option to load previously saved images
    saved_images = get_saved_images()
    selected_saved_image = st.selectbox("Or select a previously uploaded image", ["None"] + saved_images)

    if selected_saved_image != "None":
        uploaded_file = open(os.path.join('saved_images', selected_saved_image), "rb")
        st.success(f"Loaded saved image: {selected_saved_image}")

    if uploaded_file:
        # Handle image confirmation and analysis
        handle_image_analysis(uploaded_file, selected_saved_image)

def handle_image_analysis(uploaded_file, selected_saved_image):
    """Handle image confirmation and analysis process"""
    if not st.session_state.confirmed:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("✅ Confirm Image"):
                st.session_state.confirmed = True
                st.rerun()

    if st.session_state.confirmed:
        # Image saving option
        save_image = st.checkbox("Save image for future analysis")
        if save_image and selected_saved_image == "None":
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            save_path = f"saved_images/{timestamp}_{uploaded_file.name}"
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Image saved to: {save_path}")

        # Get detection parameters and analyze image
        bubble_params = get_detection_parameters()
        
        if st.button("🔍 Start Image Analysis"):
            analyze_and_display_results(uploaded_file, bubble_params)

def get_detection_parameters():
    """Get bubble detection parameters from user input."""
    with st.expander("⚙️ Detection Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            dp = st.slider("Detection Precision", 1.0, 3.0, 1.2)
            min_dist = st.slider("Minimum Bubble Distance (px)", 10, 100, 20)
            param1 = st.slider("Edge Detection Threshold", 30, 300, 50)
        with col2:
            param2 = st.slider("Circle Accumulator Threshold", 10, 100, 30)
            min_radius = st.slider("Minimum Radius", 0, 100, 0)
            max_radius = st.slider("Maximum Radius", 10, 500, 100)
        
        scale_factor = st.number_input("Pixels per cm", min_value=1.0, value=100.0)
        speed_mode = st.checkbox("Fast Processing Mode", True)

        return {
            'dp': dp,
            'minDist': min_dist,
            'param1': param1,
            'param2': param2,
            'minRadius': min_radius,
            'maxRadius': max_radius,
            'speed_mode': speed_mode,
            'scale_factor': scale_factor
        }

def analyze_and_display_results(image_file, params):
    """Analyze image and display results."""
    image = Image.open(image_file)
    image_bytes = image_to_bytes(image)

    # Run image analysis
    circles, processed_img, scale, dimensions = bubble_detection.analyze_image(
        image_bytes, params, params['scale_factor']
    )

    # Create output tabs
    tabs = ["📤 Original", "📊 Overview", "📋 Metrics", "🔴 Marked Bubbles", "📌 Rank Analysis"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)

    if circles is not None:
        # Convert processed image coordinates to original dimensions
        orig_width, orig_height = dimensions
        circles_np = np.uint16(np.around(circles))
        
        # Create dataframe with scaled coordinates
        bubble_data = []
        for circle in circles_np[0, :]:
            x_proc, y_proc, r_proc = circle
            x_orig = int((x_proc / scale) * (orig_width / (orig_width * scale)))
            y_orig = int((y_proc / scale) * (orig_height / (orig_height * scale)))
            radius_orig = int(r_proc / scale)
            
            bubble_data.append({
                'x': x_orig,
                'y': y_orig,
                'radius': radius_orig,
                'diameter_px': 2 * radius_orig,
                'diameter_mm': (2 * radius_orig) * (10 / params['scale_factor']),
                'diameter_cm': (2 * radius_orig) / params['scale_factor'],
            })

        df_metrics = pd.DataFrame(bubble_data)
        df_metrics['Area (cm²)'] = np.pi * (df_metrics['diameter_cm']/2)**2
        df_metrics = df_metrics.sort_values(by='diameter_px', ascending=False)
        df_metrics['Rank'] = range(1, len(df_metrics)+1)
        df_metrics = df_metrics[['Rank', 'x', 'y', 'diameter_px', 'diameter_mm', 
                               'diameter_cm', 'Area (cm²)']]

        # Display tabs content
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original Image", use_container_width=True)
            with col2:
                # Display processed image with detected bubbles
                output_img = processed_img.copy()
                for circle in circles_np[0]:
                    cv2.circle(output_img, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
                    cv2.circle(output_img, (circle[0], circle[1]), 2, (0, 0, 255), 3)
                st.image(output_img, caption="Processed Image", use_container_width=True)

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Key Metrics")
                st.metric("Total Bubbles", len(df_metrics))
                st.metric("Avg Diameter (cm)", f"{df_metrics['diameter_cm'].mean():.4f}")
            with col2:
                st.subheader("Size Distribution")
                fig = go.Figure([go.Histogram(x=df_metrics['diameter_cm'], nbinsx=20)])
                fig.update_layout(
                    xaxis_title="Diameter (cm)",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.dataframe(df_metrics.style.format({
                'diameter_cm': '{:.4f}',
                'Area (cm²)': '{:.4f}'
            }))

        with tab4:
            # Create marked image
            marked_image = np.array(image)
            for idx, row in df_metrics.iterrows():
                x, y, r = int(row['x']), int(row['y']), int(row['diameter_px']/2)
                cv2.rectangle(marked_image, 
                            (x-r, y-r), 
                            (x+r, y+r), 
                            (0, 0, 255), 2)
                cv2.putText(marked_image, 
                          str(row['Rank']), 
                          (x+r+5, y), 
                          cv2.FONT_HERSHEY_SIMPLEX, 
                          0.7, 
                          (0, 0, 255), 
                          2)
            st.image(marked_image, caption="Ranked Bubbles", use_container_width=True)

        with tab5:
            max_rank = len(df_metrics)
            selected_rank = st.number_input("Enter Bubble Rank", 
                                          min_value=1, 
                                          max_value=max_rank, 
                                          value=1)
            if selected_rank:
                bubble = df_metrics[df_metrics['Rank'] == selected_rank].iloc[0]
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Diameter (cm)", f"{bubble['diameter_cm']:.4f}")
                    st.metric("Position X", f"{bubble['x']} px")
                with col2:
                    st.metric("Area (cm²)", f"{bubble['Area (cm²)']:.4f}")
                    st.metric("Position Y", f"{bubble['y']} px")
                
                # Highlight selected bubble
                highlighted = marked_image.copy()
                x, y, r = int(bubble['x']), int(bubble['y']), int(bubble['diameter_px']/2)
                cv2.rectangle(highlighted, 
                            (x-r, y-r), 
                            (x+r, y+r), 
                            (0, 255, 0), 3)
                st.image(highlighted, 
                        caption=f"Bubble Rank {selected_rank}", 
                        use_container_width=True)
