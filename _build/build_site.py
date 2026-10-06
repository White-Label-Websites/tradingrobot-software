# Generates the static pages of a sober satellite site (home, contact, legal
# pages, sitemap, robots.txt) from the SITE config below.
# Run from anywhere: python3 _build/build_site.py
# Rules (Rami, 2026-10-05): simple, clear, no promise of gains; never use the
# words scam / review / legit, never show another brand's name or logo.
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "5 October 2026"

SITE = {'domain': 'tradingrobot.software',
 'brand': 'Trading Robot',
 'script': 183,
 'ga': '',
 'theme': '#f2f4ee',
 'title': 'Build a Trading Robot and Test It on Live Prices, Free | Trading Robot',
 'desc': 'Set up a trading robot and run it on live market prices with a virtual $10,000 under fixed risk '
         'limits. Free: no card, no deposit.',
 'tag': 'Trading robot workshop',
 'h1': 'Build a trading robot. <mark>Test it on live prices with a virtual $10,000.</mark>',
 'intro': 'Choose a market and set your robot&rsquo;s rules. Then let it trade live prices with a virtual '
          '$10,000, under risk limits it cannot negotiate with.',
 'join': 'Set up your first robot',
 'how_title': 'From a trading idea to a live robot in four steps',
 'stages': [('Choose a market', 'Pick the instrument your robot will trade.'),
            ('Set the rules', 'Entry, exit and how much of the balance each trade uses.'),
            ('Run it live', 'Your robot trades live prices with a virtual $10,000. No card, no deposit.'),
            ('Climb or rebuild',
             'Hit the target to move up a level. Break a limit and the challenge ends, so you adjust the '
             'rules and start again.')],
 'faq': [('What is a trading robot?',
          'A program that places buy and sell orders on its own, following rules set in advance. Robot, bot '
          'and algorithm mean the same thing here.'),
         ('How long does a test last?',
          'Level 1 lasts between 5 and 10 days. Level 2 needs at least 5 days and has no end date. Level 3 '
          'has neither a minimum nor a deadline.')],
 'closing': 'Have a trading idea? Turn it into a robot and watch it trade.',
 'risk': 'Trading is high risk.'}

D = SITE["domain"]; B = SITE["brand"]; URL = f"https://{D}"

FOOTER = f"""<footer class="foot">
  <div class="wrap">
    <nav aria-label="Footer"><a href="/contact/">Contact</a><a href="/terms/">Terms</a><a href="/privacy-policy/">Privacy</a><a href="/legal-notice/">Legal notice</a><a href="/privacy-policy/#cookies" data-cookie-settings>Cookie settings</a></nav>
    <p class="copy">&copy; 2026 {B}</p>
    <small>Educational simulator. All balances are virtual and no real money is traded. Nothing on this site is financial advice. {SITE["risk"]} Results on virtual money do not predict real results. Sign-up is handled by our partner AFFCOIN, and we may receive a commission when you open an account.</small>
  </div>
</footer>"""

HEADER = f"""<header class="bar">
  <div class="wrap">
    <a class="logo" href="/"><span class="logo-glyph" aria-hidden="true"></span>{B}</a>
    <nav aria-label="Main"><a href="/#how">How it works</a><a class="hide-sm" href="/#rules">The rules</a><a href="/contact/">Contact</a></nav>
  </div>
</header>"""

def head(title, desc, path, jsonld=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{URL}/{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{URL}/{path}">
<meta property="og:type" content="website">
<meta name="theme-color" content="{SITE["theme"]}">
<link rel="preload" href="/assets/fonts/BricolageGrotesque-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/consent.js" data-ga="{SITE["ga"]}"></script>
{jsonld}</head>
<body>
"""

def write(path, html):
    full = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(html)

LEVELS = """      <table>
        <thead><tr><th>Level</th><th>Target</th><th>Min. days</th><th>Max. days</th><th>Max. drawdown</th><th>Daily drawdown</th></tr></thead>
        <tbody>
          <tr><td>Level 1</td><td>+10%</td><td>5</td><td>10</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 2</td><td>+5%</td><td>5</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 3</td><td>+5%</td><td>None</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
        </tbody>
      </table>"""

# ---------------------------------------------------------------- home
faq = SITE["faq"] + [
    ("How much does it cost?", "Nothing. Opening an account asks for no card and no deposit."),
    ("Can I win or lose real money?", "No. Every robot trades a virtual balance. There is no deposit, no withdrawal and no payout: the only thing at stake is your strategy's record."),
    ("What stops a test early?", "A loss of 5% in a single day, or a total drawdown of 10%. Either one ends the challenge on the spot."),
    ("Can I test more than one robot?", "Yes. Each robot gets its own virtual $10,000 balance, so you can compare versions of a strategy side by side."),
]
faq_ld = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False) + "\n</script>\n"
HERE = ' class="here"'
stages = "\n".join(f'      <li{HERE if i == 3 else ""}><span class="stage-n">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(SITE["stages"]))
qa = "\n".join(f'      <details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq))

home = head(SITE["title"], SITE["desc"], "", faq_ld) + HEADER + f"""

<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="tag fade">{SITE["tag"]} <span>Free</span></p>
      <h1 class="fade f1">{SITE["h1"]}</h1>
      <p class="intro fade f2">{SITE["intro"]}</p>
      <figure class="curve fade f3" aria-labelledby="curve-cap">
        <svg viewBox="0 0 560 230" role="img" aria-label="Illustration: a robot's virtual balance on live prices, between a +10% target and a -10% limit">
          <line class="c-target" x1="0" y1="42" x2="560" y2="42"/>
          <line class="c-limit" x1="0" y1="192" x2="560" y2="192"/>
          <line class="c-zero" x1="0" y1="117" x2="560" y2="117"/>
          <polyline class="c-live" points="0,117 28,121 56,112 84,116 112,104 140,110 168,99 196,105 224,94 252,100 280,90 308,97 336,88 364,95 392,84 420,90 448,80 476,87 504,76"/>
          <circle class="c-dot" cx="504" cy="76" r="6"/>
          <text class="c-lab c-lab-live" x="10" y="24">LIVE PRICES &middot; VIRTUAL $10,000</text>
          <text class="c-val c-val-t" x="552" y="36" text-anchor="end">+10% target</text>
          <text class="c-val c-val-r" x="552" y="210" text-anchor="end">-10% limit</text>
        </svg>
        <figcaption id="curve-cap">Illustration only. Every robot starts at a virtual $10,000; no real money is involved.</figcaption>
      </figure>
    </div>
    <aside class="join fade f2" id="start" aria-labelledby="join-title">
      <div class="join-head">
        <h2 id="join-title">{SITE["join"]}</h2>
        <p>Free account &middot; no card &middot; no deposit</p>
      </div>
      <div class="wl-signup"></div>
    </aside>
  </div>
</section>

<section class="pipeline" id="how" aria-labelledby="pipe-title">
  <div class="wrap">
    <div class="head">
      <p class="label">How it works</p>
      <h2 class="title" id="pipe-title">{SITE["how_title"]}</h2>
    </div>
    <ol class="stages">
{stages}
    </ol>
  </div>
</section>

<section class="levels" id="rules" aria-labelledby="levels-title">
  <div class="wrap">
    <div class="head">
      <p class="label">The rules</p>
      <h2 class="title" id="levels-title">Three levels, one set of limits</h2>
      <p class="sub">Targets get smaller as the robot climbs. The limits never move, so a steady strategy goes further than a lucky one.</p>
    </div>
    <div class="lv-grid">
      <article class="lv"><p class="lv-n">Level 1</p><p class="lv-goal">+10%</p><p class="lv-name">Prove it</p><ul><li><span>Minimum</span>5 days</li><li><span>Maximum</span>10 days</li></ul></article>
      <article class="lv"><p class="lv-n">Level 2</p><p class="lv-goal">+5%</p><p class="lv-name">Repeat it</p><ul><li><span>Minimum</span>5 days</li><li><span>Maximum</span>No limit</li></ul></article>
      <article class="lv"><p class="lv-n">Level 3</p><p class="lv-goal">+5%</p><p class="lv-name">Hold it</p><ul><li><span>Minimum</span>None</li><li><span>Maximum</span>No limit</li></ul></article>
    </div>
    <div class="limits" role="note">
      <p><b>-10%</b> maximum drawdown</p>
      <p><b>-5%</b> daily drawdown</p>
      <p class="stop">Breaking either one ends the challenge immediately.</p>
    </div>
    <p class="actions"><a class="btn" href="#start">Create my free account <span aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>

<section class="faq" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="head">
      <p class="label">Questions</p>
      <h2 class="title" id="faq-title">Before your robot goes live</h2>
    </div>
    <div class="qa">
{qa}
      <details><summary>Who runs this site?</summary><p>An independent publisher. See the <a href="/legal-notice/">legal notice</a>, or write to us through the <a href="/contact/">contact page</a>.</p></details>
    </div>
  </div>
</section>

<section class="closing">
  <div class="wrap">
    <h2>{SITE["closing"]}</h2>
    <a class="btn btn-light" href="#start">Create my free account <span aria-hidden="true">&rarr;</span></a>
  </div>
</section>
</main>

{FOOTER}

<script src="/assets/site.js" defer></script>
<script src="https://affcoin.com/products/scripts/{SITE["script"]}/" defer></script>
</body>
</html>
"""
write("", home)

# ---------------------------------------------------------------- inner pages
def page(slug, kicker, h1, title, desc, body, scripts="", updated=True):
    upd = f'      <p class="updated">Last updated: {UPDATED}</p>\n' if updated else ""
    html = head(title, desc, slug + "/") + HEADER + f"""

<main class="page">
  <div class="wrap">
    <div class="page-head">
      <p class="label">{kicker}</p>
      <h1>{h1}</h1>
{upd}    </div>
    <div class="prose">
{body}
    </div>
  </div>
</main>

{FOOTER}
{scripts}</body>
</html>
"""
    write(slug, html)

page("contact", "Contact", f"Talk to the {B} team", f"Contact | {B}",
  f"Questions about the challenges, your virtual balance or the rules? Send the {B} team a message and we will reply by email.",
  f"""      <p>Questions about a challenge, the rules or how your robot is evaluated? Send us a message and we will reply by email, usually within two working days.</p>
      <form class="cform" id="cform" novalidate>
        <div class="row">
          <label>Name<input name="name" type="text" autocomplete="name" maxlength="100" required></label>
          <label>Email<input name="email" type="email" autocomplete="email" maxlength="200" required></label>
        </div>
        <label>Message<textarea name="message" maxlength="5000" required></textarea></label>
        <div class="hp" aria-hidden="true"><label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
        <button class="btn" type="submit">Send message <span aria-hidden="true">&rarr;</span></button>
        <p class="cform-status" role="status" aria-live="polite"></p>
      </form>
      <h2>Login, password or verification code</h2>
      <p>Accounts are handled by our partner AFFCOIN. For a lost password, a verification code that never arrived or a request about your account data, you can also write to <a href="mailto:support@affcoin.com">support@affcoin.com</a>.</p>
      <div class="callout"><p><strong>We will never ask you for money, a card number or a wallet.</strong> Every balance on {B} is virtual. If someone contacts you on our behalf and asks for a payment, it is not us.</p></div>""",
  scripts="""<script>
(function(){
  var f=document.getElementById("cform");if(!f)return;
  var st=f.querySelector(".cform-status"),btn=f.querySelector("button");
  function show(msg,cls){st.textContent=msg;st.className="cform-status "+(cls||"")}
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var d={name:f.name.value.trim(),email:f.email.value.trim(),message:f.message.value.trim(),website:f.website.value};
    if(!d.name||!d.message||!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(d.email)){show("Please fill in your name, a valid email and a message.","err");return}
    btn.disabled=true;show("Sending...");
    fetch("https://bitcoinera-contact.martinratinaud.workers.dev",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)})
      .then(function(r){return r.json().then(function(j){return{ok:r.ok&&j.ok,j:j}})})
      .then(function(res){if(res.ok){f.reset();show("Thanks, your message has been sent. We will reply by email.","ok")}else{show(res.j.error||"Message could not be sent. Please try again later.","err")}})
      .catch(function(){show("Message could not be sent. Please try again later.","err")})
      .then(function(){btn.disabled=false});
  });
})();
</script>
""", updated=False)

# TODO before going live: replace the publisher block with the legal entity.
page("legal-notice", "Legal", "Legal notice", f"Legal notice | {B}",
  f"Who publishes {D}, who hosts it, who runs the trading accounts and how to reach us.",
  f"""      <h2>Publisher</h2>
      <dl class="facts">
        <dt>Site</dt><dd>{D}</dd>
        <!-- TODO: legal entity, registration number and registered address of the publisher -->
        <dt>Publisher</dt><dd>{B}, independent publisher and owner of the {D} domain name</dd>
        <dt>Contact</dt><dd><a href="/contact/">Contact form</a></dd>
      </dl>
      <h2>Hosting</h2>
      <dl class="facts">
        <dt>Host</dt><dd>GitHub, Inc. (GitHub Pages)</dd>
        <dt>Address</dt><dd>88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States</dd>
        <dt>Contact form relay</dt><dd>Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, United States</dd>
      </dl>
      <h2>Accounts and affiliate disclosure</h2>
      <p>Account creation and login are handled by our partner AFFCOIN, an affiliate network. We may receive a commission when you open an account through this site. This never costs you anything, since the challenge is free. AFFCOIN can be reached at <a href="https://affcoin.com/" rel="nofollow noopener" target="_blank">affcoin.com</a> and <a href="mailto:contact@affcoin.com">contact@affcoin.com</a>. The data you enter in the sign-up form is sent directly to AFFCOIN and handled under <a href="https://affcoin.com/privacy" rel="nofollow noopener" target="_blank">its privacy policy</a>.</p>
      <h2>Not financial advice</h2>
      <p>{B} is an educational simulator. Every balance is virtual, no real money is traded and nothing on this site is investment, financial or tax advice. Results achieved with virtual money do not predict results with real money. {SITE["risk"]}</p>
      <h2>Intellectual property</h2>
      <p>The texts, design and code of this site belong to the publisher unless stated otherwise.</p>""")

page("privacy-policy", "Legal", "Privacy policy", f"Privacy policy | {B}",
  f"What personal data {D} collects, why, who receives it, how long it is kept and how to exercise your rights.",
  f"""      <p>This policy explains what happens to your personal data when you visit {D}, write to us or open an account. We collect as little as we can.</p>
      <h2>1. Who is responsible</h2>
      <p>The publisher of {D} (see the <a href="/legal-notice/">legal notice</a>) is responsible for the data collected through this site&rsquo;s contact form. Data entered in the sign-up form is collected on this page and sent directly to our partner AFFCOIN. For that collection and transfer we act together with AFFCOIN; AFFCOIN then handles your account and is responsible for it under <a href="https://affcoin.com/privacy" rel="nofollow noopener" target="_blank">its own privacy policy</a>. You can exercise your rights with either of us.</p>
      <h2>2. What we collect and why</h2>
      <table>
        <thead><tr><th>When</th><th>Data</th><th>Purpose</th><th>Legal basis</th></tr></thead>
        <tbody>
          <tr><td>You use the contact form</td><td>Name, email, message</td><td>Answer your message</td><td>Legitimate interest, or steps before a contract</td></tr>
          <tr><td>You open an account</td><td>First and last name, email, password, phone number, newsletter choice</td><td>Create and run your challenge account, verify it, and send you news if you opted in (handled by AFFCOIN)</td><td>Contract; consent for the newsletter</td></tr>
          <tr><td>You visit any page</td><td>IP address, browser, pages requested (technical logs)</td><td>Deliver the site and keep it secure</td><td>Legitimate interest</td></tr>
        </tbody>
      </table>
      <p>We do not sell your data and we do not run advertising trackers on this site. Analytics only uses cookies if you accept them (see section 5).</p>
      <h2>3. Who receives it</h2>
      <ul>
        <li><strong>AFFCOIN</strong> and the providers it works with, for everything you type in the sign-up form, sent directly from your browser to its servers.</li>
        <li><strong>Cloudflare</strong>, which relays contact-form messages to our mailbox.</li>
        <li><strong>GitHub</strong>, which hosts the site and keeps technical access logs.</li>
        <li><strong>Google</strong> (Google Analytics), only if you accept analytics cookies: pages viewed, approximate location, device and browser, used to count visits. IP addresses are not stored by Google Analytics 4. Data may be processed in the United States under the EU-US Data Privacy Framework.</li>
      </ul>
      <p>Some of these providers are based in the United States. Transfers rely on the safeguards they offer, such as the EU-US Data Privacy Framework or standard contractual clauses.</p>
      <h2>4. How long we keep it</h2>
      <p>Contact messages are kept for up to 3 years after our last exchange, then deleted. Account data is kept by AFFCOIN for as long as your account is open and then according to its policy.</p>
      <h2 id="cookies">5. Cookies</h2>
      <p>We use Google Analytics cookies (<code>_ga</code>, <code>_ga_*</code>, kept up to 13 months) to count visits and see which pages are useful. They are set only after you click &ldquo;Accept&rdquo; in the cookie banner. If you decline, Google Analytics runs without cookies and receives no identifier for you. We do not use advertising cookies. Your choice is stored in your browser and you can change it at any time with the <a href="/privacy-policy/#cookies" data-cookie-settings>cookie settings</a> link at the bottom of every page.</p>
      <p>Our fonts are served from our own host. The sign-up widget, loaded from affcoin.com, may store what it needs to run the form and your session. Those cookies are covered by AFFCOIN&rsquo;s policy.</p>
      <h2>6. Your rights</h2>
      <p>You can ask to access, correct or delete your data, object to its use, restrict it, or receive a copy. To exercise a right, use our <a href="/contact/">contact form</a>, or write to <a href="mailto:support@affcoin.com">support@affcoin.com</a> for account data. You can also complain to your data protection authority.</p>
      <h2>7. Changes</h2>
      <p>We will update this page when our practices change. The date at the top shows the latest version.</p>""")

page("terms", "Legal", "Terms of use", f"Terms of use | {B}",
  f"The rules for using {D} and taking part in the virtual trading robot challenges.",
  f"""      <p>By using {D} or opening an account through it, you accept these terms. If you do not agree with them, please do not use the site.</p>
      <h2>1. What {B} is</h2>
      <p>{B} is an educational simulator. You set up a trading robot, run it on live market prices with a <strong>virtual balance of $10,000</strong>, and try to clear three levels. No real money is deposited, traded or won, and the virtual balance has no cash value.</p>
      <h2>2. Who can join</h2>
      <p>You must be at least 18 years old and allowed to use this kind of service where you live. One person, one account. The information you give when signing up must be accurate.</p>
      <h2>3. Your account</h2>
      <p>Accounts are created and run by our partner AFFCOIN, whose own terms also apply. We may receive a commission when you open an account. Keep your password private. You are responsible for what happens under your account.</p>
      <h2>4. Challenge rules</h2>
{LEVELS}
      <p>Breaching the daily or the maximum drawdown ends the challenge immediately. We may adjust the rules for future challenges; a challenge already running keeps the rules it started with.</p>
      <h2>5. Fair use</h2>
      <p>Do not exploit bugs, price-feed errors or latency, share accounts, use several accounts to game the levels, or attack the platform. We may suspend an account that breaks these rules.</p>
      <h2>6. No financial advice, no guarantee</h2>
      <p>Nothing on {B} is investment, financial or tax advice. Performance on virtual money does not predict results on real money. {SITE["risk"]} The service is provided as is, and may be interrupted for maintenance.</p>
      <h2>7. Liability</h2>
      <p>Since no real money is at stake, we are not liable for any trading decision you take outside {B}, or for any loss arising from it. Nothing in these terms limits liability that cannot legally be limited.</p>
      <h2>8. Personal data</h2>
      <p>See our <a href="/privacy-policy/">privacy policy</a>.</p>
      <h2>9. Changes and contact</h2>
      <p>We may update these terms; the date at the top shows the current version. Questions: <a href="/contact/">contact us</a>.</p>""")

urls = [("", "1.0"), ("contact/", "0.3"), ("legal-notice/", "0.3"), ("privacy-policy/", "0.3"), ("terms/", "0.3")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{URL}/{u}</loc><lastmod>2026-10-05</lastmod><priority>{p}</priority></url>\n" for u, p in urls)
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /app/\n\nSitemap: {URL}/sitemap.xml\n")
print("built", D)
