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
    Generates a side-view diagram of the TV setup.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # --- SETUP CANVAS ---
    ax.set_xlim(-50, dist_cm + 100)
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

    # --- DRAW VIEWER ---
    ax.scatter(dist_cm, eye_level_cm, s=200, color=COLOR_BLACK, zorder=5)
    # Body
    ax.plot([dist_cm, dist_cm], [eye_level_cm, eye_level_cm - 60], color=COLOR_BLACK, linewidth=3)
    ax.plot([dist_cm, dist_cm - 20], [eye_level_cm - 30, eye_level_cm - 60], color=COLOR_BLACK, linewidth=3)
    ax.text(dist_cm, eye_level_cm + 25, "Eye Level", ha='center', fontsize=10, color=COLOR_BLACK)

    # --- DRAW GUIDES ---
    
    # 1. Horizontal Eye Line
    ax.plot([0, dist_cm], [eye_level_cm, eye_level_cm], color='gray', linestyle='--', alpha=0.4)
    
    # 2. Sight Line
    ax.plot([0, dist_cm], [tv_centre_cm, eye_level_cm], color=COLOR_MED_BLUE, linestyle='--', alpha=0.8, linewidth=1.5)
    
    # 3. Vertical Angle Arc (Only if angle > 0.5 degrees)
    if vert_angle_deg > 0.5:
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
        
        # Angle Label
        label_x = dist_cm - (arc_diam/2 * 1.15 * math.cos(math.radians(vert_angle_deg/2)))
        label_y = eye_level_cm + (arc_diam/2 * 1.15 * math.sin(math.radians(vert_angle_deg/2)))
        ax.text(label_x, label_y, f"{vert_angle_deg:.1f}°", color=COLOR_RED, fontsize=9, fontweight='bold', ha='center')
    else:
        # If standard (0 degrees), text sits right on the line
        ax.text(dist_cm/2, eye_level_cm + 5, "0° (Neutral Neck)", color='gray', fontsize=8, ha='center')

    # 4. Mounting Height Indicator
    ax.plot([20, 20], [0, tv_bottom_cm], color=COLOR_MED_BLUE, linestyle='-', linewidth=1)
    ax.text(35, tv_bottom_cm / 2, f"{tv_bottom_cm:.1f} cm", color=COLOR_MED_BLUE, va='center', fontweight='bold')
    ax.plot([0, 35], [tv_bottom_cm, tv_bottom_cm], color=COLOR_MED_BLUE, linewidth=0.5)

    # 5. Distance Indicator
    ax.plot([0, dist_cm], [10, 10], color='gray', linestyle='-')
    ax.text(dist_cm / 2, 25, f"{dist_cm/100:.2f} m", ha='center', color='gray')

    ax.set_title(f"Side View", fontsize=10, loc='left', color=COLOR_DARK_BLUE)

    return fig

def main():
    st.set_page_config(page_title="Ideal TV Height Calculator", page_icon="📺")
    
    st.title("📺 Ideal TV Height Calculator")
    st.markdown("Calculate the ideal mounting height for your living room setup.")
    
    st.divider()

    # --- SECTION 1: PREFERENCES ---
    st.header("1. Your Setup")
    
    # Setup Mode Selector
    setup_mode = st.radio(
        "Setup Style",
        ["Standard Living Room (Ergonomic)", "Home Theater (Reclined)"],
        help="**Standard:** TV Center aligns with Eye Level (Neutral neck). Best for couches.\n\n**Home Theater:** TV mounted higher to look up (like a cinema). Best for recliners."
    )

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
            help="Measure from floor to eyes while seated. Standard couch height is usually 90-100cm."
        )

    # --- SECTION 2: VIEWING ANGLE ---
    st.subheader("Field of View (Horizontal)")
    
    angle_help = """
    **30° (SMPTE):** The standard for mixed use (TV, Sports, Gaming).  
    **36° (THX):** Recommended for movies.  
    **40°:** Cinema limit.
    """
    
    angle_standard = st.radio(
        "Select your preferred immersion:",
        options=[30, 36, 40],
        format_func=lambda x: f"{x}° ({'SMPTE Standard' if x==30 else 'THX Recommended' if x==36 else 'Cinema Limit'})",
        horizontal=True,
        help=angle_help
    )

    # --- CALCULATIONS ---
    # Screen Math
    screen_width_inch = tv_size_inch * 0.87157
    screen_height_inch = tv_size_inch * 0.4903
    screen_width_cm = screen_width_inch * 2.54
    screen_height_cm = screen_height_inch * 2.54

    # Distance Math (Horizontal Angle)
    angle_rad = math.radians(angle_standard)
    rec_dist_inches = (screen_width_inch / 2) / math.tan(angle_rad / 2)
    rec_dist_m = (rec_dist_inches * 2.54) / 100
    
    # Distance Input
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

    # --- HEIGHT LOGIC BRANCH ---
    if setup_mode == "Standard Living Room (Ergonomic)":
        # Ergonomic Standard: Center of TV = Eye Level
        tv_centre_height_cm = eye_level_cm
        vert_angle_deg = 0.0
        mode_note = "Standard mode aligns the TV center directly with your eyes."
    else:
        # KEF / Theater Mode: Center = EL + (VD * 0.22)
        tv_centre_height_cm = eye_level_cm + (final_dist_cm * 0.22)
        vert_angle_rad = math.atan(0.22)
        vert_angle_deg = math.degrees(vert_angle_rad)
        mode_note = "Theater mode lifts the TV ~12° for a reclined viewing angle."

    tv_bottom_height_cm = tv_centre_height_cm - (screen_height_cm / 2)
    
    # Calculate Actual Horizontal Angle
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
        
    # Row 2: Secondary Metrics (Angles)
    r2_col1, r2_col2 = st.columns(2)
    
    with r2_col1:
        delta_val = None
        if use_manual_dist:
             delta_val = f"{act_horiz_angle_deg - angle_standard:.1f}° vs Target"
             
        st.metric(
            label="Horizontal Viewing Angle (Width)", 
            value=f"{act_horiz_angle_deg:.1f}°",
            delta=delta_val,
            help="How much of your field of view is filled by the screen width."
        )

    with r2_col2:
        st.metric(
            label="Vertical Mounting Angle (Height)", 
            value=f"{vert_angle_deg:.1f}°", 
            help="The angle you look UP to see the center. 0° is neutral (straight ahead)."
        )

    st.caption(f"ℹ️ {mode_note}")

    # --- DIAGRAM ---
    st.divider()
    st.subheader("Side View")
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
        st.markdown(f"### 1. Distance Calculation")
        st.write(f"*Targeting {angle_standard}° Horizontal Field of View.*")
        st.latex(r"Distance = \frac{\text{Width}}{2 \cdot \tan(\text{Angle}/2)}")
        
        st.markdown(f"### 2. Height Calculation ({setup_mode})")
        st.write(f"**Eye Level:** {eye_level_cm} cm")
        st.write(f"**Screen Height:** {screen_height_cm:.1f} cm")
        
        if setup_mode == "Standard Living Room (Ergonomic)":
            st.write("**Formula:** $Centre = EyeLevel$")
            st.write("This places the center of the screen exactly at your neutral gaze.")
        else:
            st.write("**Formula:** $Centre = EyeLevel + (Distance \\times 0.22)$")
            st.write("This places the center higher to account for leaning back.")
            
        st.markdown("**Final Step:**")
        st.latex(r"Bottom = Centre - (\text{TV Height} / 2)")
        st.code(f"{tv_centre_height_cm:.1f} - {screen_height_cm/2:.1f} = {tv_bottom_height_cm:.1f} cm")

if __name__ == "__main__":
    main()
