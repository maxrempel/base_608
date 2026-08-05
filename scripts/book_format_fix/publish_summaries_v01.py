#!/usr/bin/env python3
"""Post a chapter 0 'Summary' (with publication date) to each published book.

Chapter 0 is rendered by the worker as the book's default landing view.
Idempotent: re-running upserts (ON CONFLICT book_slug,chapter_num).
"""
import json, urllib.request

API = "https://maxrempel.com/api/book"
TOKEN = "mxr-blog-7f3k9x2m4p"

DATE = '<p style="color:#888;font-style:italic;margin-bottom:1.2rem;">{}</p>'


def p(*paras):
    return "\n".join(f"<p>{x}</p>" for x in paras)


BOOKS = [
    {
        "slug": "celestial-science", "title": "Summary",
        "date": "First edition published November 2011",
        "body": p(
            "A textbook of the New Paradigm, written before the Official Disclosure, that blends science and spirituality, New Age channelings and ufology into one non-contradictory whole. It begins where most books on ufology stop -- taking the extraterrestrial visitation as a given -- and attempts a systematic integration of that knowledge into our science and worldview.",
            "The book is organized in six parts: an Introduction to the need for integrated knowledge; Star Children (the emergence of Indigo, Crystal and Starseed children and the alien hybridization program); Our Future (the coming Shift); the Transformation of Religion; Reincarnation; and the Higher Self. Throughout, Max uses the term 'celestials' for the higher-dimensional beings and angels we are dealing with.",
            "Conceived as a straw man for a future university course in the new metaphysics.",
        ),
    },
    {
        "slug": "from-the-galaxy", "title": "Summary",
        "date": "First edition published July 2018, San Diego",
        "body": p(
            "By Max Rempel and James Ernest Charles. A positive, deliberately simple textbook about friendly aliens and Ascension, based on the channelings of Jim Charles together with other channelers and the testimony of experiencers.",
            "It explains that most aliens visiting Earth are inter-dimensional beings from the 4th Density -- normally invisible to us, yet able to materialize here briefly. The book covers how contact happens, who the visitors are, and why the awakening of humanity to this visitation is, in Max's view, the most important event happening to us. The fruit of seven years of research, with the information current as of early 2017.",
        ),
    },
    {
        "slug": "metaphysics-for-lightworkers", "title": "Summary",
        "date": "Published July 2015",
        "body": p(
            "By Max Rempel, Reiki Master, Ph.D. A guide for lightworkers, starseeds, and indigo and crystal children and adults -- all who feel a strong connection with the stars and star people.",
            "Drawing on years of channeling sessions (Max founded the online channeling community HumanColony.org in 2013) and on his Reiki practice, the book lays out a cosmology in which creation and evolution work side by side. It treats the origins of the universe, of life and of humanity; the seeding of the human form across the galaxy by Lyrans, Pleiadians, the Annunaki and others; dimensions and densities; energy healing; and the modern, consent-based phase of the alien hybridization program.",
        ),
    },
    {
        "slug": "welcome-to-earth", "title": "Summary",
        "date": "First edition 2013; second edition 2020",
        "body": p(
            "'Welcome to Earth! A Guide for Aliens.' Written tongue-in-cheek as an orientation manual for newly arrived star beings and hybrids, the book explains humanity to outsiders.",
            "Its starting point is two facts that set humans apart: we are, at large, neither telepathic nor psychic, and our lifespan is short. From these flow Earth's extraordinary diversity, its history, and its conflicts. The book describes the many alien lineages woven into the human genome -- Annunaki, Pleiadian, Lemurian, Lyran, Sirian and others -- and presents Earth as a miniature model of the galactic world, imprinted by a long history of galactic wars and expansions.",
        ),
    },
    {
        "slug": "bogi-o-nas", "title": "\u0410\u043d\u043d\u043e\u0442\u0430\u0446\u0438\u044f",
        "date": "\u0418\u0437\u0434\u0430\u043d\u043e \u0432 2012 \u0433\u043e\u0434\u0443",
        "body": p(
            "\u00ab\u0411\u043e\u0433\u0438 \u043e \u043d\u0430\u0441. \u0412\u0432\u0435\u0434\u0435\u043d\u0438\u0435 \u0432 \u0441\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e \u043c\u0435\u0442\u0430\u0444\u0438\u0437\u0438\u043a\u0443.\u00bb \u041a\u043d\u0438\u0433\u0430 \u043d\u0430 \u0440\u0443\u0441\u0441\u043a\u043e\u043c \u044f\u0437\u044b\u043a\u0435, \u0432\u0432\u043e\u0434\u044f\u0449\u0430\u044f \u0447\u0438\u0442\u0430\u0442\u0435\u043b\u044f \u0432 \u0441\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e \u043c\u0435\u0442\u0430\u0444\u0438\u0437\u0438\u043a\u0443 \u2014 \u043d\u0430\u0443\u043a\u0443, \u0432\u044b\u0445\u043e\u0434\u044f\u0449\u0443\u044e \u0437\u0430 \u043f\u0440\u0435\u0434\u0435\u043b\u044b \u0444\u0438\u0437\u0438\u043a\u0438 \u0438 \u0432\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0443\u044e \u043a\u0430\u043a \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044c\u043d\u044b\u0439, \u0442\u0430\u043a \u0438 \u043d\u0435\u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u043c\u0438\u0440.",
            "\u041e\u043f\u0438\u0440\u0430\u044f\u0441\u044c \u043d\u0430 \u043f\u0430\u0440\u0430\u043f\u0441\u0438\u0445\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u044f \u0434\u0443\u0448\u0438 \u0438 \u043d\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u044b \u0441 \u0440\u0430\u0437\u0443\u043c\u043d\u044b\u043c\u0438 \u043e\u0431\u0438\u0442\u0430\u0442\u0435\u043b\u044f\u043c\u0438 \u043d\u0435\u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043c\u0438\u0440\u0430 \u2014 \u043f\u0440\u0438\u0448\u0435\u043b\u044c\u0446\u0435\u0432 \u0438\u0437 \u0434\u0440\u0443\u0433\u0438\u0445 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u0439 \u0438 \u0431\u0435\u0441\u0442\u0435\u043b\u0435\u0441\u043d\u044b\u0445 \u0444\u043e\u0440\u043c \u0440\u0430\u0437\u0443\u043c\u0430, \u043a\u043e\u0442\u043e\u0440\u044b\u0445 \u0432 \u0434\u0440\u0435\u0432\u043d\u043e\u0441\u0442\u0438 \u043d\u0430\u0437\u044b\u0432\u0430\u043b\u0438 \u0431\u043e\u0433\u0430\u043c\u0438, \u2014 \u0430\u0432\u0442\u043e\u0440 \u043f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0435\u0442, \u0447\u0442\u043e \u043e\u043d\u0438 \u0440\u0430\u0441\u0441\u043a\u0430\u0437\u044b\u0432\u0430\u044e\u0442 \u043e \u043d\u0430\u0448\u0435\u0439 \u0438\u0441\u0442\u043e\u0440\u0438\u0438, \u0431\u0438\u043e\u043b\u043e\u0433\u0438\u0438, \u044d\u043d\u0435\u0440\u0433\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0442\u0435\u043b\u0430\u0445 \u0438 \u0434\u0443\u0448\u0430\u0445.",
            "\u041c\u0435\u0442\u0430\u0444\u0438\u0437\u0438\u043a\u0430 \u0437\u0434\u0435\u0441\u044c \u043f\u043e\u043d\u0438\u043c\u0430\u0435\u0442\u0441\u044f \u043a\u0430\u043a \u043d\u0430\u0443\u043a\u0430: \u0431\u0435\u0437 \u0441\u0442\u0440\u0430\u0445\u0430 \u0438 \u0431\u0435\u0437 \u043f\u0438\u0435\u0442\u0435\u0442\u0430, \u0441\u0440\u0430\u0432\u043d\u0438\u0432\u0430\u044f \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u044b\u0435 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438. \u041a\u043d\u0438\u0433\u0430 \u0441\u043b\u0443\u0436\u0438\u0442 \u043f\u0443\u0442\u0435\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u0435\u043c \u043f\u043e \u043f\u0435\u0440\u0432\u043e\u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430\u043c, \u0431\u043e\u043b\u044c\u0448\u0438\u043d\u0441\u0442\u0432\u043e \u043a\u043e\u0442\u043e\u0440\u044b\u0445 \u0430\u043d\u0433\u043b\u043e\u044f\u0437\u044b\u0447\u043d\u044b.",
        ),
    },
]


def post(payload):
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) maxrempel-book-importer/1.0"},
        method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


for b in BOOKS:
    content = DATE.format(b["date"]) + "\n" + b["body"]
    r = post({"type": "chapter", "book_slug": b["slug"], "chapter_num": 0,
              "title": b["title"], "content": content})
    print(f"{b['slug']:<32} ch0 -> {r.get('success')}")
