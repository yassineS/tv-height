import streamlit as st

def main():
    st.set_page_config(page_title="Ideal TV Height Calculator", page_icon="📺")
    
    st.title("📺 Ideal TV Height Calculator")
    st.markdown(
        """
        Calculate the ideal mounting height for your TV.  
        Based on the formula by [KEF Australia](https://au.kef.com/blogs/news/calculate-the-ideal-tv-height).
        """
    )
    
    st.divider()

    # --- SECTION 1: INPUTS ---
    st.header("1. Your Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tv_size_inch = st.number_input(
            "TV Size (Diagonal inches)", 
            min_value=32, 
            max_value=120, 
            value=65, 
            step=1,
            format="%d"
        )

    with col2:
        eye_level_cm = st.number_input(
            "Eye Level Height (cm)", 
            min_value=50.0, 
            max_value=150.0, 
            value=92.0, 
            step=1.0,
            help="Height from floor to your eyes when seated."
        )

    # --- DISTANCE LOGIC ---
    # Calculate the theoretical recommended distance first
    # Formula: TV Diameter (inches) * 1.67
    rec_dist_inches = tv_size_inch * 1.67
    rec_dist_m = (rec_dist_inches * 2.54) / 100

    st.write("") # Spacer
    
    # Toggle for manual distance
    use_manual_dist = st.checkbox("I sit at a specific distance (Override recommendation)")
    
    if use_manual_dist:
        manual_dist_m = st.number_input(
            "Your Actual Viewing Distance (meters)",
            min_value=0.5,
            max_value=10.0,
            value=3.6, # Default based on your example
            step=0.1
        )
        
        # Use the manual distance for calculation
        final_dist_m = manual_dist_m
        dist_source_label = "Your Distance"
        
        # Show comparison
        st.caption(f"ℹ️ *Note: The standard recommended distance for this TV size is {rec_dist_m:.2f}m.*")
    else:
        # Use the recommended distance
        final_dist_m = rec_dist_m
        dist_source_label = "Recommended Distance"

    # --- CALCULATIONS ---
    # Convert distance to cm for the formula
    final_dist_cm = final_dist_m * 100
    
    # Formula: EL + (VD * 0.22) = TVH
    tv_mounting_height_cm = eye_level_cm + (final_dist_cm * 0.22)

    st.divider()

    # --- SECTION 2: RESULTS ---
    st.header("2. Results")

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.info(f"**{dist_source_label}**\n\n# {final_dist_m:.2f} m")

    with res_col2:
        st.success(f"**Ideal Centre Height**\n\n# {tv_mounting_height_cm:.1f} cm")
    
    st.caption("Measure from the floor to the exact center of the TV screen.")

    # --- SECTION 3: DETAILS ---
    with st.expander("See Calculation Breakdown"):
        st.markdown("### 1. Variables")
        st.write(f"- **Eye Level (EL):** {eye_level_cm} cm")
        st.write(f"- **Viewing Distance (VD):** {final_dist_cm:.1f} cm")
        st.write("- **Vertical Factor:** 0.22 (coefficient for comfortable viewing angle)")

        st.markdown("### 2. The Math")
        st.markdown("The formula calculates how much higher the TV should be relative to your eyes based on how far away you are sitting.")
        
        # Using LaTeX for the formula strictly, text for the numbers
        st.latex(r"Height = EL + (VD \times 0.22)")
        
        st.markdown("**Your calculation:**")
        st.code(f"{eye_level_cm} + ({final_dist_cm:.1f} * 0.22) = {tv_mounting_height_cm:.1f} cm")

if __name__ == "__main__":
    main()
