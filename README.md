# Flow Remote Ops -- Landing Page

A single-page marketing site for Flow Remote Ops, a remote staffing and
business support partner. Built with HTML5, CSS3, vanilla JavaScript, and a
minimal Flask app to serve it.

## What this is

- **A landing page, not a web app.** There is no login, no user accounts,
  and no database.
- **The lead form is external.** The "Let's Talk" button in the Contact
  section opens a Google Form in a new tab instead of submitting to a
  backend. Flask's only job here is to serve `index.html` and the static
  assets.

## Before you launch

Open `static/js/script.js` and replace the placeholder with your real
Google Form link:

```js
var GOOGLE_FORM_URL = 'https://forms.gle/REPLACE-WITH-YOUR-FORM-LINK';
```

That's the only thing you need to change to go live.

## Project structure

```
flow-remote-ops/
|
├── app.py                 # Flask app -- serves the page, nothing else
├── requirements.txt
├── README.md
|
├── templates/
│   └── index.html         # The full landing page
|
└── static/
    ├── css/
    │   └── style.css      # Design system + layout (brand colors/type)
    ├── js/
    │   └── script.js      # Mobile menu, FAQ accordion, Google Form link
    └── images/            # Empty -- drop in a favicon/OG image if desired
```

## Running it locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000

## Brand tokens used

| Name        | Hex       | Used for                          |
|-------------|-----------|------------------------------------|
| Midnight    | `#0A0F1E` | Hero, contact, dark section fills  |
| Navy        | `#0F172A` | Footer, secondary dark             |
| Primary Blue| `#2563EB` | Primary buttons, links, accents    |
| Accent Blue | `#38BDF8` | Eyebrow labels, gradient accents   |
| Light Gray  | `#E5E7EB` | Light section backgrounds          |
| White       | `#FFFFFF` | Base background, text on dark      |

Typefaces: **Space Grotesk** for headlines/display, **Inter** for body text
(loaded from Google Fonts).

## Content notes

No testimonials, client logos, statistics, or case studies were invented,
per the brand brief -- those sections are intentionally left out until real
proof is available. When you have real proof, a "Trusted by" or results
section can be added between "Why Flow" and "Who We Help."

## Deploying

This is a standard Flask app, so it can be deployed anywhere that runs
Python (Render, Railway, Fly.io, a VPS behind gunicorn/nginx, etc.). Since
there's no database or secrets involved, no special configuration is
needed beyond installing `requirements.txt` and running the app behind a
production WSGI server (e.g. `gunicorn app:app`).
