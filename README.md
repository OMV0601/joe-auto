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
  area    : null,   // e.g. "Tacoma & South Sound"
  hours   : null,   // e.g. "Mon–Sat, 8am–7pm"
};
```

`area` and `hours` are optional. Left as `null`, the page simply doesn't
mention them — no placeholder, nothing invented. Fill them in once Joe confirms
and they appear in the hero line and the footer.

The 253 area code points at Tacoma / South Sound, WA — **that's a guess, not
something Joe said.** Confirm before publishing an area.

`phone` must stay in `+1XXXXXXXXXX` form; it powers the call and text links.
`display` is only what's printed on screen.

## Photos

There is no gallery on the page until there is something real to put in it.
See [photos/README.md](photos/README.md) — once Joe sends a picture, drop it
in that folder, list it in `PHOTOS`, and the section appears.

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

**The landing screen is a tour of the car.** One technical drawing stays
pinned while the copy scrolls past it; each step tells the drawing which part
to look at. Opening: the whole car. Then the engine bay, front end, a wheel,
the bodywork, the underside, the cabin — and back out to the whole car with the
number. Six areas, no photographs needed.

How it works, in three pieces:

1. **Pinned stage.** `.stage` is `position: sticky`; the `.steps` column scrolls
   over it (desktop, left 44%) or under it (phone, where the stage is the top
   42% of the screen). An `IntersectionObserver` with a thin band in the
   middle of the viewport decides which step is "in front of" the reader.
2. **Zoom is one CSS transform.** `applyFocus()` takes the active area's focus
   box in drawing units, works out the scale that fits it in the car area, and
   sets `translate() scale()` on the `<svg>` so the box's centre lands in the
   middle of the stage. A 1.15s transition does the camera move. Every stroke
   uses `vector-effect: non-scaling-stroke`, so lines stay hairline at 4× zoom,
   and label text is sized by `1 / (zoom × px-per-unit)` so it stays the same
   size on screen whatever the zoom.
3. **X-ray.** Each area's internals (engine block, brake disc and caliper,
   exhaust run, seats and harness…) live in their own `<g class="part">`,
   hidden until their step is active. When any part is lit the shell drops to
   40% so the internals read.

**One source of truth.** `ZONES` at the bottom of the file holds the areas, the
copy, the focus boxes and the job lists. The tour steps, the callouts on the
drawing, the right-hand rail and the written-out index are all generated from
it.

### Motion

**Reveals** — the drawing stroking itself in on load, step copy rising in,
section rules sweeping across — have a *visible* resting state. Script adds a
hidden class, an observer removes it, and a timeout clears everything after a
few seconds regardless. No script, no observer, a printer: the page still
shows everything. (Because of `non-scaling-stroke`, dash lengths are in screen
pixels, so the draw-on measures each path and multiplies by the render scale
rather than using the usual `pathLength="1"` trick.)

**Continuous effects** — the car rolling in from the right on load, and the
wheels turning with the scroll via `animation-timeline: scroll()` — can't hide
anything if they fail to run.

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
