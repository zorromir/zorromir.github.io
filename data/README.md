# Research paper library

The **Exploring & Reading** section of [the portfolio](../../index.html) reads this directory's `reading-list.json` at page load. **To add or revise a paper, edit only the JSON file** — the site generates the cover, paper description, project links, category buttons and carousel controls automatically.

## Adding a paper

Copy an object inside `papers`, give it a unique `id`, and fill the required fields:

| Field | Meaning |
|---|---|
| `id` | Stable unique identifier, e.g. `cochrane-2005-asset-pricing` |
| `short_label` | Short text printed on the custom cover (e.g. `SDF`) |
| `title`, `authors`, `year`, `journal` | Publication metadata |
| `url` | Original publication or DOI URL, beginning with `https://` |
| `topic` | Concise technical field |
| `category_ids` | One or more existing `categories[].id` values; determines filters |
| `idea` | What the work argues or establishes, in plain English |
| `relevance` | How it helps a specific econometric method or project |
| `project_ids` | Existing `projects[].id` values; optional, otherwise `[]` |
| `reading_status` | `null` (unconfirmed), `"to-read"`, `"reading"` or `"read"` |
| `cover_accent` | Optional muted `#RRGGBB` colour |

For a newly established project, add one object to the top-level `projects` list with `id`, `name` and a same-site `#hash` or a verified `https://` URL. Use that ID in papers' `project_ids`. Add a new `categories` entry only when the existing category choices do not fit; category buttons are generated automatically from available papers.

## Reading progress and accuracy

All six initial papers are **example references**, not confirmed reading history. Their `reading_status` values are intentionally `null`. Only switch to `"reading"` or `"read"` after confirmation.

- `library_state: "sample_references"` keeps the provisional reading note visible. Change to `"curated"` once your actual list replaces the examples.
- Do not use a paper's bibliographic metadata to imply authorship, replication, completion, or publication by the portfolio owner.
- Covers are deliberately typographic illustrations. Do not upload third-party PDF pages or copyrighted journal covers as substitutes without permission.

## Checking and previewing

1. Validate the JSON with `python -m json.tool data/reading-list.json` from the repository root.
2. Run a local HTTP server at the repository root, such as `python -m http.server 8000`.
3. Open `http://localhost:8000/#engineering` and test filter buttons, previous/next arrows, keyboard arrows and mobile touch.
4. Click paper sources and project links, and check that the site doesn't show an unsupported reading status.

A local HTTP server is necessary because most browsers restrict `fetch()` from `file://` URLs.
