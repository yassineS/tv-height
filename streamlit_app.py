import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def draw_diagram(dist_cm, eye_level_cm, tv_bottom_cm, tv_height_cm, tv_centre_cm, angle_deg):
    """
    Generates a side-view diagram of the TV setup with angle visualization.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # --- SETUP CANVAS ---
    ax.set_xlim(-50, dist_cm + 100)
    # Dynamic ceiling height, ensure we have room above TV
    room_height = max(250, tv_bottom_cm + tv_height_cm + 50)
    ax.set_ylim(0, room_height)
    ax.set_aspect('equal')
    ax.axis('off')

    # --- DRAW ROOM ---
    # Floor
    ax.axhline(y=0, color='black', linewidth=2)
    # Wall
    ax.axvline(x=0, color='gray', linewidth=4)
    
    # --- DRAW TV ---
    tv_thickness = 5 
    tv_rect = patches.Rectangle(
        (0, tv_bottom_cm), 
        tv_thickness, 
        tv_height_cm, 
        linewidth=1, 
        edgecolor='black', 
        facecolor='#2c3e50'
    )
    ax.add_patch(tv_rect)
    ax.text(-15, tv_centre_cm, "TV", ha='right', va='center', fontsize=12, fontweight='bold')

    # --- DRAW VIEWER ---
    ax.scatter(dist_cm, eye_level_cm, s=200, color='#e74c3c', zorder=5) # Head
    # Simple body
    ax.plot([dist_cm, dist_cm], [eye_level_cm, eye_level_cm - 60], color='#e74c3c', linewidth=2)
    ax.plot([dist_cm, dist_cm - 20], [eye_level_cm - 30, eye_level_cm - 60], color='#e74c3c', linewidth=2)
    ax.text(dist_cm, eye_level_cm + 20, "Eye Level", ha='center', fontsize=10)

    # --- DRAW GUIDES ---
    
    # 1. Horizontal Eye Line (The "0 degree" reference)
    ax.plot([0, dist_cm], [eye_level_cm, eye_level_cm], color='gray', linestyle='--', alpha=0.3)
    
    # 2. Sight Line (Eye to Center)
    ax.plot([0, dist_cm], [tv_centre_cm, eye_level_cm], color='#3498db', linestyle='--', alpha=0.8)
    
    # 3. Angle Arc
    # We are looking left (towards negative x). Horizontal is 180 deg in matplotlib.
    # The TV is UP, so the angle is < 180 (e.g. 167 deg).
    # Arc should span from (180 - angle) to 180.
    arc_diam = dist_cm * 0.4 # Make arc size proportional to distance
    angle_patch = patches.Arc(
        (dist_cm, eye_level_cm), 
        width=arc_diam, 
        height=arc_diam, 
        angle=0, 
        theta1=180-angle_deg, 
        theta2=180, 
        color='#e67e22', 
        linewidth=2
    )
    ax.add_patch(angle_patch)
    
    # Angle Label
    # Position it slightly offset from the viewer along the angle bisector
    label_x = dist_cm - (arc_diam/2 * 1.1 * math.cos(math.radians(angle_deg/2)))
    label_y = eye_level_cm + (arc_diam/2 * 1.1 * math.sin(math.radians(angle_deg/2)))
    ax.text(label_x, label_y, f"{angle_deg:.1f}°", color='#e67e22', fontsize=10, fontweight='bold')

    # 4. Mounting Height Indicator
    ax.plot([20, 20], [0, tv_bottom_cm], color='green', linestyle='-', linewidth=1)
    ax.text(30, tv_bottom_cm / 2, f"{tv_bottom_cm:.1f} cm", color='green', va='center', fontweight='bold')
    ax.plot([0, 30], [tv_bottom_cm, tv_bottom_cm], color='green', linewidth=0.5)

    # 5. Distance Indicator
    ax.plot([0, dist_cm], [10, 10], color='gray', linestyle='-')
    ax.text(dist_cm / 2, 25, f"{dist_cm/100:.2f} m", ha='center', color='gray')

    ax.set_title("Room Side View", fontsize=10, loc='left')

    return fig

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

    # --- INPUTS ---
    st.header("1. Your Setup")
    col1, col2 = st.columns(2)
    
    with col1:
        tv_size_inch = st.number_input("TV Size (Diagonal inches)", 32, 120, 65, step=1, format="%d")

    with col2:
        eye_level_cm = st.number_input("Eye Level Height (cm)", 50.0, 150.0, 92.0, step=1.0)

    # --- DISTANCE ---
    rec_dist_inches = tv_size_inch * 1.67
    rec_dist_m = (rec_dist_inches * 2.54) / 100
    
    st.write("") 
    use_manual_dist = st.checkbox("I sit at a specific distance (Override recommendation)")
    
    if use_manual_dist:
        manual_dist_m = st.number_input("Your Actual Viewing Distance (meters)", 0.5, 10.0, 3.6, step=0.1)
        final_dist_m = manual_dist_m
        dist_source_label = "Your Distance"
        st.caption(f"ℹ️ *Note: The standard recommended distance for this TV size is {rec_dist_m:.2f}m.*")
    else:
        final_dist_m = rec_dist_m
        dist_source_label = "Recommended Distance"

    # --- CALCULATIONS ---
    final_dist_cm = final_dist_m * 100
    
    # 1. Height Calculation (The core KEF formula)
    # TVH = EL + (VD * 0.22)
    tv_centre_height_cm = eye_level_cm + (final_dist_cm * 0.22)
    
    # 2. Angle Calculation
    # The factor 0.22 represents tan(theta)
    # theta = arctan(0.22)
    angle_rad = math.atan(0.22)
    angle_deg = math.degrees(angle_rad)
    
    # 3. Screen Dimensions (16:9)
    screen_height_inch = tv_size_inch * 0.4903
    screen_height_cm = screen_height_inch * 2.54
    tv_bottom_height_cm = tv_centre_height_cm - (screen_height_cm / 2)

    st.divider()

    # --- RESULTS ---
    st.header("2. Results")
    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.info(f"**{dist_source_label}**\n\n# {final_dist_m:.2f} m")

    with res_col2:
        st.success(f"**Height to Bottom of TV**\n\n# {tv_bottom_height_cm:.1f} cm")
        st.caption(f"Height to Centre: {tv_centre_height_cm:.1f} cm")
    
    # --- DIAGRAM ---
    st.divider()
    st.subheader("Visual Guide")
    fig = draw_diagram(
        dist_cm=final_dist_cm,
        eye_level_cm=eye_level_cm,
        tv_bottom_cm=tv_bottom_height_cm,
        tv_height_cm=screen_height_cm,
        tv_centre_cm=tv_centre_height_cm,
        angle_deg=angle_deg
    )
    st.pyplot(fig, use_container_width=True)

    # --- DETAILS ---
    with st.expander("See Calculation Breakdown"):
        st.markdown("### The Math")
        st.write("The formula assumes a specific comfortable viewing angle:")
        st.latex(r"\text{Vertical Angle} = \arctan(0.22) \approx " + f"{angle_deg:.1f}" + r"^\circ")
        
        st.markdown("This angle is used to determine how much higher the TV center should be relative to your eyes.")
        st.latex(r"Height_{offset} = Distance \times \tan(" + f"{angle_deg:.1f}" + r"^\circ)")
        st.code(f"{final_dist_cm:.1f} * 0.22 = {final_dist_cm * 0.22:.1f} cm (Height above eye level)")
        
        st.markdown("**Final Steps:**")
        st.write(f"1. Add Eye Level: {eye_level_cm} + {final_dist_cm * 0.22:.1f} = **{tv_centre_height_cm:.1f} cm (Centre)**")
        st.write(f"2. Subtract Half Screen: {tv_centre_height_cm:.1f} - {screen_height_cm/2:.1f} = **{tv_bottom_height_cm:.1f} cm (Bottom)**")

if __name__ == "__main__":
    main()
