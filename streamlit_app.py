import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# --- COLOR PALETTE ---
COLOR_RED = '#E63946'
COLOR_HONEYDEW = '#F1FAEE'
COLOR_LIGHT_BLUE = '#A8DADC'
COLOR_MED_BLUE = '#457B9D'
COLOR_DARK_BLUE = '#1D3557'
COLOR_BLACK = '#000000'

def draw_diagram(dist_cm, eye_level_cm, tv_bottom_cm, tv_height_cm, tv_centre_cm, vert_angle_deg):
    """Generates a side-view diagram of the TV setup."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-50, dist_cm + 100)
    room_height = max(250, tv_bottom_cm + tv_height_cm + 50)
    ax.set_ylim(0, room_height)
    ax.set_aspect('equal')
    ax.axis('off')

    # Floor & Wall
    ax.axhline(y=0, color=COLOR_BLACK, linewidth=2) 
    ax.axvline(x=0, color=COLOR_LIGHT_BLUE, linewidth=4)
    
    # TV
    tv_thickness = 5 
    tv_rect = patches.Rectangle((0, tv_bottom_cm), tv_thickness, tv_height_cm, linewidth=1, edgecolor=COLOR_BLACK, facecolor=COLOR_DARK_BLUE)
    ax.add_patch(tv_rect)
    ax.text(-15, tv_centre_cm, "TV", ha='right', va='center', fontsize=12, fontweight='bold', color=COLOR_DARK_BLUE)

    # Viewer
    ax.scatter(dist_cm, eye_level_cm, s=200, color=COLOR_BLACK, zorder=5)
    ax.plot([dist_cm, dist_cm], [eye_level_cm, eye_level_cm - 60], color=COLOR_BLACK, linewidth=3)
    ax.plot([dist_cm, dist_cm - 20], [eye_level_cm - 30, eye_level_cm - 60], color=COLOR_BLACK, linewidth=3)
    ax.text(dist_cm, eye_level_cm + 25, "Eye Level", ha='center', fontsize=10, color=COLOR_BLACK)

    # Guides
    ax.plot([0, dist_cm], [eye_level_cm, eye_level_cm], color='gray', linestyle='--', alpha=0.4)
    ax.plot([0, dist_cm], [tv_centre_cm, eye_level_cm], color=COLOR_MED_BLUE, linestyle='--', alpha=0.8, linewidth=1.5)
    
    if vert_angle_deg > 0.5:
        arc_diam = dist_cm * 0.4
        angle_patch = patches.Arc((dist_cm, eye_level_cm), width=arc_diam, height=arc_diam, angle=0, theta1=180-vert_angle_deg, theta2=180, color=COLOR_RED, linewidth=2)
        ax.add_patch(angle_patch)
        label_x = dist_cm - (arc_diam/2 * 1.15 * math.cos(math.radians(vert_angle_deg/2)))
        label_y = eye_level_cm + (arc_diam/2 * 1.15 * math.sin(math.radians(vert_angle_deg/2)))
        ax.text(label_x, label_y, f"{vert_angle_deg:.1f}°", color=COLOR_RED, fontsize=9, fontweight='bold', ha='center')
    else:
        ax.text(dist_cm/2, eye_level_cm + 5, "0° (Neutral Neck)", color='gray', fontsize=8, ha='center')

    # Dimensions
    ax.plot([20, 20], [0, tv_bottom_cm], color=COLOR_MED_BLUE, linestyle='-', linewidth=1)
    ax.text(35, tv_bottom_cm / 2, f"{tv_bottom_cm:.1f} cm", color=COLOR_MED_BLUE, va='center', fontweight='bold')
    ax.plot([0, 35], [tv_bottom_cm, tv_bottom_cm], color=COLOR_MED_BLUE, linewidth=0.5)
    ax.plot([0, dist_cm], [10, 10], color='gray', linestyle='-')
    ax.text(dist_cm / 2, 25, f"{dist_cm/100:.2f} m", ha='center', color='gray')

    ax.set_title(f"Side View", fontsize=10, loc='left', color=COLOR_DARK_BLUE)
    return fig

def main():
    st.set_page_config(page_title="Ideal TV Height Calculator", page_icon="📺")
    
    # Initialize Session State for Mode
    if 'setup_mode' not in st.session_state:
        st.session_state.setup_mode = 'standard'

    st.title("📺 Ideal TV Height Calculator")
    st.markdown("Calculate the ideal mounting height and viewing distance for your specific setup.")
    st.divider()

    # --- SECTION 1: MODE SELECTION (BUTTONS) ---
    st.header("1. Choose Setup Style")
    
    col_mode1, col_mode2 = st.columns(2)
    
    with col_mode1:
        # If standard is active, use primary color, else secondary
        if st.button("🛋️ Standard Living Room", 
                     type="primary" if st.session_state.setup_mode == 'standard' else "secondary", 
                     use_container_width=True):
            st.session_state.setup_mode = 'standard'
            st.rerun()
            
    with col_mode2:
        if st.button("🎬 Home Theater (Cinema)", 
                     type="primary" if st.session_state.setup_mode == 'cinema' else "secondary", 
                     use_container_width=True):
            st.session_state.setup_mode = 'cinema'
            st.rerun()

    # Description of current mode
    if st.session_state.setup_mode == 'standard':
        st.info("**Standard Mode:** Optimizes for ergonomic comfort (couch sitting). Aligns TV center with eye level.")
    else:
        st.info("**Cinema Mode:** Optimizes for immersion (reclined seating). Mounts TV higher and uses advanced FOV controls.")

    # --- SECTION 2: INPUTS ---
    st.subheader("Your Measurements")
    col1, col2 = st.columns(2)
    with col1:
        tv_size_inch = st.number_input("TV Size (Diagonal inches)", 32, 120, 65, step=1, format="%d")

    with col2:
        eye_level_cm = st.number_input(
            "Eye Level Height (cm)", 
            min_value=50.0, max_value=150.0, value=92.0, step=1.0,
            help="Measure from floor to eyes while seated. Standard couch height is usually 90-100cm."
        )

    # --- SECTION 3: FIELD OF VIEW (Conditional) ---
    angle_standard = 30 # Default
    
    if st.session_state.setup_mode == 'cinema':
        st.subheader("Field of View (Horizontal)")
        
        angle_standard = st.radio(
            "Select target immersion level:",
            options=[30, 36, 40],
            format_func=lambda x: f"{x}°",
            horizontal=True
        )
        
        # Explicit Descriptions (No tooltip needed)
        if angle_standard == 30:
            st.caption("✅ **30° (SMPTE Standard):** The gold standard for mixed usage (Sports, TV, Gaming). Keeps the whole screen in view.")
        elif angle_standard == 36:
            st.caption("🎥 **36° (THX Recommended):** The sweet spot for movies. Increases immersion without causing eye fatigue.")
        else:
            st.caption("⚠️ **40° (Cinema Limit):** Maximum immersion. Screen fills your peripheral vision. Best for 2.39:1 movies.")
            
    # --- CALCULATIONS ---
    # Screen Math
    screen_width_inch = tv_size_inch * 0.87157
    screen_height_inch = tv_size_inch * 0.4903
    screen_width_cm = screen_width_inch * 2.54
    screen_height_cm = screen_height_inch * 2.54

    # Distance Math
    angle_rad = math.radians(angle_standard)
    rec_dist_inches = (screen_width_inch / 2) / math.tan(angle_rad / 2)
    rec_dist_m = (rec_dist_inches * 2.54) / 100
    
    # Distance Override
    st.write("") 
    use_manual_dist = st.checkbox("I sit at a different distance")
    
    if use_manual_dist:
        manual_dist_m = st.number_input("Your Actual Viewing Distance (meters)", 0.5, 10.0, 3.6, step=0.1)
        final_dist_m = manual_dist_m
        dist_source_label = "Your Distance"
    else:
        final_dist_m = rec_dist_m
        dist_source_label = "Recommended Distance"
    
    final_dist_cm = final_dist_m * 100

    # Height Math
    if st.session_state.setup_mode == 'standard':
        tv_centre_height_cm = eye_level_cm
        vert_angle_deg = 0.0
    else:
        # KEF / Theater Mode formula
        tv_centre_height_cm = eye_level_cm + (final_dist_cm * 0.22)
        vert_angle_rad = math.atan(0.22)
        vert_angle_deg = math.degrees(vert_angle_rad)

    tv_bottom_height_cm = tv_centre_height_cm - (screen_height_cm / 2)
    
    # Actual Horizontal Angle
    act_horiz_angle_rad = 2 * math.atan((screen_width_cm / 2) / final_dist_cm)
    act_horiz_angle_deg = math.degrees(act_horiz_angle_rad)

    st.divider()

    # --- RESULTS ---
    st.header("2. Results")
    
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.info(f"**{dist_source_label}**\n\n# {final_dist_m:.2f} m")
    with r1_col2:
        st.success(f"**Height to Bottom of TV**\n\n# {tv_bottom_height_cm:.1f} cm")
        
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        delta_val = None
        if use_manual_dist:
             delta_val = f"{act_horiz_angle_deg - angle_standard:.1f}° vs Target"
        st.metric("Horizontal Viewing Angle (Width)", f"{act_horiz_angle_deg:.1f}°", delta=delta_val)
    with r2_col2:
        st.metric("Vertical Mounting Angle (Height)", f"{vert_angle_deg:.1f}°")

    # --- DIAGRAM ---
    st.divider()
    st.subheader("Visual Guide")
    fig = draw_diagram(
        dist_cm=final_dist_cm,
        eye_level_cm=eye_level_cm,
        tv_bottom_cm=tv_bottom_height_cm,
        tv_height_cm=screen_height_cm,
        tv_centre_cm=tv_centre_height_cm,
        vert_angle_deg=vert_angle_deg
    )
    st.pyplot(fig, use_container_width=True)

    # --- REFERENCES ---
    st.divider()
    with st.expander("📚 Methodology & References"):
        st.markdown("""
        This calculator uses industry standards to determine optimal placement:
        
        **1. Viewing Distance (Field of View)**
        *   **SMPTE EG-18-1994:** Recommends a minimum viewing angle of **30°** for general usage.
        *   **THX Systems:** Recommends a viewing angle of **36°** (up to 40°) for immersive cinematic content.
        *   *Calculation:* Distance is derived using the screen width and the tangent of the desired angle.
        
        **2. Mounting Height (Vertical)**
        *   **Ergonomic Standard:** Aligns the center of the screen with eye level (0° vertical angle) to prevent neck strain.
        *   **KEF Formula:** Adds a 12.4° vertical offset (`Distance * 0.22`) for reclined home theater seating.
        """)

if __name__ == "__main__":
    main()
