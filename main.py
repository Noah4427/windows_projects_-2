import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_transistor(ax, x, y, type='nmos', gate_label='', color='black'):
    """ 
    Draws a transistor symbol and returns the location of its gate terminal (gx, gy).
    Handles PMOS bubbles and text labeling.
    """
    h = 0.8 # Height of the transistor
    
    # --- Draw Structure ---
    # Gate Plate (Vertical line)
    ax.plot([x, x], [y - h/2, y + h/2], 'k-', lw=2)
    
    # Channel Plate (Vertical line offset)
    channel_x = x + 0.2
    ax.plot([channel_x, channel_x], [y - h/2, y + h/2], 'k-', lw=2)
    
    # Source/Drain Terminals
    ax.plot([channel_x, channel_x + 0.3], [y + h/2, y + h/2], 'k-', lw=2) # Top terminal
    ax.plot([channel_x, channel_x + 0.3], [y - h/2, y - h/2], 'k-', lw=2) # Bottom terminal
    
    # Gate Terminal (Input wire stub)
    gate_x_start = x - 0.5
    ax.plot([gate_x_start, x], [y, y], 'k-', lw=2)
    
    # --- Type Specific Elements ---
    if type == 'pmos':
        # Bubble for PMOS
        circle = patches.Circle((x - 0.15, y), 0.08, fill=False, edgecolor='black', lw=1.5)
        ax.add_patch(circle)
        # Clean line behind bubble (aesthetic fix)
        ax.plot([gate_x_start, x - 0.23], [y, y], 'k-', lw=2)
        # Label PMOS
        ax.text(channel_x + 0.1, y + 0.5, 'PMOS', ha='left', va='bottom', fontsize=8, color='black')
    else:
        # Standard line for NMOS
        ax.plot([gate_x_start, x], [y, y], 'k-', lw=2)
        # Label NMOS
        ax.text(channel_x + 0.1, y + 0.5, 'NMOS', ha='left', va='bottom', fontsize=8, color='black')
    
    # --- Add Signal Label ---
    if gate_label:
        ax.text(gate_x_start - 0.1, y, gate_label, ha='right', va='center', fontsize=10, fontweight='bold', color=color)

    return (gate_x_start, y)

def draw_schematic_colored():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(-3, 16)
    ax.set_ylim(0, 12)
    ax.axis('off') # Hide axes
    
    # --- Color Definitions ---
    color_A = '#008000'   # Dark Green for Input A
    color_nA = '#32CD32'  # Lime Green for Signal !A
    color_B = '#0000FF'   # Blue for Input B
    color_nB = '#1E90FF'  # Light Blue for Signal !B

    # --- Draw Rails ---
    ax.plot([-1, 15], [11, 11], 'k-', lw=3)
    ax.text(15.2, 11, 'VDD', va='center', fontweight='bold', fontsize=14)
    ax.plot([-1, 15], [1, 1], 'k-', lw=3)
    ax.text(15.2, 1, 'VSS', va='center', fontweight='bold', fontsize=14)

    # Dictionary to store gate coordinates for wiring
    gates = {} 

    # ==========================
    # 1. INVERTERS (Left Side)
    # ==========================
    
    # --- Inverter A ---
    inv_a_x = 0
    gates['inv_a_p'] = draw_transistor(ax, inv_a_x, 9.5, 'pmos')
    gates['inv_a_n'] = draw_transistor(ax, inv_a_x, 2.5, 'nmos')
    # Connections
    ax.plot([inv_a_x+0.5, inv_a_x+0.5], [11, 9.9], 'k-', lw=2) # VDD to PMOS
    ax.plot([inv_a_x+0.5, inv_a_x+0.5], [9.1, 2.9], 'k-', lw=2) # PMOS to NMOS
    ax.plot([inv_a_x+0.5, inv_a_x+0.5], [2.1, 1], 'k-', lw=2)   # NMOS to VSS
    
    # Input A Wiring (Green)
    ax.plot([gates['inv_a_p'][0], gates['inv_a_p'][0]], [9.5, 2.5], '-', color=color_A, lw=2) # Gate tie
    ax.plot([-2, gates['inv_a_p'][0]], [6, 6], '-', color=color_A, lw=2) # Input Line
    ax.text(-2.2, 6, 'Input A', ha='right', va='center', fontweight='bold', color=color_A)
    
    # Output !A Node (Lime Green)
    node_notA = (inv_a_x + 0.5, 6.0)
    ax.add_patch(patches.Circle(node_notA, 0.1, color=color_nA))
    
    # --- Inverter B ---
    inv_b_x = 3
    gates['inv_b_p'] = draw_transistor(ax, inv_b_x, 9.5, 'pmos')
    gates['inv_b_n'] = draw_transistor(ax, inv_b_x, 2.5, 'nmos')
    # Connections
    ax.plot([inv_b_x+0.5, inv_b_x+0.5], [11, 9.9], 'k-', lw=2)
    ax.plot([inv_b_x+0.5, inv_b_x+0.5], [9.1, 2.9], 'k-', lw=2)
    ax.plot([inv_b_x+0.5, inv_b_x+0.5], [2.1, 1], 'k-', lw=2)

    # Input B Wiring (Blue)
    ax.plot([gates['inv_b_p'][0], gates['inv_b_p'][0]], [9.5, 2.5], '-', color=color_B, lw=2)
    ax.plot([-2, gates['inv_b_p'][0]], [5, 5], '-', color=color_B, lw=2) # Input Line
    ax.text(-2.2, 5, 'Input B', ha='right', va='center', fontweight='bold', color=color_B)
    
    # Output !B Node (Light Blue)
    node_notB = (inv_b_x + 0.5, 5.0)
    ax.add_patch(patches.Circle(node_notB, 0.1, color=color_nB))

    # ==========================
    # 2. XOR CORE (Right Side)
    # ==========================
    
    x_col1 = 9  # Left Branch
    x_col2 = 13 # Right Branch
    
    # --- Draw Gates & Labels ---
    # Branch 1 (Left)
    gates['pun_1_top'] = draw_transistor(ax, x_col1, 10.0, 'pmos', 'A', color_A)
    gates['pun_1_bot'] = draw_transistor(ax, x_col1, 8.5, 'pmos', '!B', color_nB)
    gates['pdn_1_top'] = draw_transistor(ax, x_col1, 3.5, 'nmos', 'A', color_A)
    gates['pdn_1_bot'] = draw_transistor(ax, x_col1, 2.0, 'nmos', 'B', color_B)

    # Branch 2 (Right)
    gates['pun_2_top'] = draw_transistor(ax, x_col2, 10.0, 'pmos', '!A', color_nA)
    gates['pun_2_bot'] = draw_transistor(ax, x_col2, 8.5, 'pmos', 'B', color_B)
    gates['pdn_2_top'] = draw_transistor(ax, x_col2, 3.5, 'nmos', '!A', color_nA)
    gates['pdn_2_bot'] = draw_transistor(ax, x_col2, 2.0, 'nmos', '!B', color_nB)

    # --- Vertical Structure (Series Logic) ---
    for x in [x_col1, x_col2]:
        ax.plot([x+0.5, x+0.5], [11, 10.4], 'k-', lw=2) # VDD to Top
        ax.plot([x+0.5, x+0.5], [9.6, 8.9], 'k-', lw=2) # Series PMOS
        ax.plot([x+0.5, x+0.5], [8.1, 6.0], 'k-', lw=2) # PMOS to Output
        ax.plot([x+0.5, x+0.5], [6.0, 3.9], 'k-', lw=2) # Output to NMOS
        ax.plot([x+0.5, x+0.5], [3.1, 2.4], 'k-', lw=2) # Series NMOS
        ax.plot([x+0.5, x+0.5], [1.6, 1], 'k-', lw=2)   # NMOS to VSS
    
    # --- Output Bridge (The Middle Connection) ---
    ax.plot([x_col1+0.5, x_col2+0.5], [6.0, 6.0], 'k-', lw=3)
    ax.add_patch(patches.Circle((x_col1+0.5, 6.0), 0.12, color='black')) # Solder dot Left
    ax.add_patch(patches.Circle((x_col2+0.5, 6.0), 0.12, color='black')) # Solder dot Right
    ax.plot([x_col2+0.5, 15], [6.0, 6.0], 'k-', lw=3) # Final Output Line
    ax.text(15.2, 6.0, 'EOR OUT', va='center', fontweight='bold', color='red', fontsize=12)

    # ==========================
    # 3. WIRING (Explicit Lines)
    # ==========================
    
    def connect_wire(start_xy, dest_name, color, style='-'):
        """ Draws a Manhattan-style wire from start to destination gate """
        dest_xy = gates[dest_name]
        # Route logic: Horizontal -> Vertical -> Horizontal
        # We step back -1.0 unit from the destination gate to create a "wire channel"
        ax.plot([start_xy[0], dest_xy[0]-1.0], [start_xy[1], start_xy[1]], style, color=color, lw=1.5)
        ax.plot([dest_xy[0]-1.0, dest_xy[0]-1.0], [start_xy[1], dest_xy[1]], style, color=color, lw=1.5)
        ax.plot([dest_xy[0]-1.0, dest_xy[0]], [dest_xy[1], dest_xy[1]], style, color=color, lw=1.5)
        # Solder dot at the start point
        ax.add_patch(patches.Circle((start_xy[0], start_xy[1]), 0.08, color=color))

    # --- Route Signal A (Green) ---
    # From Input A to PUN Left Top & PDN Left Top
    connect_wire((-1.5, 6), 'pun_1_top', color_A)
    connect_wire((-1.5, 6), 'pdn_1_top', color_A)

    # --- Route Signal !A (Lime Green) ---
    # From Inverter A Output to PUN Right Top & PDN Right Top
    connect_wire(node_notA, 'pun_2_top', color_nA, '--')
    connect_wire(node_notA, 'pdn_2_top', color_nA, '--')

    # --- Route Signal B (Blue) ---
    # From Input B to PUN Right Bot & PDN Left Bot
    connect_wire((-1.5, 5), 'pun_2_bot', color_B)
    connect_wire((-1.5, 5), 'pdn_1_bot', color_B)

    # --- Route Signal !B (Light Blue) ---
    # From Inverter B Output to PUN Left Bot & PDN Right Bot
    connect_wire(node_notB, 'pun_1_bot', color_nB, '--')
    connect_wire(node_notB, 'pdn_2_bot', color_nB, '--')

    # --- Legend ---
    ax.text(0, 0, 'Green = Signal A', color=color_A, fontsize=12, fontweight='bold')
    ax.text(5, 0, 'Lime = Signal !A', color=color_nA, fontsize=12, fontweight='bold')
    ax.text(0, -0.5, 'Blue = Signal B', color=color_B, fontsize=12, fontweight='bold')
    ax.text(5, -0.5, 'Sky = Signal !B', color=color_nB, fontsize=12, fontweight='bold')

    plt.title('12-Transistor CMOS XOR Schematic (Corrected Wiring)', fontsize=16, pad=20)
    plt.savefig('xor_schematic_final.png')
    plt.show()

# Run the function
draw_schematic_colored()