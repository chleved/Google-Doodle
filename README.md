# Rainmeter Google Doodle Widget

A highly-optimized, dynamic Rainmeter skin that automatically fetches and animates the daily Google Doodle directly on your desktop!

## Features

* **Automated Daily Fetching:** A lightweight Python script silently runs in the background to scrape the official Google Doodle archive and download today's animated GIF.
* **Smart Auto-Cropping & Spritesheets:** The script seamlessly converts the GIF into a mathematically precise vertical spritesheet, bypassing Rainmeter's standard GIF limitations.
* **0% Disk I/O & GPU Acceleration:** Utilizes Rainmeter's native `Bitmap` meter with `BitmapExtend=1` and `Shape` caching. The image is loaded directly into GPU RAM once, meaning absolutely zero disk polling or CPU bottlenecks during animation.
* **Dynamic Framerate Math:** Automatically calculates the optimal Rainmeter `UpdateDivider` based on the native framerate of the daily GIF. It perfectly limits useless calculation cycles to save battery while preserving flawless frame-sync.
* **Intelligent Hardware Freeze:** Includes a built-in `UsageMonitor` that tracks your CPU, GPU, and Physical Disk. If your system exceeds 60% load (e.g. launching a game or rendering a video), the animation instantly freezes to yield 100% of your PC's power back to you.
* **Smart Refresh Delay:** Automatically checks for a new doodle every 3 hours and at exactly midnight. However, if your system is currently under heavy load, the refresh is safely queued and will *only* execute after your PC has dropped below 60% load for 3 uninterrupted seconds.
* **Interactive Tooltips:** Hovering over the doodle displays the official title of the daily event, and clicking it takes you directly to the Google Search results for the doodle!

## Requirements
* **[Rainmeter](https://www.rainmeter.net/)**
* **Python 3.x**
  * Open your terminal and install the required background scraping engine:
    ```cmd
    pip install playwright
    playwright install chromium
    ```
* **ImageMagick**
  * Install the latest version natively via Winget:
    ```cmd
    winget install ImageMagick.ImageMagick
    ```
  * *(Alternative for older Windows versions: `scoop install imagemagick`)*

## Installation
1. Open your terminal and navigate to your Rainmeter Skins folder:
   ```cmd
   cd %USERPROFILE%\Documents\Rainmeter\Skins\
   ```
2. Clone the repository directly into the folder:
   ```cmd
   git clone https://github.com/chleved/GoogleDoodle.git
   ```
3. Open Rainmeter, click "Refresh all" in the bottom left corner, and load the `GoogleDoodle.ini` skin!

## Customizing the Framerate
The skin is mathematically optimized to run at a buttery-smooth default of ~60 FPS (using an internal 16ms update tick) to perfectly sync with high-quality doodles. However, you can easily reduce this to save even more performance.

To modify the framerate, open `GoogleDoodle.ini` and locate the two update variables at the very top of the file:
1. Under `[Rainmeter]`, change `Update=16`
2. Under `[Variables]`, change `SkinUpdate=16`

**CRITICAL:** Both of these values *must* exactly match for the animation math to correctly track real-world time. If you desynchronize them, the doodle will play in slow-motion!

**Example configurations:**
* **60 FPS (Default):** Set both to `16` *(Smoothest animation)*
* **30 FPS:** Set both to `32` *(Balanced)*
* **15 FPS:** Set both to `64` *(Maximum performance)*
* **8 FPS:** Set both to `128` *(Ultra power-saving mode)*

No matter what framerate you choose, the widget's internal math will organically skip frames to ensure the 1-second GIF always plays out over exactly 1 second!
