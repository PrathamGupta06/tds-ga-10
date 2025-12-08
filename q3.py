import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    # This notebook demonstrates interactive data analysis with variable dependencies
    # Import required libraries for data analysis and visualization
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # Email: 23f3004131@ds.study.iitm.ac.in
    email = "23f3004131@ds.study.iitm.ac.in"
    return mo, np, pd, plt, email


@app.cell
def __(mo):
    # Create an interactive slider widget to control sample size
    # This slider will be used to dynamically adjust the dataset size
    sample_size_slider = mo.ui.slider(
        start=50, stop=500, step=50, value=200, label="Sample Size"
    )
    sample_size_slider
    return (sample_size_slider,)


@app.cell
def __(np, pd, sample_size_slider):
    # Generate synthetic dataset based on slider value
    # This cell depends on the sample_size_slider widget
    # Data flow: slider value -> sample size -> dataset generation
    n_samples = sample_size_slider.value

    # Generate random data with a correlation structure
    np.random.seed(42)
    x_data = np.random.normal(50, 15, n_samples)
    # y has a linear relationship with x plus some noise
    y_data = 2.5 * x_data + np.random.normal(0, 20, n_samples)

    # Create a pandas DataFrame for easier manipulation
    df = pd.DataFrame({"Variable_X": x_data, "Variable_Y": y_data})

    # Calculate correlation coefficient
    correlation = df["Variable_X"].corr(df["Variable_Y"])

    return n_samples, x_data, y_data, df, correlation


@app.cell
def __(df, plt, n_samples, correlation):
    # Create visualization of the relationship between variables
    # This cell depends on df, n_samples, and correlation from the previous cell
    # Data flow: dataset -> visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["Variable_X"], df["Variable_Y"], alpha=0.6, edgecolors="k")
    ax.set_xlabel("Variable X", fontsize=12)
    ax.set_ylabel("Variable Y", fontsize=12)
    ax.set_title(
        f"Scatter Plot: X vs Y (n={n_samples}, r={correlation:.3f})", fontsize=14
    )
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    plot_output = fig
    return fig, ax, plot_output


@app.cell
def __(mo, n_samples, correlation, df, email):
    # Dynamic markdown output that changes based on widget state
    # This cell depends on n_samples, correlation, and df statistics
    # Data flow: computed statistics -> formatted markdown display

    mean_x = df["Variable_X"].mean()
    std_x = df["Variable_X"].std()
    mean_y = df["Variable_Y"].mean()
    std_y = df["Variable_Y"].std()

    # Interpret correlation strength
    if abs(correlation) > 0.7:
        strength = "strong"
    elif abs(correlation) > 0.4:
        strength = "moderate"
    else:
        strength = "weak"

    mo.md(f"""
    ## Analysis Summary
    
    **Author**: {email}
    
    **Dataset Statistics (Sample Size: {n_samples})**
    
    - **Variable X**: Mean = {mean_x:.2f}, Std Dev = {std_x:.2f}
    - **Variable Y**: Mean = {mean_y:.2f}, Std Dev = {std_y:.2f}
    - **Correlation**: {correlation:.3f} ({strength} positive relationship)
    
    ### Interpretation
    
    The data shows a **{strength}** positive correlation between Variable X and Variable Y.
    This suggests that as X increases, Y tends to {"increase significantly" if abs(correlation) > 0.7 else "increase moderately" if abs(correlation) > 0.4 else "show some increase"}.
    
    **Adjust the slider above to see how sample size affects the observed relationship!**
    """)
    return mean_x, std_x, mean_y, std_y, strength


@app.cell
def __(mo, plot_output):
    # Display the plot
    # This cell depends on the plot_output from the visualization cell
    mo.as_html(plot_output)
    return


if __name__ == "__main__":
    app.run()
