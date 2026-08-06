# Joe — Mobile Auto Repair

A one-page site for Joe, who does auto repair at the customer's place and has no
shop. It's built to be **shown**: Joe pulls it up on his phone when he's pitching
someone, and it answers "what do you actually do?" without him having to list it.

`index.html` is the whole site. One file, no build step, no dependencies, no
server, no network requests at all. Double-click it to open it.

---

## Change Joe's details

Open `index.html`, scroll to the bottom, find this block:

```js
const BIZ = {
  phone   : "+12535616361",
  display : "(253) 561-6361",
  area    : "CONFIRM_WITH_JOE",
  hours   : "CONFIRM_WITH_JOE",
};
```

Anything left as `CONFIRM_WITH_JOE` shows on the page as a dashed **need from
Joe** tag. That's deliberate — a missing fact stays visible instead of being
quietly replaced with a plausible-sounding invention.

| Field | What to ask him |
|---|---|
| `area` | The area he covers, e.g. `"Tacoma & South Sound"` |
| `hours` | When he takes calls, e.g. `"Mon–Sat, 8am–7pm"` |

The 253 area code points at Tacoma / South Sound, WA — **that's a guess, not
something Joe said.** Confirm before publishing.

`phone` must stay in `+1XXXXXXXXXX` form; it powers the call and text links.
`display` is only what's printed on screen.

## Photos

Six empty slots are waiting. See [photos/README.md](photos/README.md) for what to
ask Joe for and how to add them — it's written so you can forward it to him
more or less as-is.

---

## Deploying

`index.html` is fully self-contained, so any static host works. For Vercel from
GitHub: push this folder, import the repo, and accept the defaults — Vercel
serves `index.html` from the root with no configuration and no build command.
There's no framework to detect and nothing to install.

Before it goes public: the page carries Joe's real phone number, and a public
URL means that number can be scraped. Worth his explicit okay first.

---

## Files

```
index.html      the site — this is the deliverable
artifact.html   same page, body only, for the hosted preview link
photos/         Joe's photos go here (see its README)
build/
  page.html     source used to generate both pages
  make.py       wraps page.html into index.html + artifact.html
  fonts.py      re-downloads and re-embeds the fonts
  fonts.css     generated: the four faces as base64
  gf.css        generated: the Google Fonts stylesheet the URLs came from
```

You only need `build/` to change the fonts. For everything else, edit
`index.html` directly.

```bash
python build/make.py
```

**Careful:** `make.py` overwrites `index.html` from `build/page.html`. If you've
been editing `index.html` by hand, don't run it. Either edit `index.html` only,
or edit `build/page.html` and rebuild.

---

## How it's put together

**Palette** is Gulf livery — petrol blue, warm cream, burnt marigold. Light is
the default, because people read this standing outdoors next to a car that has
just broken. Dark mode is a deep petrol blue rather than black; black plus
orange is what made the first version read as Halloween.

**Fonts** are embedded as base64 rather than linked from Google Fonts, because
the hosted preview blocks external requests — a `<link>` would silently fall
back to system fonts and quietly destroy the type hierarchy. Zilla Slab for
headings, IBM Plex Sans for prose, IBM Plex Mono for numbers and labels.

**The diagram** is hand-drawn SVG. The six areas are real radio buttons: one tab
stop, arrow keys to move between them. Every badge is positioned to stay clear
of overlapping hit areas — the engine badge in particular has to sit outside the
front wheel's hit circle or the wheel swallows the tap.

**The service list** underneath is generated from the same data as the diagram,
so there's one source of truth and everything is readable without interacting
with the SVG at all.

### Motion

Two mechanisms, split by how bad it is when each one fails.

**Reveals** — the blueprint drawing itself, photos settling in, section rules
stroking across — run on IntersectionObserver and plain CSS transitions. These
decide whether content is *visible*, so they must never depend on a scroll
timeline resolving. The resting state in the CSS is fully visible; script adds a
`.pre` class to hide, the observer removes it, and a timeout clears it after
four seconds no matter what. No script, no observer, a stalled timeline, a
printer — the page still shows everything. An unseen animation is a far smaller
problem than an invisible page.

**Continuous effects** — the phone number drifting against the scroll, the
wheels turning as the car arrives — use CSS scroll-driven animation
(`animation-timeline`), which runs off the main thread and is genuinely better
at this. Neither can hide anything: if the timeline never resolves, the number
just sits still.

Everything is off under `prefers-reduced-motion: reduce`.

**There is no contact form and no send button.** Joe is standing in front of the
customer when he shows them this, so a message composer was solving a problem
that doesn't exist. The number is a tap-to-call and tap-to-text link instead.
Nothing is collected, stored, or transmitted — there's no backend, no analytics,
and no database.

## What's deliberately not on the page

No testimonials, star ratings, review counts, "trusted by N drivers,"
years-in-business, or certifications. None of it is known to be true, and
inventing it on a real tradesman's site is a liability for him, not an asset.
The moment Joe has one real quote from one real customer, there's a place for it.
