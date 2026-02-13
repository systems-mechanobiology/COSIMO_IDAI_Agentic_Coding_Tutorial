import matplotlib.pyplot as plt
import numpy as np

# Use XKCD style for hand-drawn look
with plt.xkcd():
    fig, ax = plt.subplots(figsize=(8, 6))

    # Remove spines
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Set axis limits
    plt.xlim(0, 100)
    plt.ylim(0, 100)

    # Label axes
    plt.xlabel('Speed of Research')
    plt.ylabel('Robustness & Reproducibility')

    # Generate curves for Pareto fronts
    x = np.linspace(10, 90, 100)
    
    # Traditional Workflow (lower capability)
    # y = k/x shape roughly
    y_traditional = 100 - x - (1000/(x+20)) + 15
    # Let's just make convex curves manually for better control
    # Lower curve: (20, 80) -> (50, 50) -> (80, 20)
    t = np.linspace(0, np.pi/2, 100)
    x_trad = 90 - 70*np.sin(t)
    y_trad = 90 - 70*np.cos(t)
    
    # AI-Augmented Workflow (higher capability)
    # Shifted outwards
    x_ai = 110 - 70*np.sin(t)
    y_ai = 110 - 70*np.cos(t)
    
    # Plot curves
    plt.plot(x_trad, y_trad, 'orange', label='Traditional Workflow', lw=3)
    plt.plot(x_ai, y_ai, 'cornflowerblue', label='AI-Augmented Science', lw=3)

    # Add text labels on the plot lines themselves? Or use legend?
    # Let's put text directly on the plot for better readability
    plt.text(25, 30, 'Traditional\nWorkflow', color='orange', fontsize=12, ha='center')
    plt.text(65, 75, 'AI-Augmented\nScience', color='cornflowerblue', fontsize=12, ha='center')

    # Draw arrow indicating improvement
    # From (40, 40) on Trad to (60, 60) on AI?
    # Let's find close points.
    # Trad roughly passes (45, 45). AI roughly passes (65, 65).
    plt.annotate('Better Pareto Front', xy=(65, 60), xytext=(35, 35),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'),
                fontsize=12)

    # Remove ticks
    plt.xticks([])
    plt.yticks([])
    
    # Title
    plt.title('The Goal: Expanding the Frontier', fontsize=16)

    # Save figure
    plt.savefig('slides/assets/pareto_front.png', dpi=300, bbox_inches='tight', transparent=True)
    print("Figure saved to slides/assets/pareto_front.png")
