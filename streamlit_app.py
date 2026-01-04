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
    """
    Generates a side-view diagram of the TV setup (Vertical/Side Profile).
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # --- SETUP CANVAS ---
    ax.set_xlim(-50, dist_cm + 100)
    # Dynamic ceiling height
    room_height = max(250, tv_bottom_cm + tv_height_cm + 50)
    ax.set_ylim(0, room_height)
    ax.set_aspect('equal')
    ax.axis('off')

    # --- DRAW ROOM ---
    # Floor
    ax.axhline(y=0, color=COLOR_BLACK, linewidth=2) 
    # Wall
    ax.axvline(x=0, color=COLOR_LIGHT_BLUE, linewidth=4)
    
    # --- DRAW TV ---
    tv_thickness = 5 
    tv_rect = patches.Rectangle(
        (0, tv_bottom_cm), 
        tv_thickness, 
        tv_height_cm, 
        linewidth=1, 
        edgecolor=COLOR_BLACK, 
        facecolor=COLOR_DARK_BLUE
    )
    ax.add_patch(tv_rect)
    ax.text(-15, tv_centre_cm, "TV", ha='right', va='center', fontsize=12, fontweight='bold', color=COLOR_DARK_BLUE)

    # --- DRAW VIEWER (Human) ---
    # Head
    ax.scatter(dist_cm, eye_level_cm, s=200, color=COLOR_BLACK, zorder=5)
    # Body (Stick figure)
    ax.plot([dist_cm, dist_cm], [eye_level_cm, eye_level_cm - 60], color=COLOR_BLACK, linewidth=3) # Spine
    ax.plot([dist_cm, dist_cm - 20], [eye_level_cm - 30, eye_level_cm - 60], color=COLOR_BLACK, linewidth=3) # Legs
    ax.text(dist_cm, eye_level_cm + 25, "Eye Level", ha='center', fontsize=10, color=COLOR_BLACK)

    # --- DRAW GUIDES ---
    
    # 1. Horizontal Eye Line (0 degrees)
    ax.plot([0, dist_cm], [eye_level_cm, eye_level_cm], color='gray', linestyle='--', alpha=0.4)
    
    # 2. Sight Line
    ax.plot([0, dist_cm], [tv_centre_cm, eye_level_cm], color=COLOR_MED_BLUE, linestyle='--', alpha=0.8, linewidth=1.5)
    
    # 3. Vertical Angle Arc
    arc_diam = dist_cm * 0.4
    angle_patch = patches.Arc(
        (dist_cm, eye_level_cm), 
        width=arc_diam, 
        height=arc_diam, 
        angle=0, 
        theta1=180-vert_angle_deg, 
        theta2=180, 
        color=COLOR_RED, 
        linewidth=2
    )
    ax.add_patch(angle_patch)
    
    # Angle Label (Vertical)
    label_x = dist_cm - (arc_diam/2 * 1.15 * math.cos(math.radians(vert_angle_deg/2)))
    label_y = eye_level_cm + (arc_diam/2 * 1.15 * math.sin(math.radians(vert_angle_deg/2)))
    ax.text(label_x, label_y, f"{vert_angle_deg:.1f}°", color=COLOR_RED, fontsize=9, fontweight='bold', ha='center')

    # 4. Mounting Height Indicator
    ax.plot([20, 20], [0, tv_bottom_cm], color=COLOR_MED_BLUE, linestyle='-', linewidth=1)
    ax.text(35, tv_bottom_cm / 2, f"{tv_bottom_cm:.1f} cm", color=COLOR_MED_BLUE, va='center', fontweight='bold')
    ax.plot([0, 35], [tv_bottom_cm, tv_bottom_cm], color=COLOR_MED_BLUE, linewidth=0.5)

    # 5. Distance Indicator
    ax.plot([0, dist_cm], [10, 10], color='gray', linestyle='-')
    ax.text(dist_cm / 2, 25, f"{dist_cm/100:.2f} m", ha='center', color='gray')

    ax.set_title("Room Side View (Vertical Profile)", fontsize=10, loc='left', color=COLOR_DARK_BLUE)

    return fig

def main():
    st.set_page_config(page_title="Ideal TV Height Calculator", page_icon="📺")
    
    st.title("📺 Ideal TV Height Calculator")
    st.markdown(
        """
        Calculate the ideal mounting height and viewing distance.  
        Implements **SMPTE/THX** standards for distance and **KEF formulas** for height.
        """
    )
    
    st.divider()

    # --- INPUTS ---
    st.header("1. Your Setup")
    col1, col2 = st.columns(2)
    
    with col1:
        tv_size_inch = st.number_input("TV Size (Diagonal inches)", 32, 120, 65, step=1, format="%d")

    with col2:
        eye_level_cm = st.number_input(
            "Eye Level Height (cm)", 
            min_value=50.0, 
            max_value=150.0, 
            value=92.0, 
            step=1.0,
            help="Measure from the floor to your eyes while seated in your normal viewing position."
        )

    # --- VIEWING ANGLE STANDARDS (HORIZONTAL) ---
    st.subheader("Viewing Standard (Horizontal Field of View)")
    
    angle_help = """
    **30° (SMPTE):** Standard recommendation for mixed usage (Movies, TV, Sports).  
    **36° (THX):** Recommended for a more immersive, cinema-like experience.  
    **40°:** Limit recommended for pure cinema immersion (Screen fills most of your vision).
    """
    
    angle_standard = st.radio(
        "Select your preferred immersion level:",
        options=[30, 36, 40],
        format_func=lambda x: f"{x}° ({'SMPTE Standard' if x==30 else 'THX Recommended' if x==36 else 'Cinema Limit'})",
        horizontal=True,
        help=angle_help
    )
    
    # --- MATH: SCREEN DIMENSIONS (16:9) ---
    screen_width_inch = tv_size_inch * 0.87157
    screen_height_inch = tv_size_inch * 0.4903
    screen_width_cm = screen_width_inch * 2.54
    screen_height_cm = screen_height_inch * 2.54

    # --- MATH: RECOMMENDED DISTANCE ---
    # Distance = (Width / 2) / tan(Angle / 2)
    angle_rad = math.radians(angle_standard)
    rec_dist_inches = (screen_width_inch / 2) / math.tan(angle_rad / 2)
    rec_dist_m = (rec_dist_inches * 2.54) / 100
    
    # --- DISTANCE OVERRIDE ---
    st.write("") 
    use_manual_dist = st.checkbox("I sit at a different distance")
    
    if use_manual_dist:
        manual_dist_m = st.number_input("Your Actual Viewing Distance (meters)", 0.5, 10.0, 3.6, step=0.1)
        final_dist_m = manual_dist_m
        dist_source_label = "Your Distance"
    else:
        final_dist_m = rec_dist_m
        dist_source_label = f"Recommended Distance"

    # --- CALCULATIONS: HEIGHT ---
    final_dist_cm = final_dist_m * 100
    
    # KEF Formula: EL + (VD * 0.22) = TVH
    tv_centre_height_cm = eye_level_cm + (final_dist_cm * 0.22)
    tv_bottom_height_cm = tv_centre_height_cm - (screen_height_cm / 2)
    
    # Vertical Angle
    vert_angle_rad = math.atan(0.22)
    vert_angle_deg = math.degrees(vert_angle_rad)

    # --- CALCULATIONS: ACTUAL HORIZONTAL ANGLE ---
    act_horiz_angle_rad = 2 * math.atan((screen_width_cm / 2) / final_dist_cm)
    act_horiz_angle_deg = math.degrees(act_horiz_angle_rad)

    st.divider()

    # --- RESULTS ---
    st.header("2. Results")
    
    # Row 1: Primary Metrics
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.info(f"**{dist_source_label}**\n\n# {final_dist_m:.2f} m")
    with r1_col2:
        st.success(f"**Height to Bottom of TV**\n\n# {tv_bottom_height_cm:.1f} cm")
        
    # Row 2: Secondary Metrics (Angles) - Perfectly Aligned
    r2_col1, r2_col2 = st.columns(2)
    
    with r2_col1:
        # Check delta
        delta_val = None
        delta_color = "normal"
        if use_manual_dist:
            diff = act_horiz_angle_deg - angle_standard
            delta_val = f"{diff:.1f}° vs Target"
            # If diff is negative (further away), standard metric colors it red (down).
            # If positive (closer), green (up).
            
        st.metric(
            label="Horizontal Viewing Angle (Width)", 
            value=f"{act_horiz_angle_deg:.1f}°",
            delta=delta_val,
            help="The angle the screen width occupies in your field of vision. SMPTE recommends 30°."
        )

    with r2_col2:
        st.metric(
            label="Vertical Mounting Angle (Height)", 
            value=f"{vert_angle_deg:.1f}°", 
            help="The angle you look UP to see the center of the screen. KEF recommends ~12.4° for a reclined position."
        )

    if tv_bottom_height_cm > 100:
        st.warning(
            "⚠️ **Note on Height:** This result may seem high compared to standard TV stands. "
            "This formula assumes a **home theatre reclined posture** (looking up). "
            "For a standard upright living room setup, consider mounting 15-20cm lower."
        )

    # --- DIAGRAM ---
    st.divider()
    st.subheader("Side View (Vertical Layout)")
    fig = draw_diagram(
        dist_cm=final_dist_cm,
        eye_level_cm=eye_level_cm,
        tv_bottom_cm=tv_bottom_height_cm,
        tv_height_cm=screen_height_cm,
        tv_centre_cm=tv_centre_height_cm,
        vert_angle_deg=vert_angle_deg
    )
    st.pyplot(fig, use_container_width=True)

    # --- DETAILS ---
    with st.expander("See Calculation Breakdown"):
        st.markdown(f"""
        ### 1. Distance (Horizontal FOV)
        *   **Standard:** {angle_standard}° ({'SMPTE' if angle_standard==30 else 'THX'})
        *   **TV Width:** {screen_width_cm:.1f} cm
        *   **Formula:** $Distance = \\frac{{Width}}{{2 \\cdot \\tan(Angle/2)}}$
        
        ### 2. Height (Vertical Angle)
        *   **Eye Level:** {eye_level_cm} cm
        *   **Formula:** $Centre = EL + (Distance \\times 0.22)$
        *   **Result:** The $0.22$ factor calculates a {vert_angle_deg:.1f}° upward angle for comfortable reclined viewing.
        """)

if __name__ == "__main__":
    main()
