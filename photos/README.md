# Photos

Put Joe's photos in this folder, then list the filenames in the `PHOTOS` block
near the bottom of `index.html`:

```js
const PHOTOS = [
  { file:"engine-bay.jpg", want:"An engine bay he's just worked in" },
  { file:null,             want:"Before and after on a dent or a scrape" },
  ...
];
```

`file:null` leaves the slot as a marked empty placeholder. Any filename you put
there gets loaded from this folder.

---

## What to ask Joe for

Six shots, roughly in order of how much they're worth:

1. **Joe himself, working.** People book a person, not a service. This is the
   single most valuable photo on the list.
2. **A car mid-job at someone's house** — tools out, driveway or kerb visible.
   This is the whole pitch in one image: he came to them.
3. **Before and after on a dent or scrape.** Two images, same angle, same
   distance. The comparison does the selling.
4. **A finished respray or a colour-matched panel.** Paint is the work people
   least expect a mobile mechanic to do.
5. **An engine bay he's just worked in.** Proves he goes deeper than oil changes.
6. **Brakes off, rotors visible.** Instantly readable as real mechanical work.

### Tell him

- Landscape, not portrait. The slots are 4:3 and landscape fills them properly.
- Daylight. No flash. Phone camera is completely fine.
- Wipe the lens first — it's usually the difference between a sharp photo and a
  soft one.
- Get closer than feels natural. The part he worked on should fill the frame.
- No customer number plates, faces, or house numbers in shot.

### Before adding them

- Resize to about 1600px on the long edge. Straight-from-phone photos are
  3–6 MB each and six of those makes the page slow on mobile data — which is
  exactly where it'll be opened.
- Save as `.jpg`. Name them plainly: `dent-before.jpg`, `dent-after.jpg`.
- The `alt` text comes from the `want` field, so keep it describing the actual
  photo once you swap a real one in.
