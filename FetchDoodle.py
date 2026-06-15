import os
import time
from playwright.sync_api import sync_playwright

def download_doodle_with_playwright():
    # print("Launching Playwright to scrape the Google Doodle...")
    
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DownloadFile")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "doodle.gif")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using a mobile user-agent sometimes gives a simpler static doodle image instead of complex canvas
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720},
            locale="it-IT"
        )
        page = context.new_page()
        
        found_urls = []
        
        # Intercept network responses to catch the doodle image loading
        def on_response(response):
            url = response.url
            if '/logos/doodles/' in url and url.endswith(('.gif', '.png', '.jpg', '.webp')):
                found_urls.append(url)

        page.on("response", on_response)
        
        # print("Navigating to https://www.google.it/ ...")
        page.goto("https://www.google.it/", wait_until="networkidle")
        
        # Give it a few seconds to fully render any JS doodles
        page.wait_for_timeout(3000)
        
        found_url = None
        
        # Prefer .gif files over .png files (because Google serves a static -lsg.png first)
        for u in found_urls:
            if u.endswith('.gif'):
                found_url = u
                break
        
        if not found_url and found_urls:
            found_url = found_urls[-1]  # take the last loaded image just in case
            
        if found_url:
            # Download the chosen url
            # print(f"Intercepted Doodle URL in network: {found_url}")
            try:
                # We have to fetch it via evaluate since we only kept the URL, not the response object
                js_fetch = f"""
                fetch('{found_url}')
                .then(r => r.blob())
                .then(blob => new Promise((resolve, reject) => {{
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.onerror = reject;
                    reader.readAsDataURL(blob);
                }}))
                """
                data_url = page.evaluate(js_fetch)
                import base64
                header, encoded = data_url.split(",", 1)
                with open(save_path, "wb") as f:
                    f.write(base64.b64decode(encoded))
            except Exception as e:
                pass
        
        # Fallback: check DOM if not found in network
        if not found_url:
            # print("No doodle found in network requests. Checking DOM...")
            images = page.locator("img").all()
            for img in images:
                src = img.get_attribute("src")
                if src and '/logos/doodles/' in src:
                    found_url = src
                    title = img.get_attribute("alt") or "Google Doodle"
                    
                    # print(f"Found Doodle in DOM: {src} - Title: {title}")
                    
                    # Save the title
                    with open(os.path.join(save_dir, "title.txt"), "w", encoding='utf-8') as f:
                        f.write(title)
                        
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = 'https://www.google.it' + src
                    
                    # Download it using page.evaluate to fetch
                    js_fetch = f"""
                    fetch('{src}')
                    .then(r => r.blob())
                    .then(blob => new Promise((resolve, reject) => {{
                        const reader = new FileReader();
                        reader.onloadend = () => resolve(reader.result);
                        reader.onerror = reject;
                        reader.readAsDataURL(blob);
                    }}))
                    """
                    data_url = page.evaluate(js_fetch)
                    import base64
                    header, encoded = data_url.split(",", 1)
                    with open(save_path, "wb") as f:
                        f.write(base64.b64decode(encoded))
                    # print(f"Successfully saved DOM image to {save_path}")
                    break
                    
        # Also grab title if we intercepted from network
        if found_url and not os.path.exists(os.path.join(save_dir, "title.txt")):
            images = page.locator("img").all()
            for img in images:
                src = img.get_attribute("src")
                if src and '/logos/doodles/' in src:
                    title = img.get_attribute("alt") or "Google Doodle"
                    with open(os.path.join(save_dir, "title.txt"), "w", encoding='utf-8') as f:
                        f.write(title)
                    break
                    
        if not found_url:
            # print("No Google Doodle active today on google.it.")
            # Fallback to standard google logo to not break the skin
            fallback_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
            page.goto(fallback_url)
            page.wait_for_timeout(1000)
        # Generate the search link based on the doodle's title
        import urllib.parse
        doodle_title = "Google Doodle"
        images = page.locator("img").all()
        for img in images:
            src = img.get_attribute("src")
            if src and '/logos/doodles/' in src:
                alt = img.get_attribute("alt")
                if alt:
                    doodle_title = alt
                break
                
        search_query = urllib.parse.quote_plus(doodle_title)
        doodle_link = f"https://www.google.com/search?q={search_query}"
                
        with open(os.path.join(save_dir, "link.txt"), "w", encoding='utf-8') as f:
            f.write(doodle_link)
            
        browser.close()
        
    process_gif(save_path, os.path.join(save_dir, "sprite.png"))

def process_gif(input_file, output_file):
    import subprocess
    import sys
    import math
    
    width = 250
    skin_update = 16
    if len(sys.argv) > 1:
        width = int(sys.argv[1])
    if len(sys.argv) > 2:
        skin_update = int(sys.argv[2])
        
    speed_multiplier = 1.5
    
    try:
        # Get frame count
        res = subprocess.run(["magick", "identify", "-format", "%n\n", input_file], capture_output=True, text=True, check=True)
        frames_lines = res.stdout.strip().split('\n')
        frames = int(frames_lines[0]) if frames_lines and frames_lines[0].strip() else 1
        
        # Get delays
        res = subprocess.run(["magick", "identify", "-format", "%T\n", input_file], capture_output=True, text=True, check=True)
        delay_lines = res.stdout.strip().split('\n')
        valid_delays = []
        for d in delay_lines:
            try:
                val = int(d.strip())
                if val > 1:
                    valid_delays.append(val)
            except ValueError:
                pass
                
        if valid_delays:
            avg_delay = sum(valid_delays) / len(valid_delays)
            delay_cs = round(avg_delay)
        else:
            delay_cs = 10
            
        if delay_cs <= 1:
            delay_cs = 10
            
        delay_ms = (delay_cs * 10) / speed_multiplier
        optimal_divider = max(1, round(delay_ms / skin_update))
        
        # Get dimensions
        first_frame = f"{input_file}[0]"
        res = subprocess.run(["magick", "identify", "-format", "%w %h", first_frame], capture_output=True, text=True, check=True)
        dims = res.stdout.strip().split(' ')
        orig_w = int(dims[0])
        orig_h = int(dims[1])
        
        target_w = width
        target_h = round(orig_h * (target_w / orig_w))
        
        temp_file = output_file + ".miff"
        
        # Process image
        subprocess.run(["magick", input_file, "-coalesce", "-resize", f"{target_w}x{target_h}!", "-background", "none", temp_file], check=True)
        subprocess.run(["magick", "montage", temp_file, "-tile", "1x", "-geometry", "+0+0", "-background", "none", output_file], check=True)
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        sys.stdout.write(f"{frames}|{delay_ms:.2f}|{target_h}|{optimal_divider}")
        sys.stdout.flush()
        
    except Exception as e:
        # Default fallback output if anything fails
        sys.stdout.write(f"1|100|250|1")
        sys.stdout.flush()

if __name__ == "__main__":
    download_doodle_with_playwright()
