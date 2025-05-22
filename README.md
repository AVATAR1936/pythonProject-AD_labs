# Processing Scenarios for Multispectral Satellite Imagery 

This project provides a Python-based solution, implemented in a Jupyter Notebook, for automating common processing workflows for multispectral satellite imagery. It is designed to handle data from both **Sentinel-2** and **Landsat-8** missions, covering steps from data acquisition to analysis. The primary goal is to demonstrate the use of the **GDAL library** and other geospatial tools in Python to perform complex data processing tasks in an automated script.

---

## How it Works

### 1. Data Acquisition and Preparation

The script begins by preparing the raw satellite data for processing. This can be done in two ways:

* **Local Archives**: The script automatically finds and unpacks raw data archives (`.zip` for Sentinel-2, `.tar.gz` for Landsat-8) located in the `sentinel_raw_data` and `landsat_raw_data` directories. Each archive is unpacked into a new folder corresponding to the product's identifier.
* **API Download (Sentinel-2 only)**: If enabled, the script can directly download Sentinel-2 imagery using the `sentinelhub-py` library. It sends a request for a specific, predefined Region of Interest (ROI) over Kyiv and a specified time interval.

### 2. Sentinel-2 Processing Workflow

For Sentinel-2 data, the script executes a sequential pipeline to produce a clean, analysis-ready image.

1.  **Band Concatenation**: The script identifies individual spectral bands within the complex `.SAFE` product structure. It then uses a process equivalent to `gdal_merge.py` with the `-separate` parameter to combine the Blue (B2), Green (B3), Red (B4), and Near-Infrared (B8) bands into a single 4-band GeoTIFF file.
2.  **Reprojection**: Each concatenated image is reprojected to the standard **EPSG:4326 (WGS 84)** coordinate system. This is handled by a function that wraps the `gdalwarp` command-line tool.
3.  **Mosaicking**: If multiple Sentinel-2 scenes are processed, they are merged into a single, seamless mosaic. This step ensures that images covering adjacent areas are combined correctly.
4.  **Clipping**: The final mosaicked image is clipped to a specific area of interest using a provided vector shapefile (e.g., `Kyiv_regions.shp`). This is achieved using `gdalwarp` with the `-cutline` and `-crop_to_cutline` parameters, which trims the raster to the exact boundaries of the vector polygon.

### 3. Landsat-8 Pansharpening Workflow

The second part of the script is dedicated to pansharpening Landsat-8 data to increase its spatial resolution.

* **Purpose**: Pansharpening combines the high spatial resolution of a panchromatic (single-band) image with the spectral information of a lower-resolution multispectral image to create a high-resolution color image.
* **Data Resampling**: To prepare for pansharpening, the script uses a function wrapping `gdal_translate` to perform two resampling steps:
    * The original 30-meter multispectral (RGB) bands are downsampled to 60 meters.
    * The original 15-meter panchromatic band is downsampled to 30 meters to serve as the high-resolution source.
* **Pansharpening Application**: The core of this workflow is the `gdal_pansharpen.py` tool. The script iteratively applies different fusion algorithms by changing the `-r` parameter (`-r {nearest, bilinear, cubic, ...}`). This generates multiple pansharpened 30-meter RGB images—one for each tested method.

### 4. Accuracy Assessment

To objectively evaluate the pansharpening results, the script compares the generated images to a ground truth.

* **Comparison**: The original 30-meter RGB image is used as the reference ("ground truth") against which each pansharpened 30-meter output is compared.
* **Metrics Calculation**: The script uses the `scikit-learn` library to calculate regression accuracy metrics. For each band in the images, it computes:
    * **R-squared ($R^2$)**: Measures how well the pansharpened pixel values predict the original pixel values.
    * **Mean Squared Error (MSE)**: The average of the squares of the errors.
    * **Mean Absolute Error (MAE)**: The average of the absolute errors.
* **Result**: The metrics are printed in a summary table, allowing for a quantitative comparison to determine the best-performing pansharpening algorithm for the given data.

---

## Dependencies

* `gdal`
* `rasterio`
* `sentinelhub-py`
* `scikit-learn`
* `matplotlib`
* `numpy`

---

## How to Run

### 1. Environment Setup

It is **highly recommended** to use a Python distribution via **Anaconda** or **Miniconda**. This approach is the simplest and avoids many common issues when installing complex geospatial libraries like GDAL.

```bash
# Create and activate a new conda environment
conda create --name geo_env python=3.9
conda activate geo_env

# Install dependencies
conda install -c conda-forge gdal rasterio sentinelhub scikit-learn matplotlib