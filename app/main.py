import streamlit as st
from pages import bubble_analysis, mass_transfer

def main():
    st.set_page_config(
        page_title="Chemical Engineering Analysis Suite",
        page_icon="⚗️",
        layout="wide"
    )
    
    st.title("Chemical Engineering Analysis Suite")
    st.sidebar.title("Navigation")

    pages = {
        "Home": None,
        "Bubble Analysis": bubble_analysis.app,
        "Mass Transfer Analysis": mass_transfer.app
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()))

    if selection == "Home":
        st.write("Welcome to the Chemical Engineering Analysis Suite!")
        st.write("""
        This suite provides advanced tools for chemical engineering analysis:
        - Bubble Analysis Tool: Analyze bubble size and distribution in images
        - Mass Transfer Analysis: Calculate mass transfer coefficients
        - Data Visualization: Interactive plots and analytics
        - Statistical Analysis: Comprehensive statistical tools
        """)
        
        # Add project information
        st.markdown("""
        ### Project Features
        - Advanced image processing for bubble detection
        - Mass transfer coefficient calculations
        - Dimensionless number analysis
        - Interactive data visualization
        - Statistical analysis tools
        - Report generation
        
        ### Getting Started
        1. Select a tool from the sidebar
        2. Upload your data or images
        3. Adjust parameters as needed
        4. View and export results
        """)
    else:
        pages[selection]()

if __name__ == "__main__":
    main()
