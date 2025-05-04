# Linear Regression: Least Squares vs. Gradient Descent

This Python script demonstrates and compares two fundamental methods for performing simple linear regression: the analytical Least Squares Method (LSM) and the iterative Gradient Descent algorithm. It generates synthetic data, applies both methods to find the best-fit line, and visualizes the results.

## How it Works

### 1. Data Generation

-   Synthetic data points (`x`, `y`) are generated to loosely follow a predefined linear relationship.
-   `numpy.random.rand` is used to create `x` values.
-   Corresponding `y` values are calculated based on the predefined line equation, with Gaussian noise added using `numpy.random.randn` to simulate real-world data scatter.
-   The original `k_orig` and `b_orig` values (slope and intercept) are stored for later comparison.

### 2. Least Squares Method (LSM)

-   **Principle:** LSM aims to find the line parameters (`k`, `b`) that minimize the sum of the squared differences (residuals) between the observed `y` values and the values predicted by the linear model.
-   **Implementation (`least_squares_fit` function):**
    -   Calculates the necessary sums from the input data (`x_data`, `y_data`).
    -   Applies the analytical formulas derived from calculus to find the optimal `k` and `b` that minimize the squared error based on these sums and the number of data points.
-   **NumPy Comparison:** The results from the custom `least_squares_fit` function are compared against NumPy's built-in `numpy.polyfit(x, y, 1)` function, which also uses LSM for polynomial fitting (degree 1 for a straight line).

### 3. Gradient Descent

-   **Principle:** Gradient Descent is an iterative optimization algorithm used to find the minimum of a function (in this case, the Mean Squared Error loss function). It starts with initial guesses for `k` and `b` and repeatedly adjusts them in the direction opposite to the gradient of the loss function.
-   **Implementation (`gradient_descent` function):**
    -   Initializes `k` and `b` (typically to 0).
    -   Iterates a predefined number of times (`n_iter`):
        1.  **Predict:** Calculates the predicted `y` values using the current `k` and `b`.
        2.  **Calculate Loss:** Computes the Mean Squared Error (MSE) between predicted and actual `y` values. The MSE history is stored.
        3.  **Calculate Gradients:** Computes the partial derivatives (the gradients) of the MSE loss function with respect to `k` and `b`.
        4.  **Update Parameters:** Adjusts `k` and `b` using the calculated gradients and the `learning_rate`.
-   **Hyperparameters:** The `learning_rate` determines the step size in each iteration, and `n_iter` defines how many steps are taken. These need careful tuning.

### 4. Visualization & Comparison

-   **Regression Lines Plot:** `matplotlib` is used to create a scatter plot of the generated data points. The original line (if generated) and the regression lines found by the custom LSM function, `numpy.polyfit`, and Gradient Descent are overlaid for visual comparison.
-   **MSE Plot:** A separate plot shows the decrease in the Mean Squared Error (MSE) over the iterations of the Gradient Descent algorithm, illustrating its convergence towards a minimum.
-   **Parameter Comparison:** The script prints a summary table comparing the original `k` and `b` values with those estimated by the custom LSM function, `numpy.polyfit`, and Gradient Descent.

## Dependencies

-   `numpy`
-   `matplotlib`

## How to Run

1.  Make sure you have the required dependencies installed (`pip install numpy matplotlib`).
2.  Run the script using a Python interpreter (`python your_script_name.py`).
3.  The script will print the calculated parameters from each method and display two plots: one showing the data and the regression lines, and another showing the MSE convergence for Gradient Descent.
