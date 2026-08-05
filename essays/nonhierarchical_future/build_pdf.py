import subprocess, pathlib, re, urllib.request

here = pathlib.Path(r"C:\claude_base\essays\nonhierarchical_future")
plates = here / "plates_web"

req = urllib.request.Request("https://postcontact.world/foh", headers={"User-Agent":"Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")

m = re.search(r'<main>(.*?)</main>', html, re.S)
body = m.group(1)
body = re.sub(r'<div class="page-toc".*?</div>\s*', '', body, flags=re.S)
body = re.sub(r'<div class="page-nav">.*?</div>', '', body, flags=re.S)
body = body.replace('src="/media/foh/', f'src="file:///{plates.as_posix()}/')

doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Non-Hierarchical Future of Humanity</title>
<style>
@page {{ size: A4; margin: 18mm 16mm 18mm 16mm; }}
body {{ font-family: Georgia, 'Times New Roman', serif; color:#1a1a1a; line-height:1.55; font-size:11.5pt; }}
h2.section-title {{ font-size: 22pt; color:#1a1a2e; margin: 0 0 6pt; border-bottom: 2px solid #c9a44b; padding-bottom:6pt; }}
.essay-subtitle {{ font-size: 13pt; font-style: italic; color:#444; text-align:center; margin: 8pt 0 2pt; }}
.essay-byline {{ font-size: 10.5pt; color:#8b7355; text-align:center; margin: 0 0 20pt; }}
p {{ margin: 0 0 9pt; text-align: justify; }}
.content-img {{ text-align:center; margin: 14pt 0; page-break-inside: avoid; }}
.content-img img {{ max-width: 92%; height:auto; border-radius: 3pt; }}
</style></head><body>{body}</body></html>"""

out_html = here / "foh_print.html"
out_html.write_text(doc, encoding="utf-8")

pdf = here / "20260518_nonhierarchical_future_v1.1_with_plates_v01.pdf"
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
    f"--print-to-pdf={pdf}", out_html.as_uri()
], check=True)
print("PDF:", pdf, pdf.stat().st_size // 1024, "KB")
