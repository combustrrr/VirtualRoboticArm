"""
Interactive Matplotlib Arm - Matplotlib interface
Interactive workspace analysis and visualization using Matplotlib
"""
import sys
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider
    import matplotlib.patches as patches
    from mpl_toolkits.mplot3d import Axes3D
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not installed.")
    print("To install: pip install matplotlib")


def main():
    """Main function for Interactive Matplotlib Arm"""
    print("=" * 60)
    print("INTERACTIVE MATPLOTLIB ARM")
    print("=" * 60)
    print("Interactive workspace analysis and visualization")
    print()
    
    if not MATPLOTLIB_AVAILABLE:
        print("❌ Matplotlib not available")
        print("Please install: pip install matplotlib")
        return
    
    print("📊 Matplotlib Features:")
    print("- Interactive workspace analysis")
    print("- Real-time joint control with sliders")
    print("- Reachable area mapping")
    print("- 2D and 3D visualization modes")
    print("- Joint configuration studies")
    print()
    
    print("🎮 Controls:")
    print("- Use sliders to control joint angles")
    print("- Real-time visualization updates")
    print("- Workspace boundary analysis")
    print("- Forward kinematics demonstration")
    print()
    
    print("🔧 Implementation Status:")
    print("Creating interactive Matplotlib demonstration...")
    print()
    
    # Create interactive demonstration
    create_interactive_demo()


def create_interactive_demo():
    """Create interactive Matplotlib demonstration"""
    if not MATPLOTLIB_AVAILABLE:
        return
    
    print("🎬 Creating interactive Matplotlib demo...")
    print("📊 Use the sliders to control the robotic arm!")
    
    # Set up the figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # 2D view
    ax_2d = plt.subplot(2, 2, 1)
    ax_2d.set_title('🚜 JCB Arm - Side View (2D)')
    ax_2d.set_xlabel('X (meters)')
    ax_2d.set_ylabel('Z (meters)')
    ax_2d.grid(True, alpha=0.3)
    ax_2d.set_aspect('equal')
    
    # 3D view
    ax_3d = plt.subplot(2, 2, 2, projection='3d')
    ax_3d.set_title('🚜 JCB Arm - 3D View')
    ax_3d.set_xlabel('X (meters)')
    ax_3d.set_ylabel('Y (meters)')
    ax_3d.set_zlabel('Z (meters)')
    
    # Workspace analysis
    ax_workspace = plt.subplot(2, 2, 3)
    ax_workspace.set_title('📊 Workspace Analysis')
    ax_workspace.set_xlabel('X (meters)')
    ax_workspace.set_ylabel('Z (meters)')
    ax_workspace.grid(True, alpha=0.3)
    
    # Joint angles display
    ax_joints = plt.subplot(2, 2, 4)
    ax_joints.set_title('🎮 Joint Configuration')
    ax_joints.axis('off')
    
    # Adjust layout to make room for sliders
    plt.subplots_adjust(bottom=0.25)
    
    # Arm parameters
    arm_params = {
        'base_height': 2.0,
        'boom_length': 4.0,
        'stick_length': 3.0,
        'bucket_length': 1.5
    }
    
    # Initial joint angles
    initial_angles = {
        'base': 0,
        'boom': -30,
        'stick': 45,
        'bucket': -15
    }
    
    # Create sliders
    sliders = create_sliders(fig, initial_angles, arm_params, ax_2d, ax_3d, ax_workspace, ax_joints)
    
    # Initial plot
    update_arm_visualization(initial_angles, arm_params, ax_2d, ax_3d, ax_workspace, ax_joints)
    
    print("📊 Interactive demo created! Adjust sliders to control the arm.")
    plt.show()


def create_sliders(fig, initial_angles, arm_params, ax_2d, ax_3d, ax_workspace, ax_joints):
    """Create interactive sliders for joint control"""
    sliders = {}
    
    # Slider positions
    slider_configs = [
        ('base', 0.1, 0.15, -180, 180, '°'),
        ('boom', 0.1, 0.10, -90, 45, '°'),
        ('stick', 0.1, 0.05, -135, 45, '°'),
        ('bucket', 0.1, 0.00, -120, 60, '°')
    ]
    
    for name, x, y, min_val, max_val, unit in slider_configs:
        ax_slider = plt.axes([x, y, 0.3, 0.03])
        slider = Slider(
            ax_slider, 
            f'{name.title()} {unit}', 
            min_val, 
            max_val, 
            valinit=initial_angles[name],
            valfmt='%d'
        )
        
        # Add callback
        slider.on_changed(lambda val, s=name: update_callback(
            sliders, arm_params, ax_2d, ax_3d, ax_workspace, ax_joints
        ))
        
        sliders[name] = slider
    
    return sliders


def update_callback(sliders, arm_params, ax_2d, ax_3d, ax_workspace, ax_joints):
    """Callback function for slider updates"""
    # Get current angles from sliders
    angles = {name: slider.val for name, slider in sliders.items()}
    
    # Update visualization
    update_arm_visualization(angles, arm_params, ax_2d, ax_3d, ax_workspace, ax_joints)


def update_arm_visualization(angles, arm_params, ax_2d, ax_3d, ax_workspace, ax_joints):
    """Update all arm visualizations"""
    # Clear axes
    ax_2d.clear()
    ax_3d.clear()
    ax_workspace.clear()
    ax_joints.clear()
    
    # Calculate arm positions
    positions = calculate_arm_positions(angles, arm_params)
    
    # Update 2D view
    plot_2d_arm(ax_2d, positions, angles, arm_params)
    
    # Update 3D view
    plot_3d_arm(ax_3d, positions, angles, arm_params)
    
    # Update workspace analysis
    plot_workspace_analysis(ax_workspace, arm_params)
    
    # Update joint display
    plot_joint_info(ax_joints, angles)
    
    # Refresh display
    plt.draw()


def calculate_arm_positions(angles, arm_params):
    """Calculate arm joint positions from angles"""
    base_angle = np.radians(angles['base'])
    boom_angle = np.radians(angles['boom'])
    stick_angle = np.radians(angles['stick'])
    bucket_angle = np.radians(angles['bucket'])
    
    positions = []
    
    # Base
    base_pos = np.array([0, 0, arm_params['base_height']])
    positions.append(base_pos)
    
    # Boom end
    boom_end = base_pos + np.array([
        arm_params['boom_length'] * np.cos(boom_angle) * np.cos(base_angle),
        arm_params['boom_length'] * np.cos(boom_angle) * np.sin(base_angle),
        arm_params['boom_length'] * np.sin(boom_angle)
    ])
    positions.append(boom_end)
    
    # Stick end
    total_boom_stick = boom_angle + stick_angle
    stick_end = boom_end + np.array([
        arm_params['stick_length'] * np.cos(total_boom_stick) * np.cos(base_angle),
        arm_params['stick_length'] * np.cos(total_boom_stick) * np.sin(base_angle),
        arm_params['stick_length'] * np.sin(total_boom_stick)
    ])
    positions.append(stick_end)
    
    # Bucket end
    total_angle = boom_angle + stick_angle + bucket_angle
    bucket_end = stick_end + np.array([
        arm_params['bucket_length'] * np.cos(total_angle) * np.cos(base_angle),
        arm_params['bucket_length'] * np.cos(total_angle) * np.sin(base_angle),
        arm_params['bucket_length'] * np.sin(total_angle)
    ])
    positions.append(bucket_end)
    
    return positions


def plot_2d_arm(ax, positions, angles, arm_params):
    """Plot 2D side view of the arm"""
    # Project to XZ plane
    x_coords = [pos[0] for pos in positions]
    z_coords = [pos[2] for pos in positions]
    
    ax.plot(x_coords, z_coords, 'o-', linewidth=6, markersize=10, 
            color='orange', label='JCB Arm')
    ax.plot([0], [0], 's', markersize=15, color='gray', label='Base')
    
    ax.set_title('🚜 JCB Arm - Side View (2D)')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Z (meters)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')
    
    # Set limits
    max_reach = sum([arm_params['boom_length'], arm_params['stick_length'], arm_params['bucket_length']])
    ax.set_xlim([-max_reach*1.1, max_reach*1.1])
    ax.set_ylim([-max_reach*0.5, max_reach*1.1])


def plot_3d_arm(ax, positions, angles, arm_params):
    """Plot 3D view of the arm"""
    x_coords = [pos[0] for pos in positions]
    y_coords = [pos[1] for pos in positions]
    z_coords = [pos[2] for pos in positions]
    
    ax.plot(x_coords, y_coords, z_coords, 'o-', linewidth=6, markersize=8, 
            color='orange', label='JCB Arm')
    ax.scatter([0], [0], [0], s=200, c='gray', marker='s', label='Base')
    
    ax.set_title('🚜 JCB Arm - 3D View')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')
    ax.legend()
    
    # Set equal aspect ratio
    max_reach = sum([arm_params['boom_length'], arm_params['stick_length'], arm_params['bucket_length']])
    ax.set_xlim([-max_reach, max_reach])
    ax.set_ylim([-max_reach, max_reach])
    ax.set_zlim([0, max_reach])


def plot_workspace_analysis(ax, arm_params):
    """Plot workspace analysis"""
    # Calculate reachable area (simplified)
    max_reach = sum([arm_params['boom_length'], arm_params['stick_length'], arm_params['bucket_length']])
    min_reach = abs(arm_params['boom_length'] - arm_params['stick_length'] - arm_params['bucket_length'])
    
    # Draw workspace boundaries
    theta = np.linspace(0, 2*np.pi, 100)
    max_circle_x = max_reach * np.cos(theta)
    max_circle_z = max_reach * np.sin(theta) + arm_params['base_height']
    min_circle_x = min_reach * np.cos(theta)
    min_circle_z = min_reach * np.sin(theta) + arm_params['base_height']
    
    ax.fill_between(max_circle_x, max_circle_z, alpha=0.3, color='green', label='Reachable Area')
    ax.fill_between(min_circle_x, min_circle_z, alpha=0.3, color='white')
    
    ax.set_title('📊 Workspace Analysis')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Z (meters)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')


def plot_joint_info(ax, angles):
    """Display joint angle information"""
    ax.text(0.1, 0.8, '🎮 Current Joint Angles:', fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    y_positions = [0.6, 0.5, 0.4, 0.3]
    for i, (joint, angle) in enumerate(angles.items()):
        ax.text(0.1, y_positions[i], f'{joint.title()}: {angle:.1f}°', 
                fontsize=12, transform=ax.transAxes)
    
    # Add specifications
    ax.text(0.1, 0.1, '🚜 JCB Specifications:\n• Max Reach: 8.0m\n• Max Dig Depth: 6.2m\n• Bucket Capacity: 1.2m³', 
            fontsize=10, transform=ax.transAxes)
    
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.axis('off')


if __name__ == "__main__":
    main()