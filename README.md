# Course Materials Website (Quarto)

Navigation for students:  **Home → Academic year → Course → Lecture / Assignment**

## Folder layout

```
_quarto.yml                      site settings, navbar, footer
index.qmd                        home: auto-lists every academic year (newest first)
styles.css
tools/render_manim.py            renders a lecture's Manim scenes into its assets/ folder
2026-2027/                       one folder per academic year
  index.qmd                      auto-lists all courses of that year (all majors)
  ece/                           one folder per major
    antenna-design/              one folder per course
      index.qmd                  course page: auto-lists lectures + assignments
      lectures/
        lecture-01/
          index.qmd              MAIN file: front matter + {{< include >}} lines
          _01-pattern.qmd        parts (leading "_" = included, never a page of its own)
          _02-friis.qmd
          assets/                PNG, mp4, ... (published)
          _src/                  Manim scenes, plotting scripts (NOT published)
      assignments/
        assignment-01/index.qmd
docs/                            rendered site (publish this folder)
```

**Rule of thumb:** every lecture/assignment is a *folder* containing `index.qmd`.
Anything starting with `_` is never published, so source code and drafts stay private.

## Splitting a big lecture into parts

In `lecture-02/index.qmd`:

```
{{< include _01-intro.qmd >}}
{{< include _02-derivation.qmd >}}
```

* Part files have **no** YAML header, only content (start them with `##` headings).
* Reference images/videos from a part as `assets/figure.png` (paths are relative to the lecture folder).

## Images, videos, Manim

```
![Caption](assets/figure.png){fig-alt="Description for screen readers" width="80%"}

{{< video assets/MyScene.mp4 >}}
```

1. Put your Manim scene in `<lecture>/_src/scene_something.py` (file name must start with `scene_`).
2. Run: `python tools/render_manim.py 2026-2027/ece/<course>/lectures/lecture-01 m`
   (`l` = 480p draft, `m` = 720p, `h` = 1080p). Finished `.mp4` files are copied into `assets/`.
3. The scene's class name becomes the file name (`class BandFormation` → `BandFormation.mp4`).

Tip: render drafts with `l` while working, and `m` for the final version, to keep the repo small.

**Video size:** Cloudflare Pages limits single files (about 25 MiB at the time of writing) and GitHub
limits files over 100 MB, so keep videos short, or upload long ones to YouTube (unlisted) and embed them.
Check the current limits of the host you choose.

## Everyday commands

```bash
quarto preview      # live preview while you edit
quarto render       # builds the site into /docs
```

## Start a new academic year (e.g. 2027-2028)

1. Copy the folder `2026-2027` to `2027-2028`.
2. Delete the courses/majors you will not teach; add new ones (see below).
3. Open `2027-2028/index.qmd` and change the title and description to 2027–2028.
4. Update lecture content as needed. Run `quarto render`.

The home page lists the new year automatically. Old years stay online as an archive.

## Add a course (or a new major)

* New course, same major: copy a course folder, e.g. `2026-2027/ece/antenna-design` → `2026-2027/ece/<new-course>`.
* New major: create `2026-2027/<major>/<course>/` (copy an existing course as the starting point).
* In the course's `index.qmd` set:

```yaml
title: "Course name"
description: "One-line summary"
categories: [Major name, First-Year]     # shown as tags and filters on the year page
kind: course                             # REQUIRED: this is how the year page finds it
```

## Publishing

* **GitHub Pages:** push to a public repo; Settings → Pages → deploy from `main`, folder `/docs`.
  Re-run `quarto render` and push after each change.
* **Netlify / Cloudflare Pages:** connect the repo; build command `quarto render`
  (or commit `/docs` and skip the build); output directory `docs`.

Note: free hosting is public. Equations load MathJax from a CDN, so students need internet access.
