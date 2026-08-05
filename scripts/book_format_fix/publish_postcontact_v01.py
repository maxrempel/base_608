# -*- coding: utf-8 -*-
"""Create the 'Postcontact: the Ascension Textbook' book + its chapter-0 summary.

The full text is a living website mirrored at /poco; this book entry gives it a
place in the library (sorted last via books.sort_order, set separately) and a
reader's summary that links out to /poco.
"""
import json, urllib.request

API = "https://maxrempel.com/api/book"
TOKEN = "mxr-blog-7f3k9x2m4p"

SLUG = "postcontact"
TITLE = "Postcontact: the Ascension Textbook"
AUTHOR = "Max Rempel, Ph.D."
DESC = "An optimistic textbook for life after open contact with friendly aliens. A living online book."

LINK = ('<p style="margin-bottom:1rem;"><a href="/poco" style="font-weight:bold;">'
        'Read the full living textbook at maxrempel.com/poco</a></p>')
DATE = '<p style="color:#888;font-style:italic;margin-bottom:1.2rem;">Published online, 2025-2026 (a living book)</p>'

SUMMARY = """
"Postcontact: the Ascension Textbook" by Max Rempel, Ph.D. (2025-2026), is a hopeful, speculative non-fiction work that lays out an optimistic, "common-sense" scenario for what happens after humanity makes open contact with benevolent extraterrestrials. It is addressed to general readers curious about UFO disclosure, consciousness, and humanity's evolutionary future, and it deliberately rejects catastrophic narratives in favor of a constructive vision grounded in the law of attraction and collective choice.

The book's central premise is that a friendly Galactic Federation has long observed Earth but respected human free will under a "Prime Directive," declining to intervene openly until humanity is ready. Rempel argues Earth has effectively been treated as a colony by hidden human "runaway civilizations" and certain alien races, while the benevolent Federation gently steers events away from disaster. He places likely open contact around 2027-2037 (citing the channeled source Bashar), with the Federation engaging a coalition of Western governments, later joined by China and Russia, focusing on information and cultural exchange rather than technology transfer, and helping enforce global peace.

"Ascension" here means a gradual dimensional shift driven by spreading telepathy, peace, ecological restoration, and growing "high-vibration pockets" on Earth. The Telepathy section argues that as ecological and social anxiety ease, dormant psychic capacities reactivate; children, autistic and non-verbal people retain this ability because they never learned to perform a divided social self. Telepathy spreads as a self-reinforcing feedback loop, dissolving concealment and forcing genuine moral honesty rather than mere appearance.

The thematic sections map a transformed civilization. The Economy section foresees not AI rule but AI advisers that improve matchmaking, reduce corruption through transparency, and expand a cross-border freelance economy, needing only to sustain stability through the transition. Awakening describes a guided decade-long renaissance (2027-2037) in which institutions reform voluntarily, churches adopt telepathic teaching, education favors wisdom over memorization, and people form neighbor circles for resource-sharing, with most feeling relief rather than resistance. Healing predicts psychological recovery over consumerism, mainstreamed psychedelics and plant medicine, gentler treatment of children, and nature communication. Religion holds that faiths adapt rather than vanish as people directly experience that universal consciousness is "all that is" and God is not a separate ruler but the unified ground of being; shamanism and ceremony regain legitimacy through an expanded empiricism. The Future Humanity section envisions a non-hierarchical, cooperative, telepathically connected society, symbolized as "a silent tribal circle around the fire."

The book also includes a Stories section with short fiction ("Little by Little, A Lot by A Lot" and "Job Interview at the End of the World") dramatizing the transition through intimate personal perspectives, plus About and Podcast pages.

Its practical message is less a how-to than an invitation: humans themselves must initiate disclosure, and individuals participate by choosing positivity, cultivating inner coherence and honesty, aligning with the guided transition rather than opposing it, and trusting that a peaceful, telepathic ascension is genuinely achievable.
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def to_html(text):
    paras = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    return "\n".join(f"<p>{esc(p)}</p>" for p in paras)


def post(payload):
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) maxrempel-book-importer/1.0"},
        method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


rb = post({"type": "book", "slug": SLUG, "title": TITLE,
           "author": AUTHOR, "description": DESC, "lang": "en"})
print("book:", rb.get("success"))

# The full text now lives in this same book (chapters 1-12), so no external
# /poco link in the summary -- it would be circular. Keep date + summary only.
content = DATE + "\n" + to_html(SUMMARY)
rc = post({"type": "chapter", "book_slug": SLUG, "chapter_num": 0,
           "title": "Summary", "content": content})
print(f"ch0: {len(content)} chars ->", rc.get("success"))
