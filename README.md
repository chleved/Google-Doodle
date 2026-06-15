# Google Doodle — Rainmeter Skin

Displays **today's Google Doodle** on your desktop, automatically refreshed every hour.  
Shows the regional doodle for your country (Italy → Italian doodle), just like visiting google.com would.

---

## How it works

Google has an unofficial (but publicly accessible) JSON endpoint:

```
https://www.google.com/doodles/json/YYYY/MM
```

No API key needed. Rainmeter's WebParser fetches the JSON, extracts the image URL and title,
downloads the image, and renders it directly on your desktop.

---

## Installation

1. Copy the `GoogleDoodle\` folder into:
   ```
   %USERPROFILE%\Documents\Rainmeter\Skins\
   ```

2. Right-click the **Rainmeter tray icon** → Manage → find `GoogleDoodle` → Load `GoogleDoodle.ini`

   Or: right-click tray → Skins → GoogleDoodle → GoogleDoodle.ini

3. Done. The doodle appears on your desktop.

---

## Usage

| Action | Effect |
|---|---|
| **Click** the doodle image | Opens doodles.google.com in your browser |
| **Right-click** the skin → Refresh | Force re-fetches the current doodle immediately |
| Auto-refresh | Every 1 hour (3 600 update cycles × 1 s each) |

---

## Customization

Open `GoogleDoodle.ini` in a text editor and edit the `[Variables]` section:

```ini
[Variables]
ImgWidth=420        ; Width of the doodle image in pixels (height auto-scales)
RefreshRate=3600    ; Re-fetch interval in seconds (3600 = 1 hour)
Font=Segoe UI       ; Font for the title bar
```

To change skin position: drag it, or use Rainmeter's Manage dialog.

---

## Limitations

- **Video / interactive doodles** (e.g. the Halloween game) can't be rendered as a static image.  
  The skin shows a notice and a click-link instead.
- If Google has **no special doodle today**, the skin shows the most recent doodle from this month.
- Some doodles are **region-limited** — you'll see whichever one Google serves to Italy.
- Google may throttle or block the endpoint in the future (it's unofficial). Right-click → Refresh
  to test; if it stops working, the `MeasureJSON` debug log will say why.

---

## Troubleshooting

1. Right-click the skin → **About (Skin)** to see the log — errors show up here.
2. If the image doesn't appear on first load, wait ~5 seconds and right-click → Refresh.  
   The image downloads asynchronously (3-step chain: fetch JSON → parse URL → download image).
3. If WebParser returns nothing, add `Debug=2` to `[MeasureJSON]` temporarily, refresh the skin,
   and inspect `WebParserDump.txt` in the skin folder to see what Google returned.
