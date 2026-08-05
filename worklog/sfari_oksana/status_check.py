import asyncio
import datetime
import json
import os

from playwright.async_api import async_playwright

LOG = r"C:\claude_base\worklog\sfari_oksana\status_log.txt"
PROFILE = r"C:\claude_base\worklog\sfari_oksana\chrome_profile_oksana_v01"


def log(msg: str) -> None:
    line = f"[{datetime.datetime.now().isoformat()}] {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


async def main() -> None:
    username = os.environ.get("LOGIN_USERNAME", "")
    password = os.environ.get("LOGIN_PASSWORD", "")
    log("start")
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            PROFILE,
            channel="chrome",
            headless=False,
            viewport={"width": 1366, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        try:
            await page.goto("https://base.sfari.org/institution-details", wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(4000)
            log("url: " + page.url)
            ein = page.locator('input[name="ein"]')
            if await ein.count() > 0:
                log("RESULT: institution form still present (not yet submitted)")
                cur = (await ein.input_value()).strip()
                if cur != "83-0652460":
                    await ein.fill("83-0652460")
                    log("refilled EIN")
                np_true = page.locator('input[name="nonprofit"][value="true"]')
                if await np_true.count() > 0 and not await np_true.is_checked():
                    await np_true.check(force=True)
                    log("re-selected Non-profit")
                await page.screenshot(path=r"C:\claude_base\worklog\sfari_oksana\status_form.png")
            else:
                log("RESULT: institution form NOT present; page changed")
                body = await page.evaluate("document.body ? document.body.innerText : ''")
                log("BODY: " + body[:3000].replace("\n", " | "))
                await page.screenshot(path=r"C:\claude_base\worklog\sfari_oksana\status_page.png")
                # also try the home and user pages for institution status
                for path in ("/", "/user"):
                    try:
                        await page.goto("https://base.sfari.org" + path, wait_until="domcontentloaded", timeout=45000)
                        await page.wait_for_timeout(3000)
                        b = await page.evaluate("document.body ? document.body.innerText : ''")
                        log(f"PAGE {path}: " + b[:2500].replace("\n", " | "))
                    except Exception as e:
                        log(f"PAGE {path} error: {e!r}")
        except Exception as e:
            log("ERROR: " + repr(e))
        try:
            while True:
                await asyncio.sleep(30)
                if page.is_closed() or (ctx.browser and not ctx.browser.is_connected()):
                    break
        except Exception:
            pass
        log("browser closed by user")


asyncio.run(main())
