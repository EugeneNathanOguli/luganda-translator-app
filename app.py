from __future__ import annotations

import html
import json
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Luganda Bridge", page_icon="L", layout="centered")

PHRASEBOOK = {
    "hello": "olyotya",
    "good morning": "wasuze otya",
    "good afternoon": "osibye otya",
    "good evening": "osiibye otya",
    "good night": "sula bulungi",
    "how are you?": "oli otya?",
    "how are you": "oli otya",
    "i am fine": "ndi bulungi",
    "i am fine, thank you": "ndi bulungi, webale",
    "thank you": "webale",
    "thanks": "webale",
    "you are welcome": "kale nyo",
    "please": "nsaba",
    "sorry": "nsonyiwa",
    "excuse me": "nsonyiwa",
    "yes": "yee",
    "no": "nedda",
    "what is your name?": "olinnyira ki?",
    "my name is": "erinnya lyange ye",
    "i love you": "nkwagala",
    "welcome": "tukwanirizza",
    "see you later": "tulabagane olulala",
    "goodbye": "weraba",
    "help": "obuyambi",
    "help me": "nyamba",
    "i need help": "netaaga obuyambi",
    "where is the bathroom?": "kabuyonjo eri ludda wa?",
    "how much is this?": "kino kibbe sente mmeka?",
    "i do not understand": "sittegeera",
    "speak slowly, please": "yogera mpola, nsaba",
    "water": "amazzi",
    "food": "emmere",
    "friend": "mukwano",
    "home": "eka",
    "today": "leero",
    "tomorrow": "enkya",
    "now": "kaakano",
    "good luck": "omukisa omulungi",
    "congratulations": "mwebale nnyo",
    "happy birthday": "amazaalibwa amalungi",
    "have a nice day": "sula bulungi",
    "see you tomorrow": "tulabagane enkya",
    "what time is it?": "saawa meka?",
    "where are you going?": "ogenda wa?",
    "where do you live?": "obeera wa?",
    "i am from uganda": "nva mu Uganda",
    "i speak english": "njogera Lungereza",
    "do you speak english?": "oyogera Lungereza?",
    "can you help me?": "oyinza okunnyamba?",
    "call the police": "kuba poliisi",
    "call a doctor": "kuba dokita",
    "i am sick": "ndi mulwadde",
    "i am hungry": "njala ennuma",
    "i am thirsty": "nnyonta ennuma",
    "the food is delicious": "emmere ewooma",
    "i would like water": "njagala amazzi",
    "where is the market?": "akatale kali wa?",
    "where is the hotel?": "hoteeri eri wa?",
    "where is the hospital?": "eddwaliro liri wa?",
    "turn left": "kati ku kkono",
    "turn right": "kati ku ddyo",
    "go straight": "genda butereevu",
    "stop here": "yimirira wano",
    "i am lost": "mbuze ekkubo",
    "how far is it?": "wali wala wa?",
    "one": "emu",
    "two": "bbiri",
    "three": "ssatu",
    "four": "nnya",
    "five": "ttaano",
    "six": "mukaaga",
    "seven": "musanvu",
    "eight": "munana",
    "nine": "mwenda",
    "ten": "kkumi",
    "monday": "balaza",
    "tuesday": "wakubiri",
    "wednesday": "wakusatu",
    "thursday": "wakuna",
    "friday": "wakutaano",
    "saturday": "lwomukaaga",
    "sunday": "ssande",
}

WORDBOOK = {
    "i": "nze", "you": "ggwe", "we": "ffe", "they": "bo", "my": "wange",
    "your": "wo", "this": "kino", "that": "ekyo", "is": "ye", "are": "oli",
    "am": "ndi", "want": "njagala", "need": "netaaga", "like": "njagala",
    "know": "manyi", "understand": "tegeera", "come": "jja", "go": "genda",
    "eat": "lya", "drink": "nywa", "today": "leero", "tomorrow": "enkya",
    "water": "amazzi", "food": "emmere", "home": "eka", "friend": "mukwano",
    "and": "ne", "please": "nsaba", "or": "oba", "but": "naye",
    "not": "si", "very": "nyo", "more": "okusingawo",
    "good": "lungi", "bad": "bubi", "big": "nene", "small": "tono",
    "new": "pya", "old": "kadde", "hot": "buguma", "cold": "nyogoga",
    "happy": "sanyufu", "sad": "munyiivu", "beautiful": "lungi",
    "man": "musajja", "woman": "mukyala", "child": "mwana", "children": "abaana",
    "mother": "maama", "father": "taata", "son": "mutabani", "daughter": "muwala",
    "brother": "ow'oluganda", "sister": "ow'oluganda", "family": "amaka",
    "person": "muntu", "people": "abantu", "name": "linnya", "language": "lulimi",
    "country": "eggwanga", "city": "kibuga", "village": "kyalo",
    "market": "katale", "shop": "duuka", "hotel": "hoteeri", "hospital": "ddwaliro",
    "school": "ssomero", "church": "kanisa", "office": "ofesi", "bank": "bbanka",
    "road": "kkubo", "street": "luguudo", "car": "mottoka", "bus": "bbaasi",
    "taxi": "takisi", "airport": "kisaawe", "ticket": "tikiti", "money": "sente",
    "price": "beeyi", "time": "saawa", "day": "lunaku", "week": "wiiki",
    "month": "mwezi", "year": "mwaka", "morning": "makya", "evening": "akawungeezi",
    "night": "kibululu", "later": "olulala", "before": "nga tonnaba", "after": "oluvannyuma",
    "here": "wano", "there": "wali", "left": "kkono", "right": "ddyo", "straight": "butereevu",
    "near": "kumpi", "far": "wala", "inside": "munda", "outside": "wabweru",
    "open": "ggulawo", "close": "ggalawo", "wait": "lindirira", "listen": "wuliriza",
    "speak": "yogera", "read": "soma", "write": "wandiika", "work": "kola",
    "live": "beera", "stay": "sula", "buy": "gula", "sell": "tunda", "pay": "sasula",
    "give": "wa", "take": "twala", "bring": "leeta", "see": "laba", "look": "tunuulira",
    "tell": "gamba", "ask": "buuza", "answer": "ddamu", "call": "kuba",
    "learn": "yiga", "teach": "yigiriza", "remember": "jjukira", "forget": "weerabira",
    "love": "kwagala", "feel": "wulira", "sleep": "sula", "sit": "tuula", "stand": "yimirira",
    "walk": "tambula", "run": "dduka", "turn": "kuba", "stop": "yimirira",
    "one": "emu", "two": "bbiri", "three": "ssatu", "four": "nnya", "five": "ttaano",
    "six": "mukaaga", "seven": "musanvu", "eight": "munana", "nine": "mwenda", "ten": "kkumi",
    "red": "myufu", "blue": "bbulu", "green": "kiragala", "yellow": "kyenvu", "black": "nzirugavu",
    "white": "weru", "brown": "kitaka",
}


def load_translation_data() -> None:
    data_path = Path(__file__).parent / "data" / "translations.json"
    try:
        with data_path.open(encoding="utf-8") as data_file:
            data = json.load(data_file)
    except (OSError, json.JSONDecodeError):
        return

    phrase_keys = set()
    for entry in data.get("phrases", []):
        english = str(entry.get("en", "")).strip().lower()
        luganda = str(entry.get("lg", "")).strip()
        if english and luganda:
            phrase_keys.add(english)
            PHRASEBOOK[english] = luganda

    for entry in data.get("words", []):
        english = str(entry.get("en", "")).strip().lower()
        luganda = str(entry.get("lg", "")).strip()
        if english and luganda:
            WORDBOOK[english] = luganda
            if english not in phrase_keys:
                PHRASEBOOK.pop(english, None)


load_translation_data()


def local_translate(text: str) -> tuple[str, str]:
    normalized = " ".join(text.lower().strip().split())
    if normalized in PHRASEBOOK:
        return PHRASEBOOK[normalized], "Phrasebook match"
    if " " not in normalized and normalized in WORDBOOK:
        return WORDBOOK[normalized], "Phrasebook word match"
    words = normalized.split(" ")
    translated = []
    matched = 0
    for word in words:
        clean_word = word.strip(".,!?;:")
        translated_word = WORDBOOK.get(clean_word)
        if translated_word:
            matched += 1
            translated.append(word.replace(clean_word, translated_word, 1))
        else:
            translated.append(word)
    if matched:
        return " ".join(translated), f"Offline word match ({matched}/{len(words)} words)"
    return "", ""


def online_translate(text: str) -> str:
    query = urllib.parse.urlencode({"q": text, "langpair": "en|lg"})
    request = urllib.request.Request(
        f"https://api.mymemory.translated.net/get?{query}",
        headers={"User-Agent": "LugandaBridge/1.0"},
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        payload = json.loads(response.read().decode("utf-8"))
    result = payload.get("responseData", {}).get("translatedText", "").strip()
    if not result or result.upper() == text.upper():
        raise ValueError("No translated result returned")
    return html.unescape(result)


def translate(text: str, use_online: bool) -> tuple[str, str]:
    if use_online:
        try:
            return online_translate(text), "MyMemory online translation"
        except Exception:
            local_result, source = local_translate(text)
            if local_result:
                return local_result, f"Online unavailable; {source.lower()}"
    local_result, source = local_translate(text)
    if local_result:
        return local_result, source
    return "Translation unavailable offline. Try a common phrase or enable online translation.", "Offline fallback"


def add_to_history(source: str, result: str, method: str) -> None:
    st.session_state.history.insert(0, {
        "source": source, "result": result, "method": method,
        "time": datetime.now().strftime("%H:%M"),
    })
    st.session_state.history = st.session_state.history[:5]


if "history" not in st.session_state:
    st.session_state.history = []
if "source_text" not in st.session_state:
    st.session_state.source_text = ""
if "translation" not in st.session_state:
    st.session_state.translation = ""
if "method" not in st.session_state:
    st.session_state.method = ""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap');
:root { --ink: #173f3b; --mint: #dcefe7; --coral: #e86f51; --cream: #fbf7ef; --line: #c7ddd3; }
.stApp { background: var(--cream); color: var(--ink); }
.block-container { max-width: 850px; padding: 4rem 1.25rem 3rem; }
h1, h2, h3, p, label, .stMarkdown { font-family: 'Manrope', sans-serif; }
h1 { font-size: clamp(2.5rem, 7vw, 5.4rem); line-height: .95; letter-spacing: -0.04em; color: var(--ink); margin-bottom: .8rem; }
.eyebrow { color: var(--coral); font: 500 .78rem 'DM Mono', monospace; letter-spacing: .12em; text-transform: uppercase; }
.intro { max-width: 600px; color: #52736c; font-size: 1.05rem; line-height: 1.6; margin-bottom: 2.2rem; }
.panel { border: 1px solid var(--line); background: #fffdf8; padding: 1.3rem; border-radius: 8px; box-shadow: 7px 7px 0 #cce3d9; }
.result { min-height: 125px; border: 1px solid var(--line); background: var(--mint); padding: 1.2rem 1.3rem; border-radius: 8px; margin-top: 1rem; }
.result-label { font: 500 .72rem 'DM Mono', monospace; text-transform: uppercase; letter-spacing: .1em; color: #47736a; }
.result-text { color: var(--ink); font: 700 1.45rem 'Manrope', sans-serif; margin-top: .6rem; }
.stTextArea textarea { background: #fffdf8; border: 1px solid var(--line); color: var(--ink); font: 1rem 'Manrope', sans-serif; }
.stButton button { border-radius: 5px; border: 1px solid var(--ink); font-family: 'Manrope', sans-serif; font-weight: 700; }
.stButton button[kind='primary'] { background: var(--coral); border-color: var(--coral); color: white; }
.history-item { border-top: 1px solid var(--line); padding: .75rem 0; }
.history-source { color: #52736c; font-size: .82rem; }
.history-result { color: var(--ink); font-weight: 700; margin-top: .2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="eyebrow">English / Luganda</div>', unsafe_allow_html=True)
st.title("Luganda Bridge")
st.markdown('<p class="intro">A small, friendly translator for moving everyday English into Luganda. Start with a phrase, then make it yours.</p>', unsafe_allow_html=True)

with st.container(border=False):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    source = st.text_area("English", value=st.session_state.source_text, height=150, placeholder="Type something like: Good morning, how are you?")
    controls = st.columns([1.4, 1, 1])
    with controls[0]:
        translate_clicked = st.button("Translate to Luganda", type="primary", use_container_width=True)
    with controls[1]:
        online = st.toggle("Online translation", value=True, help="Try MyMemory first, then use the offline dictionary if it is unavailable.")
    with controls[2]:
        clear_clicked = st.button("Clear", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if clear_clicked:
    st.session_state.source_text = ""
    st.session_state.translation = ""
    st.session_state.method = ""
    st.rerun()

if translate_clicked:
    if not source.strip():
        st.warning("Enter an English phrase first.")
    else:
        result, method = translate(source, online)
        st.session_state.source_text = source
        st.session_state.translation = result
        st.session_state.method = method
        add_to_history(source, result, method)

if st.session_state.translation:
    st.markdown(f'<div class="result"><div class="result-label">Luganda</div><div class="result-text">{html.escape(st.session_state.translation)}</div><div class="result-label" style="margin-top:.9rem">{html.escape(st.session_state.method)}</div></div>', unsafe_allow_html=True)

with st.expander("Recent translations", expanded=bool(st.session_state.history)):
    if not st.session_state.history:
        st.caption("Your recent translations will appear here.")
    for item in st.session_state.history:
        st.markdown(f'<div class="history-item"><div class="history-source">{html.escape(item["source"])} <span>at {item["time"]}</span></div><div class="history-result">{html.escape(item["result"])}</div></div>', unsafe_allow_html=True)

st.caption("Offline phrasebook included. Online results use the MyMemory translation service.")
