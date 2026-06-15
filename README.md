# Rainmeter Google Doodle Widget

![Google Doodle Widget Preview](preview.gif) <!-- TODO: Add a real preview GIF or screenshot here and name it preview.gif -->

The **Google Doodle Rainmeter Widget** is a Rainmeter skin that automatically fetches and animates the daily Google Doodle directly on your desktop!

## Features

* **Automated Daily Fetching:** A lightweight Python script silently runs in the background to scrape the official Google Doodle archive and download today's animated GIF.
* **Smart Auto-Cropping & Spritesheets:** The script seamlessly converts the GIF into a mathematically precise vertical spritesheet, bypassing Rainmeter's standard GIF limitations.
* **0% Disk I/O & GPU Acceleration:** Utilizes Rainmeter's native `Bitmap` meter with `BitmapExtend=1` and `Shape` caching. The image is loaded directly into GPU RAM once, meaning absolutely zero disk polling or CPU bottlenecks during animation.
* **Dynamic Framerate Math:** Automatically calculates the optimal Rainmeter `UpdateDivider` based on the native framerate of the daily GIF. It perfectly limits useless calculation cycles to save battery while preserving flawless frame-sync.
* **Intelligent Hardware Freeze:** Includes a built-in `UsageMonitor` that tracks your CPU, GPU, and Physical Disk. If your system exceeds 60% load (e.g. launching a game or rendering a video), the animation instantly freezes to yield 100% of your PC's power back to you.
* **Smart Refresh Delay:** Automatically checks for a new doodle every 3 hours (doodles can change in the middle of the day to alternate versions) and at exactly midnight. However, if your system is currently under heavy load, the refresh is safely queued and will *only* execute after your PC has dropped below 60% load for 3 uninterrupted seconds.
* **Interactive Tooltips:** Hovering over the doodle displays the official title of the daily event, and clicking it takes you directly to the Google Search results for the doodle!

## Requirements
* **[Rainmeter](https://www.rainmeter.net/)**
* **Python 3.x**
  * To verify you have python installed open a terminal and run `python --version` and `pip --version`. If both commands return a version number you are good to go, otherwise install python.
  * After installing python install the required background scraping engine:
    ```cmd
    pip install playwright
    playwright install chromium
    ```
* **ImageMagick**
  * Install the latest version natively via Winget:
    ```cmd
    winget install ImageMagick.ImageMagick
    ```
  * *(Scoop also has a slightly older version of ImageMagick if you don't like winget)*

## Installation
1. Open your terminal and navigate to your Rainmeter Skins folder:
   ```cmd
   cd %USERPROFILE%\Documents\Rainmeter\Skins\
   ```
2. Either download this repository as a `.zip` and extract it here, or clone it via git:
   ```cmd
   git clone https://github.com/chleved/Google-Doodle.git
   ```
   **Important:** Ensure your final folder structure looks exactly like this:
   ```text
   ...\Documents\Rainmeter\Skins\GoogleDoodle\
   │   GoogleDoodle.ini
   │   FetchDoodle.py
   │   README.md
   ```
3. **RESTART:** If Rainmeter was running while you installed Python or ImageMagick, you must exit Rainmeter (right-click the teardrop icon in your system tray -> Exit) and relaunch it. Otherwise, Rainmeter will not recognize the new commands.
4. Open Rainmeter and load the `GoogleDoodle.ini` skin!

## Customizing the Framerate
The skin is optimized to display the doodle at ~60 FPS (using an internal 16ms update tick) to perfectly sync with high-quality doodles. However, you can easily reduce this to save performance.

To modify the framerate, open `GoogleDoodle.ini` and locate the two update variables at the very top of the file:
1. Under `[Rainmeter]`, change `Update`
2. Under `[Variables]`, change `SkinUpdate`

**IMPORTANT:** Both of these values *must* have the same value for the animation math to correctly track real-world time.

**Example configurations:**
* **60 FPS (Default):** Set both to `16`
* **30 FPS:** Set both to `32`
* **15 FPS:** Set both to `64` *(Most doodles are drawn at this framerate)*
* **8 FPS:** Set both to `128` *

No matter what framerate you choose, the widget's internal math will skip frames to ensure that the displayed doodle animation runs for the same time as the original gif.

## TBD

1. Conversion from ms to fps for variables
2. Variable to modify doodle duration (1.1x, 0.7x, 300 ms, 3 s)
3. Variable to modify load threshold for freezing
4. Improve load detection logic
5. Refine installation and requirements section for dummies
