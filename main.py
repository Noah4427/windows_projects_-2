import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_transistor(ax, x, y, type='nmos', label='', gate_label=''):
    """
    Draws a simplified transistor symbol with precise alignment.
    x, y: Center coordinates of the channel/gate area.
    """
    # Dimensions
    w = 0.6  # Width of channel line
    h = 0.8  # Height of source/drain vertical lines
    
    # Gate Plate (Vertical line)
    ax.plot([x, x], [y - h/2, y + h/2], 'k-', lw=2)
    
    # Channel Plate (Vertical line offset)
    channel_x = x + 0.2
    ax.plot([channel_x, channel_x], [y - h/2, y + h/2], 'k-', lw=2)
    
    # Source/Drain Terminals (Horizontal then Vertical)
    # Upper terminal
    ax.plot([channel_x, channel_x + 0.3], [y + h/2, y + h/2], 'k-', lw=2) 
    # Lower terminal
    ax.plot([channel_x, channel_x + 0.3], [y - h/2, y - h/2], 'k-', lw=2) 
    
    # Gate Terminal (Input)
    ax.plot([x - 0.3, x], [y, y], 'k-', lw=2)
    
    # PMOS Bubble
    if type == 'pmos':
        circle = patches.Circle((x - 0.15, y), 0.08, fill=False, edgecolor='black', lw=1.5)
        ax.add_patch(circle)
        # Clean up the line behind the bubble
        ax.plot([x - 0.5, x - 0.23], [y, y], 'k-', lw=2)
    else:
        ax.plot([x - 0.5, x], [y, y], 'k-', lw=2)

    # Labels
    if gate_label:
        # Signal name next to the gate
        ax.text(x - 0.6, y, gate_label, ha='right', va='center', fontsize=11, fontfamily='monospace')

def draw_schematic_v2():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(-1, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # --- Global Rails ---
    # VDD
    ax.plot([0, 13], [10, 10], 'k-', lw=3)
    ax.text(13.2, 10, 'VDD', va='center', fontsize=14, fontweight='bold')
    # VSS
    ax.plot([0, 13], [1, 1], 'k-', lw=3)
    ax.text(13.2, 1, 'VSS', va='center', fontsize=14, fontweight='bold')

    # ==========================================
    # STAGE 1: INVERTERS (Left Side)
    # ==========================================
    
    # --- Inverter A ---
    inv_a_x = 2
    ax.text(inv_a_x + 0.2, 10.5, 'INV A', ha='center', fontsize=12, fontweight='bold')
    
    draw_transistor(ax, inv_a_x, 8.5, 'pmos', gate_label='A')
    draw_transistor(ax, inv_a_x, 3.5, 'nmos', gate_label='A')
    
    # Connections
    ax.plot([inv_a_x + 0.5, inv_a_x + 0.5], [10, 8.9], 'k-', lw=2) # VDD to PMOS
    ax.plot([inv_a_x + 0.5, inv_a_x + 0.5], [8.1, 3.9], 'k-', lw=2) # PMOS to NMOS
    ax.plot([inv_a_x + 0.5, inv_a_x + 0.5], [3.1, 1], 'k-', lw=2) # NMOS to VSS
    
    # Input A (Gate tie)
    ax.plot([inv_a_x - 0.5, inv_a_x - 0.5], [8.5, 3.5], 'k-', lw=2) 
    ax.plot([inv_a_x - 1.0, inv_a_x - 0.5], [6, 6], 'k-', lw=2)    
    ax.text(inv_a_x - 1.1, 6, 'A_in', ha='right', va='center', fontsize=12)

    # Output node !A
    ax.plot([inv_a_x + 0.5, inv_a_x + 1.2], [6, 6], 'k-', lw=2)
    ax.add_patch(patches.Circle((inv_a_x + 0.5, 6), 0.08, color='black')) 
    ax.text(inv_a_x + 0.8, 6.2, '!A', fontsize=11, color='blue')

    # --- Inverter B ---
    inv_b_x = 5
    ax.text(inv_b_x + 0.2, 10.5, 'INV B', ha='center', fontsize=12, fontweight='bold')

    draw_transistor(ax, inv_b_x, 8.5, 'pmos', gate_label='B')
    draw_transistor(ax, inv_b_x, 3.5, 'nmos', gate_label='B')

    # Connections
    ax.plot([inv_b_x + 0.5, inv_b_x + 0.5], [10, 8.9], 'k-', lw=2)
    ax.plot([inv_b_x + 0.5, inv_b_x + 0.5], [8.1, 3.9], 'k-', lw=2)
    ax.plot([inv_b_x + 0.5, inv_b_x + 0.5], [3.1, 1], 'k-', lw=2)

    # Input B (Gate tie)
    ax.plot([inv_b_x - 0.5, inv_b_x - 0.5], [8.5, 3.5], 'k-', lw=2)
    ax.plot([inv_b_x - 1.0, inv_b_x - 0.5], [6, 6], 'k-', lw=2)
    ax.text(inv_b_x - 1.1, 6, 'B_in', ha='right', va='center', fontsize=12)

    # Output node !B
    ax.plot([inv_b_x + 0.5, inv_b_x + 1.2], [6, 6], 'k-', lw=2)
    ax.add_patch(patches.Circle((inv_b_x + 0.5, 6), 0.08, color='black'))
    ax.text(inv_b_x + 0.8, 6.2, '!B', fontsize=11, color='blue')

    # ==========================================
    # STAGE 2: XOR CORE (Right Side)
    # ==========================================
    
    # PUN (Pull Up Network) - Two parallel branches of 2 series PMOS
    # Branch 1 (Left): A series !B
    pun_x1 = 8
    draw_transistor(ax, pun_x1, 9.0, 'pmos', gate_label='A')
    draw_transistor(ax, pun_x1, 7.5, 'pmos', gate_label='!B')
    
    # Branch 2 (Right): !A series B
    pun_x2 = 11
    draw_transistor(ax, pun_x2, 9.0, 'pmos', gate_label='!A')
    draw_transistor(ax, pun_x2, 7.5, 'pmos', gate_label='B')
    
    # PDN (Pull Down Network) - Two parallel branches of 2 series NMOS
    # Branch 1 (Left): A series B
    pdn_x1 = 8
    draw_transistor(ax, pdn_x1, 3.5, 'nmos', gate_label='A')
    draw_transistor(ax, pdn_x1, 2.0, 'nmos', gate_label='B')
    
    # Branch 2 (Right): !A series !B
    pdn_x2 = 11
    draw_transistor(ax, pdn_x2, 3.5, 'nmos', gate_label='!A')
    draw_transistor(ax, pdn_x2, 2.0, 'nmos', gate_label='!B')

    # --- Connections for XOR Core ---
    
    # PUN Top connections (to VDD)
    ax.plot([pun_x1 + 0.5, pun_x1 + 0.5], [10, 9.4], 'k-', lw=2)
    ax.plot([pun_x2 + 0.5, pun_x2 + 0.5], [10, 9.4], 'k-', lw=2)
    
    # PUN Inter-transistor connections (Series)
    ax.plot([pun_x1 + 0.5, pun_x1 + 0.5], [8.6, 7.9], 'k-', lw=2)
    ax.plot([pun_x2 + 0.5, pun_x2 + 0.5], [8.6, 7.9], 'k-', lw=2)
    
    # PDN Bottom connections (to VSS)
    ax.plot([pdn_x1 + 0.5, pdn_x1 + 0.5], [1.6, 1], 'k-', lw=2)
    ax.plot([pdn_x2 + 0.5, pdn_x2 + 0.5], [1.6, 1], 'k-', lw=2)
    
    # PDN Inter-transistor connections (Series)
    ax.plot([pdn_x1 + 0.5, pdn_x1 + 0.5], [3.1, 2.4], 'k-', lw=2)
    ax.plot([pdn_x2 + 0.5, pdn_x2 + 0.5], [3.1, 2.4], 'k-', lw=2)

    # OUTPUT NODE COMBINATION
    # Connect PUN bottoms
    ax.plot([pun_x1 + 0.5, pun_x1 + 0.5], [7.1, 5.5], 'k-', lw=2)
    ax.plot([pun_x2 + 0.5, pun_x2 + 0.5], [7.1, 5.5], 'k-', lw=2)
    
    # Connect PDN tops
    ax.plot([pdn_x1 + 0.5, pdn_x1 + 0.5], [3.9, 5.5], 'k-', lw=2)
    ax.plot([pdn_x2 + 0.5, pdn_x2 + 0.5], [3.9, 5.5], 'k-', lw=2)
    
    # Horizontal bar connecting left and right branches
    ax.plot([pun_x1 + 0.5, pun_x2 + 0.5], [5.5, 5.5], 'k-', lw=2)
    # Solder dots
    ax.add_patch(patches.Circle((pun_x1 + 0.5, 5.5), 0.08, color='black'))
    ax.add_patch(patches.Circle((pun_x2 + 0.5, 5.5), 0.08, color='black'))
    
    # Final Output Line
    ax.plot([pun_x2 + 0.5, 13], [5.5, 5.5], 'k-', lw=2)
    ax.text(13.2, 5.5, 'EOR\nOUT', va='center', fontsize=12, fontweight='bold', color='red')

    plt.title('12-Transistor CMOS EOR (XOR) Circuit Schematic', fontsize=16, pad=20)
    plt.savefig('xor_schematic_v2.png')
    plt.show()

draw_schematic_v2()