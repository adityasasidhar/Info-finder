import re
import requests
from bs4 import BeautifulSoup
from newspaper import Article

def get_clean_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip() if article.text else "No text found."
    except Exception:
        return "Failed to fetch article text."

def is_url(text):
    url_pattern = re.compile(
        r"^(https?|ftp)://[^\s/$.?#].\S*$", re.IGNORECASE
    )
    return bool(url_pattern.match(text))

def check_url(url):
    suspicious_patterns = [
        r"[a-zA-Z0-9-]+\.(xyz|top|click|info|biz|gq|cf|tk|ml|ga|men|work|trade|loan)$",
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        r"(free|cheap|offer|win|bonus|prize|gift|reward|lottery|promo|hotdeal|discount|earnmoney|paynow|"
        r"fastcash|creditcard|bitcoin|forex|hack|unblock|download|crack|keygen|serial|giveaway|payperclick)\.",
    ]
    if any(re.search(pattern, url) for pattern in suspicious_patterns):
        return "unsafe (offline heuristic check)"
    return "safe"

def fetch_webpage(url, timeout=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "iframe", "img", "video", "audio", "svg", "noscript", "aside", "footer"]):
        tag.decompose()

    main_content = soup.find("article") or soup.find("main") or soup.find("div", class_="content")
    elements = main_content.find_all(["p", "h1", "h2", "h3", "li", "blockquote"]) if main_content else soup.find_all(["p", "h1", "h2", "h3", "li", "blockquote"])

    content = []
    for elem in elements:
        text = elem.get_text(strip=True)
        if text:
            if elem.name in ["h1", "h2", "h3"]:
                content.append(f"\n{text}\n")
            elif elem.name == "li":
                content.append(f"• {text}")
            else:
                content.append(text)
    clean_text = "\n".join(content)
    return clean_text if clean_text else "No text content found."

def getarticle_text(url):
    html = fetch_webpage(url)
    if html:
        return extract_text_from_html(html)
    return "Failed to fetch article text."

def search_duckduckgo(query, num_results=1):
    query = query.replace(" ", "+")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    blocked_domains = [
        "amazon.", "flipkart.", "ebay.", "aliexpress.", "walmart.", "etsy.", "bestbuy.", "target.",
        "rakuten.", "newegg.", "shein.", "wayfair.", "overstock.", "zalando.", "mercari.", "poshmark.",
        "bigcommerce.", "shopify.", "groupon.", "kohls.", "macys.", "homedepot.", "lowes.", "costco.",
        "samsclub.", "chewy.", "asos.", "boohoo.", "prettylittlething.", "zappos.", "modcloth.", "lulus.",
        "urbanoutfitters.", "hollisterco.", "abercrombie.", "victoriassecret.", "nordstrom.", "sephora.",
        "ulta.", "bhphotovideo.", "adorama.", "microcenter.", "gamestop.", "nike.", "adidas.", "puma.",
        "reebok.", "underarmour.", "lulu.", "levi.", "timberland.", "clarks.", "crocs.", "drmartens.",
        "fossil.", "swatch.", "ray-ban.", "oakley.", "warbyparker.", "wayfair.", "pier1.", "ashleyfurniture.",
        "rooms-to-go.", "ikea.", "cb2.", "westelm.", "crateandbarrel.", "bedbathandbeyond.", "staples.",
        "officedepot.", "paperchase.", "michaels.", "hobbylobby.", "joann.", "partycity.", "shutterfly.",
        "vistaprint.", "snapfish.", "redbubble.", "society6.", "cafepress.", "teepublic.", "spreadshirt.",
        "zazzle.", "moonpig.", "funkypigeon.", "bluenile.", "jamesallen.", "kay.", "zales.", "tiffany.",
        "pandora.", "cartier.", "chanel.", "gucci.", "prada.", "louisvuitton.", "burberry.", "hermes.",
        "versace.", "dior.", "armani.", "ralphlauren.", "balenciaga.", "montblanc.", "swarovski.", "tagheuer.",
        "facebook.", "twitter.", "instagram.", "linkedin.", "tiktok.", "reddit.", "pinterest.",
        "snapchat.", "tumblr.", "discord.", "threads.", "onlyfans.", "quora.", "weibo.", "wechat.",
        "buzzfeed.", "dailystar.", "mirror.", "thethings.", "thelist.", "infowars.", "beforeitsnews.",
        "naturalnews.", "sputniknews.", "rt.", "newsmax.", "theblaze.", "yournewswire.", "zerohedge.",
        "zergnet.", "boredpanda.", "viralnova.", "clickhole.", "diply.", "ranker.", "upworthy.",
        "patheos.", "yourtango.", "babylonbee.", "worldtruth.tv.", "softonic.", "cnet.com/downloads",
        "freedownloadmanager.", "getintopc.", "download.cnet.", "filehippo.", "softpedia.", "crackstreams.",
        "freetrialdownloads.", "warez-bb.", "filehorse.", "tucowsdownloads.", "oceanofgames.", "gameslopedy.",
        "igggames.", "breitbart.", "thegatewaypundit.", "msnbc.", "huffpost.", "foxnews.", "oann.", "theintercept.",
        "dailywire.", "motherjones.", "rawstory.", "newstarget.", "thepiratebay.", "1337x.", "silkroadxx.",
        "crackserialkey.", "rarbg.", "yts.", "limetorrents.", "kickasstorrents.", "proxyrarbg.", "extratorrent.",
        "zippyshare.", "torrentz2.", "torrentdownloads.", "nzbplanet.", "warez-bb.", "ddlvalley.", "katcr.co.",
        "bet365.", "pokerstars.", "fanduel.", "draftkings.", "bovada.", "888casino.", "stake.", "unibet.",
        "williamhill.", "betfair.", "sportsbetting.", "ladbrokes.", "paddypower.", "dafabet.", "pornhub.",
        "xvideos.", "xnxx.", "redtube.", "youporn.", "brazzers.", "chaturbate.", "onlyfans.", "camsoda.",
        "erome.", "hclips.", "hentaihaven.", "f95zone.", "bitconnect.", "onecoin.", "usitech.", "gainbitcoin.",
        "hyperfund.", "forsage.", "cashfxgroup.", "mirrortradinginternational.", "trustinvesting.", "arbitraging.co.",
        "hidemyass.", "protonvpn.", "nordvpn.", "expressvpn.", "surfshark.", "cyberghostvpn.", "privateinternetaccess.",
        "windscribe.", "tunnelbear.", "vpnunlimited.", "hotspotshield.", "freedom-vpn.", "hackforums.", "nulled.",
        "cracked.to.", "exploit-db.", "0day.today.", "raidforums.", "breachforums.", "dark0de.", "hackthissite.",
        "shadowforums.", "antichat.", "blackhatworld.", "crackingforum.", "freegiftcards.", "winiphone.",
        "click4money.", "earnbitcoinfast.", "surveys-for-cash.", "claimprizes.", "lotterywinner.", "getrichquick.",
        "win-free-iphone.", "instantmillionaire.", "bitcoindoubler.", "fiverr.", "upwork.", "freelancer.", "99designs.",
        "peopleperhour.", "toptal.", "guru.", "taskrabbit.", "zeerk.", "workana.", "weworkremotely.", "truelancer.",
        "hubstafftalent.", "twago.", "flexjobs."
    ]

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.find_all("div", class_="result"):
            if "result--ad" in result.get("class", []) or "result__sponsored" in result.get("class", []):
                continue

            link_tag = result.find("a", class_="result__url")
            if link_tag:
                url = "https://" + link_tag.text.strip()
                if any(blocked in url for blocked in blocked_domains):
                    continue
                results.append(url)
                if len(results) >= num_results:
                    break

        return results
    return []

def create_search_url(query):
    query = query.replace(" ", "+")
    return f"https://html.duckduckgo.com/html/?q={query}"

def create_context(text):
    if is_url(text):
        url = text
        if check_url(url) == "safe":
            article_text = get_clean_article_text(url)
            return f"Content from {url}:\n{article_text}"
        else:
            return "The URL is unsafe."
    else:
        search_results = search_duckduckgo(text, num_results=5)
        if not search_results:
            return "No results found."

        combined_content = [f"Search results for '{text}':"]
        for url in search_results:
            if check_url(url) == "safe":
                article_text = get_clean_article_text(url)
                combined_content.append(f"\nContent from {url}:\n{article_text}")
            else:
                combined_content.append(f"\nContent from {url}:\nThe URL is unsafe.")

        return "\n".join(combined_content)
