# Joe — Mobile Auto Repair

A one-page site for Joe, who does auto repair at the customer's place and has no
shop. It's built to be **shown**: Joe pulls it up on his phone when he's pitching
someone, and it answers "what do you actually do?" without him having to list it.

`index.html` is the whole site, plus two images in `media/`. No build step, no
dependencies, no server, no third-party requests. Double-click it to open it.

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
media/          the car render the tour uses (car.webp, car-2k.webp)
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

**The landing screen is a tour of the car.** A studio photograph of a sedan
stays pinned while the copy scrolls past it, and a camera glides across the
photo: the whole car, then the engine bay, front end, a wheel, the bodywork,
the underside, the cabin, and back out to the whole car with the number.

**The car is a generated render, not a real customer's car.** Joe has no
photos yet, so `media/car.webp` (3840px, transparent background) and
`media/car-2k.webp` (phones) are an AI studio render of a generic, unbranded
sedan — no badges, no plate. It is used purely as the thing the tour points at;
it is never presented as his work. When he sends real photos they go in the
gallery, not here.

How the tour works, in three pieces:

1. **Pinned stage.** `.stage` is `position: sticky`; the `.steps` column scrolls
   over it (desktop, left 42%) or under it (phone, where the stage is the top
   44% of the screen).
2. **A continuous camera.** Each area has a focus box on the photo, in photo
   pixels. On every frame the script works out how far the reader is through
   the steps as a fractional index, blends the two nearest boxes into one
   target (dwell, glide, dwell), eases the live camera toward it, and writes a
   single `translate() scale()` transform on the wrapper that holds both the
   photo and the SVG overlay. So the move is tied to the scroll, not to a
   timer, and scrolling backwards plays it in reverse.
3. **HUD, not drawings.** Each area's overlay is corner brackets, a dashed
   frame, a couple of accent shapes aligned to the photo, pulsing hotspots, a
   scan line and a label. Strokes use `vector-effect: non-scaling-stroke` and
   label text is sized by `1 / (zoom × px-per-photo-pixel)`, so lines stay
   hairline and type stays the same size on screen at any zoom.

**One source of truth.** `ZONES` at the bottom of the file holds the areas, the
copy, the focus boxes and the job lists. The tour steps, the callouts on the
drawing, the right-hand rail and the written-out index are all generated from
it.

### Motion

**Reveals** — the headline rising word by word, step copy and chips lifting
in, section rules sweeping across — have a *visible* resting state. Script adds
a hidden class, an observer removes it, and a timeout clears everything after a
few seconds regardless. No script, no observer, a printer: the page still shows
everything, with the whole car sitting in the stage.

**Continuous effects** — the camera, the grid drifting behind the car, the
ticker of jobs sliding with the scroll — can't hide anything if they fail.

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
