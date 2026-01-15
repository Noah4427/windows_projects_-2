import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_transistor(ax, x, y, type='nmos', label=''):
    """Draws a simplified transistor symbol."""
    # Gate
    ax.add_patch(patches.Rectangle((x, y-0.4), 0.2, 0.8, fill=False, edgecolor='black', lw=2))
    # Source/Drain line
    ax.plot([x+0.2, x+0.2], [y-0.6, y+0.6], 'k-', lw=2)
    # Source terminal
    ax.plot([x+0.2, x+0.5], [y+0.6, y+0.6], 'k-', lw=2)
    # Drain terminal
    ax.plot([x+0.2, x+0.5], [y-0.6, y-0.6], 'k-', lw=2)
    # Gate terminal
    ax.plot([x-0.2, x], [y, y], 'k-', lw=2)
    
    # PMOS circle
    if type == 'pmos':
        circle = patches.Circle((x-0.1, y), 0.08, fill=False, edgecolor='black', lw=2)
        ax.add_patch(circle)

    # Label
    ax.text(x-0.3, y, label, ha='right', va='center', fontsize=12)

def draw_schematic():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(-2, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Rails
    ax.plot([-1, 11], [9, 9], 'k-', lw=3)
    ax.text(11.2, 9, 'VDD', va='center', fontsize=12, fontweight='bold')
    ax.plot([-1, 11], [1, 1], 'k-', lw=3)
    ax.text(11.2, 1, 'VSS', va='center', fontsize=12, fontweight='bold')

    # --- Inverters ---
    # Inverter A
    ax.text(0.5, 9.5, 'Inverter A', ha='center', fontsize=12)
    draw_transistor(ax, 0.5, 7.5, 'pmos', 'A') # PMOS
    draw_transistor(ax, 0.5, 2.5, 'nmos', 'A') # NMOS
    # Connections Inv A
    ax.plot([0.5+0.5, 0.5+0.5], [9, 8.1], 'k-') # VDD to PMOS
    ax.plot([0.5+0.5, 0.5+0.5], [1, 1.9], 'k-') # VSS to NMOS
    ax.plot([0.5+0.5, 0.5+0.5], [6.9, 3.1], 'k-') # PMOS to NMOS drain
    ax.plot([0.5+0.5, 1.5], [5, 5], 'k-') # Output !A
    ax.text(1.6, 5, '!A', va='center', fontsize=12)
    # Input A
    ax.plot([-0.5, 0.3], [7.5, 7.5], 'k-') # Gate connection
    ax.plot([-0.5, 0.3], [2.5, 2.5], 'k-')
    ax.plot([-0.5, -0.5], [2.5, 7.5], 'k-')
    ax.text(-0.8, 5, 'Input A', va='center', fontsize=12)

    # Inverter B
    ax.text(3, 9.5, 'Inverter B', ha='center', fontsize=12)
    draw_transistor(ax, 3, 7.5, 'pmos', 'B') # PMOS
    draw_transistor(ax, 3, 2.5, 'nmos', 'B') # NMOS
    # Connections Inv B
    ax.plot([3+0.5, 3+0.5], [9, 8.1], 'k-')
    ax.plot([3+0.5, 3+0.5], [1, 1.9], 'k-')
    ax.plot([3+0.5, 3+0.5], [6.9, 3.1], 'k-')
    ax.plot([3+0.5, 4], [5, 5], 'k-') # Output !B
    ax.text(4.1, 5, '!B', va='center', fontsize=12)
    # Input B
    ax.plot([2, 2.8], [7.5, 7.5], 'k-')
    ax.plot([2, 2.8], [2.5, 2.5], 'k-')
    ax.plot([2, 2], [2.5, 7.5], 'k-')
    ax.text(1.7, 5, 'Input B', ha='right', va='center', fontsize=12)

    # --- XOR PUN ---
    # Branch 1: A series !B
    draw_transistor(ax, 6, 8, 'pmos', 'A')
    draw_transistor(ax, 6, 6.5, 'pmos', '!B')
    # Branch 2: !A series B
    draw_transistor(ax, 9, 8, 'pmos', '!A')
    draw_transistor(ax, 9, 6.5, 'pmos', 'B')
    
    # PUN Connections
    ax.plot([6.5, 6.5], [9, 8.6], 'k-') # VDD to Branch 1
    ax.plot([9.5, 9.5], [9, 8.6], 'k-') # VDD to Branch 2
    ax.plot([6.5, 6.5], [7.4, 7.1], 'k-') # Series connect Branch 1
    ax.plot([9.5, 9.5], [7.4, 7.1], 'k-') # Series connect Branch 2
    
    # --- XOR PDN ---
    # Branch 1: A series B
    draw_transistor(ax, 6, 3.5, 'nmos', 'A')
    draw_transistor(ax, 6, 2, 'nmos', 'B')
    # Branch 2: !A series !B
    draw_transistor(ax, 9, 3.5, 'nmos', '!A')
    draw_transistor(ax, 9, 2, 'nmos', '!B')

    # PDN Connections
    ax.plot([6.5, 6.5], [1, 1.4], 'k-') # VSS to Branch 1
    ax.plot([9.5, 9.5], [1, 1.4], 'k-') # VSS to Branch 2
    ax.plot([6.5, 6.5], [2.6, 2.9], 'k-') # Series connect Branch 1
    ax.plot([9.5, 9.5], [2.6, 2.9], 'k-') # Series connect Branch 2

    # --- Output Connections ---
    # Connect PUNs to common point
    ax.plot([6.5, 6.5], [5.9, 5], 'k-')
    ax.plot([9.5, 9.5], [5.9, 5], 'k-')
    # Connect PDNs to common point
    ax.plot([6.5, 6.5], [4.1, 5], 'k-')
    ax.plot([9.5, 9.5], [4.1, 5], 'k-')
    # Horizontal output line
    ax.plot([6.5, 10.5], [5, 5], 'k-')
    ax.text(10.6, 5, 'EOR OUT', fontweight='bold', fontsize=12)

    plt.title('12-Transistor CMOS EOR (XOR) Circuit Schematic', fontsize=16)
    plt.savefig('xor_schematic.png')
    plt.show()

draw_schematic()