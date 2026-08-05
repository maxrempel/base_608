import asyncio
import datetime
import json
import os

from playwright.async_api import async_playwright

LOG = r"C:\claude_base\worklog\sfari_oksana\login_log.txt"
PROFILE = r"C:\claude_base\worklog\sfari_oksana\chrome_profile_oksana_v01"
SHOT = r"C:\claude_base\worklog\sfari_oksana\after_login.png"
DUMP = r"C:\claude_base\worklog\sfari_oksana\page_dump.json"


def log(msg: str) -> None:
    line = f"[{datetime.datetime.now().isoformat()}] {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


async def main() -> None:
    username = os.environ.get("LOGIN_USERNAME", "")
    password = os.environ.get("LOGIN_PASSWORD", "")
    log("start; user=" + username)
    if not username or not password:
        log("ERROR: missing credentials")
        return
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
            await page.goto("https://base.sfari.org/", wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(4000)
            log("url after load: " + page.url)
            try:
                head = (await page.evaluate("document.body.innerText"))[:200].replace("\n", " | ")
                log("body head: " + head)
            except Exception:
                pass
            email_input = page.locator('input[name="email"]')
            if await email_input.count() > 0:
                log("login form present; filling")
                await email_input.fill(username)
                await page.fill('input[name="password"]', password)
                login_btn = page.locator('button:has-text("Log In")')
                if await login_btn.count() > 0:
                    await login_btn.first.click()
                    log("clicked Log In")
                else:
                    log("WARNING: Log In button not found; trying form submit")
                    await page.evaluate("document.querySelector('form').requestSubmit ? document.querySelector('form').requestSubmit() : document.querySelector('form').submit()")
                ok = False
                for i in range(36):
                    await page.wait_for_timeout(2500)
                    try:
                        txt = await page.evaluate("document.body ? document.body.innerText : ''")
                    except Exception:
                        txt = ""
                    url2 = page.url
                    if "Log Out" in txt or "logOut" in txt:
                        ok = True
                        log(f"login appears successful at poll {i}")
                        break
                    if "Forgot your password" not in txt and "Log In" not in txt and len(txt) > 50:
                        ok = True
                        log(f"login state changed at poll {i}")
                        break
                    if url2.rstrip("/") == "https://base.sfari.org" and "Forgot your password" not in txt:
                        ok = True
                        log(f"dashboard url reached at poll {i}")
                        break
                if not ok:
                    log("WARNING: login state uncertain; url=" + page.url +
                        "; if a Cloudflare checkbox is visible in the window, click it and wait")
            else:
                log("no login form; possibly already logged in")
            await page.wait_for_timeout(3000)
            info = await page.evaluate(
                """() => {
                  const q = (s) => Array.from(document.querySelectorAll(s)).map(e => ({
                    tag: e.tagName, name: e.name||null, id: e.id||null, type: e.type||null,
                    placeholder: e.placeholder||null, value: (e.value||'').slice(0,80),
                    disabled: e.disabled, text: (e.innerText||'').trim().slice(0,160),
                    href: e.getAttribute('href')||null
                  }));
                  return { url: location.href, title: document.title, inputs: q('input'),
                           selects: q('select'), textareas: q('textarea'), buttons: q('button'),
                           links: q('a'), bodyText: document.body.innerText.slice(0, 8000) };
                }"""
            )
            with open(DUMP, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=1)
            await page.screenshot(path=SHOT, full_page=False)
            log("dump written; url=" + page.url)
            # Fill the institution details form (leave Submit for the user)
            ein = page.locator('input[name="ein"]')
            if await ein.count() > 0:
                cur = (await ein.input_value()).strip()
                if cur != "83-0652460":
                    await ein.fill("83-0652460")
                    log("filled EIN: 83-0652460")
                else:
                    log("EIN already correct")
                np_true = page.locator('input[name="nonprofit"][value="true"]')
                np_false = page.locator('input[name="nonprofit"][value="false"]')
                if await np_true.count() > 0:
                    true_checked = await np_true.is_checked()
                    false_checked = await np_false.is_checked() if await np_false.count() > 0 else False
                    log(f"radio state: nonprofit_checked={true_checked} forprofit_checked={false_checked}")
                    if not true_checked:
                        await np_true.check(force=True)
                        log("selected Non-profit")
                else:
                    log("WARNING: nonprofit radio not found")
                await page.wait_for_timeout(1500)
                info2 = await page.evaluate(
                    """() => ({
                      ein: (document.querySelector('input[name="ein"]')||{}).value||null,
                      np_true: document.querySelector('input[name="nonprofit"][value="true"]') ? document.querySelector('input[name="nonprofit"][value="true"]').checked : null,
                      np_false: document.querySelector('input[name="nonprofit"][value="false"]') ? document.querySelector('input[name="nonprofit"][value="false"]').checked : null,
                      common: (document.querySelector('input[name="name"]')||{}).value||null,
                      official: (document.querySelector('input[name="official_name"]')||{}).value||null
                    })"""
                )
                log("form state after fill: " + json.dumps(info2))
                await page.screenshot(path=r"C:\claude_base\worklog\sfari_oksana\form_filled.png", full_page=False)
            else:
                log("no institution form on this page")
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
