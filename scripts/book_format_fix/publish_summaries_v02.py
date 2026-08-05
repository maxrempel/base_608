# -*- coding: utf-8 -*-
"""Upsert thorough (~3000 char) chapter-0 'Summary' for each published book.

Chapter 0 is rendered by the worker as the book's default landing view.
Idempotent: re-running upserts (ON CONFLICT book_slug,chapter_num).
"""
import json, urllib.request

API = "https://maxrempel.com/api/book"
TOKEN = "mxr-blog-7f3k9x2m4p"
DATE = '<p style="color:#888;font-style:italic;margin-bottom:1.2rem;">{}</p>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def to_html(text):
    paras = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    return "\n".join(f"<p>{esc(p)}</p>" for p in paras)


CELESTIAL = """
Celestial Science (2011) by Max Rempel, Ph.D. is an ambitious attempt to fuse materialist science, monotheistic religion, New Age channeling and ufology into a single integrated "New Paradigm." Written, as Max stresses, before any "Official Disclosure," the book starts where most UFO books stop: it takes alien contact as given and asks how to reconcile it with everything else we believe. Max coins the term "celestial" because the beings involved come from higher densities or dimensions rather than merely other planets.

The first part, Star Children, argues that Indigo, Crystal and Starseed children with psychic and telepathic gifts are emerging through an alien hybridization program run mainly by the Zeta Greys. Drawing on abduction research and channeled sources like Bashar and the Cassiopaeans, Max contends abductees are genetically modified, possibly humanity's "saviors," carrying genes for the coming shift to fourth density. He reframes abduction trauma as misperception, urging acceptance over anger.

Our Future centers on "the Shift" from third to fourth density around 2012 and beyond. Max trusts Bashar's optimistic, conservative predictions (gradual contact 2015-2050) over the failed catastrophic forecasts of channels like Sheldan Nidle. He explains failed prophecies through deception, confusion and a "branching paradox": multiple versions of the future exist, so higher beings struggle to convey which one applies. He describes the Galactic Federation, the Orion Empire, the lifting of Earth's ancient "Quarantine," and the Cetaceans (dolphins and whales) as a telepathic guardian species.

Transformation of Religion is the longest part. Max argues the God who guided the Hebrews through Exodus was not the Prime Creator but a deceptive extraterrestrial (linked to the Anunnaki, Yahweh/Enki). Citing Sitchin, Blavatsky and channeled material, he says humanoid "Creator Gods" engineered humans as workers and disabled our DNA and pineal gland, veiling our psychic powers. He distinguishes the Prime Creator ("All There Is," per the Ra material's "Law of One") from these lesser gods, and presents Jesus as essentially a New Age teacher who replaced Yahweh's malevolence with unconditional love. He proposes "creative evolution," blending Darwinism with archetypal seeding of universal life forms.

Reincarnation presents rebirth as humanity's forgotten truth, removed from Christianity at early councils but preserved in Kabbalah and Eastern faiths. Souls are "hatched" in nurseries (per Michael Newton's regressions), undergo roughly 100 to 160 Earth lives to learn lessons and raise their vibration, then return to the Source.

Higher Self, the climax, teaches that each person's true identity is a non-physical Higher Self that scripts our incarnation, arranging "random" events, synchronicities and even suffering to grow itself. Solipsistic and Matrix-like, reality is an illusion-school. The "Second Coming" is each individual awakening their own Christ or Buddha consciousness. The Source ultimately experiences itself through all our lives.
"""

WELCOME = """
"Welcome to Earth! A Guide for Aliens" by Max Rempel, Ph.D., is written tongue-in-cheek as an orientation manual addressed directly to newly arriving star beings and human-alien hybrids, explaining humanity from the outside in the affectionate tone of someone introducing a beloved culture to strangers. Rempel builds everything from two central premises: humans at large are neither telepathic nor psychic, and human lifespans are short. From these two facts he derives most of what makes Earth distinctive. Because there is no telepathy, communication runs only through voice, gesture and appearance, which breeds isolation, deception, and enormous diversity of languages, races and cultures; because life is short, humans learn little individually yet evolve fast, crave love and friendship, and create art to outlive themselves.

The book asserts that the human genome, though rooted in an Earth predecessor, carries ancient and recent infusions from many alien lineages, including Annunaki, Pleiadians, Lemurians, Lyrans, Sirians, and possibly Greys and Reptilians. Earth thus becomes a miniature of the galaxy, its conflicts an echo of old galactic wars imprinted in the DNA of different peoples.

Across its chapters the book surveys human life topic by topic. It covers survival, art, dance, theater, emotions, atheism, the fragmented and easily-programmed human mind, the New Age "Awakening" of lightworkers, and love in its many forms (including a stated love for the aliens themselves). It examines hatred, xenophobia, aggression, and the human fear of aliens and hybrids, while arguing humanity's exploratory, brave, self-sacrificing nature (Rempel cites Robert Shapiro's "Explorer Race") could serve a galactic community.

Drawing heavily on Rempel's own life in the Soviet Union and later America, the book treats crime and deception as universal human features, illustrated through Soviet history, film, and figures like Okudzhava, Smoktunovsky and Roerich. It describes the rhythms and cycles of daily life, a detailed "typical morning," pollution, weapons, and a political system Rempel sees as secretly run by an international Military-Industrial Complex (MIC) that thrives on war, secrecy and manipulated choice. He cites Bashar, David Icke, David Wilcock and Alex Jones as sources, and argues that, just as Radio Liberty's broadcasting of truth helped dissolve the deception-based Soviet system, alien-assisted broadcasting of truth could free humanity.

The book's practical core is a proposal: aliens should help build an off-world human colony to develop a new "alien-aware" human culture, broadcast educational material back to Earth, run schools and clinics, and gradually educate even MIC workers. It discusses how humans might eventually accept genetic improvement (via human-alien mating or gene therapy) to strengthen altruism, telempathy and psychic ability while reducing aggression and deception. Later chapters explore children and education, Rempel's youthful experience at a White Sea biological station as a model "dissident colony," and his own intuitive, empirical style of thinking, which he presents as creative, propaganda-resistant, and perhaps closer to how aliens think. Throughout, the framing remains a loving invitation: humanity is in crisis, and the aliens are asked to come and help.
"""

METAPHYSICS = """
Max Rempel opens "Metaphysics for Lightworkers" by describing his own path. From age sixteen he felt drawn to the Pleiades and to anything with a spiritual dimension. Chronic pains brought him to energy healers, whose work convinced him that healing energy is spiritual, not material. Lynn McTaggart's book "The Field" led him to research star people from 1999 onward. He hosted experiencer and abductee support groups, became a UFO-community speaker, and published his first book in 2011. He took Reiki around 2012, reached master-teacher level by 2015, began conversations with star people through channelers, and in 2013 founded the online channeling community HumanColony.org. His own channeling started in April 2015. When he does Reiki, clients sense star energies he has invited, continuing the tradition of Adrian Dvir of Israel.

The book teaches a cosmology in which creation and evolution operate side by side, like a company that founds a project, funds it, then lets it evolve. The universe was created from spirit and then evolved in waves. Material life exists only in 3rd density (our level) and 4th density, where advanced civilizations reside; higher levels are more dreamlike. God is everything, mostly spiritual; we are fractal copies of God, which is why we can channel Reiki.

Max recounts the origins of life and humanity. Stars and planets are playgrounds seeded with life and watched over by higher consciousnesses, including fairies and elves who support the dimensions. Humans entered the galaxy from outside, first as spirits. The first humans were the Lyrans, a feline cat-people race from Vega whose planet was destroyed by Reptilians, scattering the human form across the galaxy. Earth was seeded many times: the Annunaki mixed their genes with native Sasquatch, and Lyrans, Pleiadians, Yahyel, Arcturians and others added DNA. Everyone is therefore a starseed.

The book develops a detailed afterlife model: the veil of forgetfulness, Higher Selves and souls as fractal copies, reincarnation with traumas stored in chakras, spirit guides, life review, and the choices a soul makes afterward. It frames reality as a self-protecting Matrix or hologram, where proof of the spiritual is always deniable, and where healers create high-vibration "bubble realities."

Much of the text is a practical Reiki and Galactic Reiki manual: inviting star helpers, scanning energies, stepping aside to let spirit work, giving thanks, elevating mood with sage and incense, and networking through Reiki shares and spiritualist churches. Max profiles the friendly star races assisting Earth's healing and ascension: the Pleiadians of Erran culture, the Yahyel (chosen to lead Open Contact), the formal Arcturians, and the Lyrans, all part of alliances preparing first contact under quarantine and the prime directive.

Finally, the book describes the modern, consent-based alien hybridization program. Early hybridizations were traumatic, but since 2014 they require written or spoken human consent. Humans can now request small Lyran, Pleiadian or Yahyel DNA infusions, or donate DNA to raise hybrid children in 4th-density alien cultures, who later visit their human parents in dreams.
"""

GALAXY = """
From the Galaxy, With Love: A Lightworker's Textbook, by Max Rempel and James Ernest Charles (first edition July 2018, San Diego), is a deliberately positive and accessible textbook about friendly aliens and the process of Ascension. Max Rempel narrates and synthesizes seven years of research, current as of early 2017, drawing on the channelings of his co-author James Ernest Charles ("Jim") and other channelers. The authors keep complex, dramatic material simple and focus on hope: they regard the emergence of aliens and hybrid children as the most important event happening to humanity.

The book rests on two sources of knowledge. Experiencers are humans who have met aliens face to face, spoken with them and visited their ships and worlds. Channeling is the second source, in which a channeler enters trance, connects telepathically to an alien, and lets an audience converse with them directly. Much of the text alternates between Max's plain-English explanations and verbatim transcripts of channeled dialogues.

A central premise is that most aliens visiting Earth are inter-dimensional beings from the 4th Density (called 4D, versus our 3D). They normally exist in a different, lighter reality invisible to us, but can materialize here briefly, often only for a few hours. Life in 4D is marked by telepathy, psychic and telekinetic abilities, longer lifespans and more flexible time. The book explains Ascension as humanity's gradual shift from 3D to 4D, a conscious, voluntary process aided by aliens, angels and spirits, with the key collective step being "Open Contact," in which governments disclose alien contact and the public invites the friendly aliens to appear openly.

The authors then survey the friendly galactic civilizations and Earth's deep history. Chapters cover the Lyrans (tall feline humanoids, the galaxy's "Founders" and our ancestors), the Pleiadians (including the Mayans, the human-like Errans of Taygeta under King Kenjin, and the Coriatorians), the Arcturians, and the Yahyel, who will likely be first to make open contact. Historical chapters address the destruction of Atlantis, Lemuria, and the origins of humanity, explaining that modern humans are a hybrid of Earth stock and roughly twenty-two alien races. A major section details the hybridization program, both its early traumatic, abduction-based phase run by negative Zeta-Greys and Reptilians and the present-day voluntary, humane program run by Pleiadians and Yahyel, alongside the appearance of starseeds, indigo and crystal children.

The second half turns spiritual and practical, offering teachings on reincarnation, love, conception, astrology, depression, death, the chakras, spirit guides, life lessons, the Higher Self, healing and meditation, with channeled messages from beings including Angel Gahil and Buddha. Throughout, the book argues that humans are already biologically ready for 4D and that only our politics and reliance on deception hold us back; developing telepathy will heal society and enable collective awakening. Its overarching message is hopeful: humanity is awakening to a loving visitation, and our cosmic family stands ready to help us ascend.
"""

BOGI = """
Книга Макса Ремпеля «Боги о нас. Введение в современную метафизику» (2012) представляет метафизику как науку, выходящую за пределы физики и объединяющую материальный и нематериальный мир. Автор опирается на то, что уже квантовая механика размыла границу между материей и полем, и утверждает, что нематериальный мир можно изучать систематически, сравнивая независимые источники, как это делают история, биология или геология без эксперимента. Метафизика, в отличие от религии, подходит к посланиям из высших сфер без страха и пиетета: единственный авторитет для неё — истина и здравый смысл. Книга задумана не как доказательство сверхъестественного, а как путеводитель по первоисточникам, преимущественно англоязычным.

Центральная тема — душа. Автор обобщает парапсихологические исследования (гипнотическая регрессия, свидетельства переживших клиническую смерть, сообщения от умерших, ясновидящие вроде Ванги и Кейси, контактёры-ченнелеры) и делает выводы: человек обладает бессмертной душой, которая проживает десятки воплощений-реинкарнаций ради совершенствования. Страшного Суда нет — вместо него мирный совет наставников. Земная жизнь — школа для роста души, причём не душа есть часть человека, а человек есть часть души.

Мироздание описано через систему «плотностей». Первые три — мёртвая материя, простая жизнь, человек — отделены от высших уровней искусственной Вуалью, которую приоткрывает лишь сон. Четвёртая плотность отличается телепатией и коллективным разумом, пятая — мир душ умерших, шестая — бестелесные ангелы (комплекс Ра, совет девяти). Обитатели высших плотностей — это и есть «боги» древности: пришельцы с телом (инопланетяне) и бестелесные формы разума (ангелы).

Автор излагает версию происхождения человека: направленная эволюция и генная инженерия пришельцев (Аннунаки по Ситчину, расы Плеяд, Сириуса, Дзета Сетки). Человек был выведен как раса рабов, и в нас намеренно заложены «рабские качества» и подавлена телепатия через искажение генома и эфирные «глушилки». Древние боги-птицы, ящеры и драконы присутствовали на Земле лично.

Кульминация книги — трансформация около 2012 года: конец 26-тысячелетнего прецессионного цикла и постепенный переход человечества в четвёртую плотность с приподниманием Вуали, ростом телепатии и объединением в единый разум (книги, ТВ, интернет — ступени к этому). Возможности высших сил ограничены тремя принципами: уважение нашей свободы выбора, экономия энергии и небесная иерархия.

Вторая половина книги — практическая философия «новых времён», которую автор связывает с тайной доктриной Блаватской и эзотерикой. Он объясняет Высшее Я (личный бог и автор судьбы), сверхдушу (кластер около 30 тысяч душ), закон мысленного притяжения, геометрию мироздания (золотое сечение, платоновы тела, энергосеть планеты) и роль везения. Главный практический вывод: перестать бояться, отпускать старое, менять себя изнутри, оставаться открытым к помощи в любой форме — и относиться к жизни как к игре.
"""

BOOKS = [
    ("celestial-science",            "Summary",     "First edition published November 2011",    CELESTIAL),
    ("from-the-galaxy",              "Summary",     "First edition published July 2018, San Diego", GALAXY),
    ("metaphysics-for-lightworkers", "Summary",     "Published July 2015",                      METAPHYSICS),
    ("welcome-to-earth",             "Summary",     "First edition 2013; second edition 2020",  WELCOME),
    ("bogi-o-nas",                   "\u0410\u043d\u043d\u043e\u0442\u0430\u0446\u0438\u044f", "\u0418\u0437\u0434\u0430\u043d\u043e \u0432 2012 \u0433\u043e\u0434\u0443", BOGI),
]


def post(payload):
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) maxrempel-book-importer/1.0"},
        method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


for slug, title, date, text in BOOKS:
    content = DATE.format(date) + "\n" + to_html(text)
    r = post({"type": "chapter", "book_slug": slug, "chapter_num": 0,
              "title": title, "content": content})
    print(f"{slug:<32} {len(content):>5} chars  ch0 -> {r.get('success')}")
