# Interactive Signal Filtering Demo

This Python script demonstrates the concepts of generating a harmonic signal (sine wave), adding random noise to it, and then filtering the noisy signal using a digital low-pass filter. The script uses `matplotlib` widgets to allow interactive control over signal, noise, and filter parameters.

## How it Works

### 1. Clean Signal Generation

-   A "clean" base signal, a perfect sine wave, is generated first.
-   This is done using the formula: `y_clean = amp * np.sin(freq * t + ph)`
    -   `amp`: Amplitude (wave height), controlled by the "Amplitude" slider.
    -   `freq`: Frequency (how fast the wave oscillates), controlled by the "Frequency" slider.
    * `t`: A time vector (`np.linspace(0, 2 * np.pi, 1000)`), representing the X-axis.
    * `ph`: Phase (initial shift of the wave), controlled by the "Phase" slider.
-   This `y_clean` represents the ideal signal without any interference, displayed as a dashed line ('--').

### 2. Noise Generation and Addition

-   **Noise Generation:** Noise is created in the `gen_noise(mean, std)` function using `np.random.normal(mean, std, size=t.shape)`.
    -   `np.random.normal`: This NumPy function generates random numbers following a *normal (Gaussian) distribution*. This is a common way to model random noise found in many natural and technical systems.
    -   `mean` (μ): The average value of the noise. Determines if the noise has a constant offset up or down. Controlled by the "Noise μ" slider (typically 0 for simple noise).
    -   `std` (σ): The **standard deviation** of the noise. This is the crucial parameter determining the "strength" or "spread" of the noise. A larger `std` means greater random deviations from the mean, resulting in a "noisier" signal. Controlled by the "Noise σ" slider.
    * `size=t.shape`: Ensures the noise array has the exact same length (number of points) as the time vector `t` and the clean signal `y_clean`.
-   **Noise Addition:** The generated noise is added to the clean signal element-wise: `y_noisy = y_clean + noise`.
    -   Each value from the generated random noise array is added to the corresponding value of the clean sine wave.
    -   So, at a time point `t[i]`, if the clean signal is `y_clean[i]` and the noise is `noise[i]`, the noisy signal becomes `y_noisy[i] = y_clean[i] + noise[i]`.
-   **Noise Display Control:** The "Show Noise" checkbox (`check`) controls whether this generated `noise` array is actually added to `y_clean` when calculating the signal to display (`y = y_clean + noise if show else y_clean`). If unchecked, `y` will simply be equal to `y_clean`.

### 3. Signal Filtering

-   **Purpose:** The goal here is to remove the high-frequency noise while preserving the lower-frequency useful signal (the sine wave). A *low-pass filter* is used for this.
-   **Filter Design:** The filter is designed using the `create_filter(order, cutoff)` function, which calls `scipy.signal.iirfilter(order, cutoff, btype='low', ftype='butter')`.
    -   `iirfilter`: A function to design digital IIR (Infinite Impulse Response) filters.
    -   `order`: The **filter order**. This determines how "sharp" the transition is between frequencies that are passed and those that are attenuated. A higher order gives a sharper cutoff but can be more computationally intensive or have other undesired effects. Controlled by the "Filter Order" slider.
    -   `cutoff`: The **cutoff frequency**. This is the frequency below which the signal is passed largely unchanged, and above which it is significantly attenuated (filtered out). The `cutoff` value here is normalized (typically 0 to 1, where 1 corresponds to half the sampling frequency). Since the main signal (sine wave) has a low frequency (controlled by the "Frequency" slider) and the noise typically contains many high-frequency components, the `cutoff` can be chosen to be higher than the sine wave's frequency but lower than most of the noise frequencies. Controlled by the "Cutoff" slider.
    * `btype='low'`: Specifies that a low-pass filter is needed.
    * `ftype='butter'`: The type of filter - Butterworth. Known for having a maximally flat response in the passband (i.e., it doesn't distort the signal's amplitude below the `cutoff` frequency).
    * The function returns coefficients `b` and `a`, which mathematically describe the filter.
-   **Filter Application:** The filter is applied to the (usually noisy) signal `y` using the `filter_signal(x)` function, which calls `scipy.signal.filtfilt(b, a, x)`.
    -   `filtfilt`: This function applies the designed filter (with coefficients `b`, `a`) to the input signal `x`. Importantly, `filtfilt` applies the filter *twice*: once forward and then once backward. This is done to **cancel out the phase shift** introduced by standard IIR filters. As a result, the filtered signal `y_filt` has zero phase distortion relative to the original signal, which is very useful for visual comparison.
-   **Result:** The `line_filtered` plot shows the output of the filter (`y_filt`). If the filter parameters (order and cutoff) are well-chosen, this plot will be much smoother than the noisy `line_noisy` and closer to the clean `line_clean`.

## Interactivity

-   **Sliders:** Allow real-time adjustment of:
    -   Sine wave parameters: Amplitude, Frequency, Phase.
    -   Noise parameters: Mean (μ), Standard Deviation (σ).
    -   Filter parameters: Order, Cutoff Frequency.
-   **Checkbox:** Toggles the addition of noise to the clean signal.
-   **Update Function:** Any change in a slider or the checkbox triggers the `update` function, which recalculates the noise (if noise parameters changed), the clean signal, the noisy signal (if applicable), applies the filter, and redraws the plot.
-   **Reset Button:** Resets all parameters to their initial values.

## Dependencies

-   `numpy`
-   `matplotlib`
-   `scipy`

## How to Run

1.  Make sure you have the required dependencies installed (`pip install numpy matplotlib scipy`).
2.  Make sure you have the TkAgg backend installed (`pip install tk`).
3.  Run the script as a regular Python file or in the Pycharm interpreter (which is what it was tested on).
4.  You will see a full Matplotlib window with interactive sliders, a button, and a checkbox.
5.  Change the parameters below the graph to adjust the harmonics and noise.
6.  Use the "Reset" button to return to the original settings.
