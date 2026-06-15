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
* [Rainmeter](https://www.rainmeter.net/)
* Python 3.x (with `requests` and `beautifulsoup4` installed)
* ImageMagick (`magick` added to your system PATH)

## Installation
1. Clone or download this repository into your `Documents\Rainmeter\Skins\` folder.
2. Open Rainmeter, click "Refresh all", and load the `GoogleDoodle.ini` skin!
3. To customize the framerate or size, adjust the values in the `[Variables]` section of the `.ini` file!
