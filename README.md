# Enacted U.S. AI laws: open data from AI Laws by State

A weekly copy of the data behind [AI Laws by State](https://www.ailawsbystate.com): enacted state, D.C. and federal laws with a substantive provision about artificial intelligence, one row per law, with dates, topics and a link to the official text.

The same files are published live at [ailawsbystate.com/press/embeds](https://www.ailawsbystate.com/press/embeds). This repository adds a dated history, so you can cite the list as it stood on a given day and see what changed between weeks.

## Files

| File | What it holds |
|---|---|
| [`data/ai-laws.csv`](data/ai-laws.csv) | One row per enacted law. |
| [`data/ai-laws-by-state.csv`](data/ai-laws-by-state.csv) | One row per state and D.C.: enacted AI laws, then laws per topic. |
| [`data/ai-laws.json`](data/ai-laws.json) | The laws plus headline totals, the as-of date and the license. |
| [`data/manifest.json`](data/manifest.json) | When this copy was taken, the counts, and a checksum for each file. |
| [`snapshots/`](snapshots/) | A dated copy of `ai-laws.csv` for each week the list changed. |

### `ai-laws.csv`

| Column | Meaning |
|---|---|
| `jurisdiction_code` | Two-letter state code, `DC`, or `US` for federal laws. |
| `jurisdiction` | State name, "District of Columbia" or "Federal". |
| `bill_number` | The bill number as the legislature writes it. |
| `title` | The bill's title. |
| `enacted_date` | The date the bill was signed or otherwise enacted. |
| `enacted_date_source` | `reviewed` when the date was checked in our state-by-state reviews; `last_action` when it is the date of the bill's last recorded action. |
| `effective_date` | The date the law takes effect, as stated in the law, where known. |
| `topics` | The topics the law covers, separated by semicolons. |
| `page_url` | The law's page on AI Laws by State: summary, provisions and sources. |
| `official_text_url` | The legislature's official page or text. |

### `ai-laws-by-state.csv`

`state_code`, `state`, `enacted_ai_laws`, then one column per topic with the number of that state's laws on it: `deepfakes`, `government_use`, `disclosure_transparency`, `intimate_images`, `autonomous_vehicles`, `child_sexual_abuse_material`, `automated_decisions`, `political_ads`, `education`, `chatbots_consumer_ai`, `health_care`, `privacy`, `facial_recognition`, `law_enforcement`, `employment`, `likeness`, `insurance`, `social_media_platforms`, `liability`, `comprehensive`, `frontier_models`, `algorithmic_pricing`, `robots`, `real_estate`, `robocalls`. A law on several topics counts once in `enacted_ai_laws` and once in each of its topic columns. Federal laws are not in this file.

## What counts as an AI law

A law is counted when its enacted text has a substantive provision about AI or a closely related technology: an obligation, prohibition, right, crime, disclosure rule or admissibility standard, or a government body created with duties. Laws that only define AI, fund it, or order a study are not counted. Each bill counts once. The full definition is in the [methodology](https://www.ailawsbystate.com/methodology#what-counts).

Our state-by-state reviews cover laws enacted since 2019. Earlier laws appear when they meet the definition, but the list before 2019 is not complete.

## How it is updated

Every Monday a [GitHub Action](.github/workflows/snapshot.yml) downloads the three published files, checks that they agree with each other, and commits them only if a law was added, removed or corrected. The commit message gives the as-of date and the number of laws, so the history of this repository is the history of the list.

## Citing

Please credit **AI Laws by State (ailawsbystate.com)** and give the as-of date, for example:

> AI Laws by State. *Enacted U.S. AI laws* (data as of 2026-10-19). https://github.com/ailawsbystate/ai-laws-data

GitHub's "Cite this repository" button uses [`CITATION.cff`](CITATION.cff).

## License

The data is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You can share and adapt it for any purpose, including commercially, as long as you credit AI Laws by State.

## Corrections

Found an error? Tell us through the [corrections page](https://www.ailawsbystate.com/corrections). Fixes made on the site reach this repository with the next weekly snapshot.

This is not legal advice. Check the official text before relying on any law.
