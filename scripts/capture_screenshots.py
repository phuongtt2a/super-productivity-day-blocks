"""Capture Day Blocks screenshots with illustrative data, never private user data."""
from io import BytesIO
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"docs"/"screenshots"
OUT.mkdir(parents=True,exist_ok=True)
HTML=(ROOT/"plugin"/"index.html").read_text(encoding="utf-8")

def save_image(page,name,full_page=True):
    content=page.screenshot(type="png",full_page=full_page,animations="disabled")
    Image.open(BytesIO(content)).convert("RGB").save(
        OUT/name,format="WEBP",quality=84,method=6
    )

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
    try:
        page=browser.new_page(viewport={"width":1660,"height":1010},device_scale_factor=1)
        page.goto("about:blank")
        page.set_content(HTML)
        page.wait_for_selector('.morning [data-session]')
        assert page.locator('.block').count()==4
        assert page.locator('.linked').count()>=2
        save_image(page,"day-blocks-desktop.webp")
        # Show the tidy secondary-action menu and the personalized color palette.
        first=page.locator('.morning .session').first
        first.locator('[data-more-session]').click()
        assert page.locator('#more-popup[role="dialog"]').is_visible()
        page.locator('#more-popup').screenshot(path=str(OUT/"session-color-options.png"),animations="disabled")
        Image.open(OUT/"session-color-options.png").convert("RGB").save(
            OUT/"session-color-options.webp",format="WEBP",quality=88,method=6
        )
        (OUT/"session-color-options.png").unlink()
        page.locator('#more-close').click()
        page.locator('.afternoon .session.multi').first.screenshot(path=str(OUT/"continuing-session.png"))
        # Convert the focused detail to a compact webp for documentation.
        image=Image.open(OUT/"continuing-session.png").convert("RGB")
        image.save(OUT/"continuing-session.webp",format="WEBP",quality=88,method=6)
        (OUT/"continuing-session.png").unlink()
        page.close()
        phone=browser.new_page(viewport={"width":390,"height":844},device_scale_factor=1,has_touch=True,is_mobile=True)
        phone.goto("about:blank")
        phone.set_content(HTML)
        phone.wait_for_selector('.morning [data-session]')
        assert phone.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        save_image(phone,"day-blocks-phone.webp")
        phone.locator('#timeline-scroll').evaluate("(el)=>{el.scrollLeft=el.clientWidth*1.06}")
        save_image(phone,"day-blocks-phone-scroll.webp")
        phone.close()
        tiny=browser.new_page(viewport={"width":320,"height":690},device_scale_factor=1,has_touch=True,is_mobile=True)
        tiny.goto("about:blank")
        tiny.set_content(HTML)
        tiny.wait_for_selector('.morning [data-session]')
        assert tiny.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        save_image(tiny,"day-blocks-small-phone.webp")
        tiny.close()
        print("Generated desktop, slate-night, icon-toolbar, popup and responsive phone screenshots")
    finally:
        browser.close()
