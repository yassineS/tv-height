import streamlit as st

def main():
    st.set_page_config(page_title="Ideal TV Height Calculator", page_icon="📺")
    
    st.title("📺 Ideal TV Height Calculator")
    st.markdown(
        """
        This calculator helps you determine the ideal mounting height for your TV based on the 
        formula described by [KEF Australia](https://au.kef.com/blogs/news/calculate-the-ideal-tv-height).
        """
    )
    
    st.divider()

    # --- INPUTS ---
    st.header("1. Enter Your Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # TV Size is almost always sold in inches, so we keep this input in inches
        tv_size_inch = st.number_input(
            "TV Size (Diagonal)", 
            min_value=32, 
            max_value=120, 
            value=65, 
            step=1,
            format="%d",
            help="The diagonal screen size in inches (e.g., 55, 65, 75)."
        )

    with col2:
        # Eye level input in cm (Australian preference)
        eye_level_cm = st.number_input(
            "Eye Level Height (cm)", 
            min_value=50.0, 
            max_value=150.0, 
            value=92.0, 
            step=1.0,
            help="Measure the height from the floor to your eyes while seated in your viewing position."
        )

    # --- CALCULATIONS ---
    # 1. Calculate Viewing Distance (VD)
    # Formula from article: VD = TV diameter * 1.67
    vd_inches = tv_size_inch * 1.67
    vd_cm = vd_inches * 2.54 # Convert to cm for display and next calculation
    vd_meters = vd_cm / 100

    # 2. Calculate TV Mounting Height (TVH)
    # Formula from article: EL + (VD * 0.22) = TVH
    # Where EL = Eye Level, VD = Viewing Distance
    # Note: 0.22 represents the tangent of the vertical viewing angle offset (~12.4 degrees)
    tv_mounting_height_cm = eye_level_cm + (vd_cm * 0.22)
    
    st.divider()

    # --- RESULTS ---
    st.header("2. Results")

    # Display Viewing Distance
    st.subheader("Ideal Viewing Distance")
    st.write("Based on your TV size, this is how far you should sit from the screen:")
    st.info(f"**{vd_meters:.2f} meters** ({vd_inches:.1f} inches)")
    
    # Display Mounting Height
    st.subheader("Ideal Mounting Height (Centre)")
    st.write("This is the ideal height from the floor to the **exact center** of your TV screen:")
    st.success(f"**{tv_mounting_height_cm:.1f} cm**")

    # Visual explanation of the math
    with st.expander("See Calculation Details"):
        st.markdown(f"""
        **1. Viewing Distance Formula:**  
        \( VD = \\text{{TV Size}} \\times 1.67 \)  
        \( {tv_size_inch} \\times 1.67 = {vd_inches:.2f} \\text{{ inches}} \) ({vd_cm:.1f} cm)
        
        **2. Mounting Height Formula:**  
        \( TVH = EL + (VD \\times 0.22) \)  
        Where:
        *   **EL (Eye Level)**: {eye_level_cm} cm
        *   **VD (Viewing Distance)**: {vd_cm:.1f} cm
        *   **0.22**: Vertical angle factor
        
        \( {eye_level_cm} + ({vd_cm:.1f} \\times 0.22) = \\mathbf{{{tv_mounting_height_cm:.2f} \\text{{ cm}}}} \)
        """)

if __name__ == "__main__":
    main()
