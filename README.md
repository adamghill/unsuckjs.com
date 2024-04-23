# unsuckjs.com

Progressively enhance HTML with lightweight JavaScript libraries. No build tools and no compiling necessary. Most libraries should be 10 KB or less (minified).

## 🤨 Why?

Sometimes you don't need an entire SPA framework just to load a progress spinner.

## 🙋 Shouldn't this just be an `awesome` repo?

Yeah, probably.

## 🛠️ Add a new library

1. Fork this repo
1. Update `data/libraries.json` following the current examples
1. Make a PR
1. ???
1. Profit!

## 🤓 Why use `coltrane` to build this site?

unsuckjs.com looks like a static site (and it mostly is), but I wanted to fetch repository metadata dynamically without having to re-run a static site generator on a schedule. So, I used my personal static site framework, [coltrane](https://coltrane.readthedocs.io) to write most of the content in Markdown, but still have the flexibility of using Django `templatetags` for server-side functionality. It's the best of both worlds.

Also, because it's my site and I wanted to. 🥹

## Hacker News Discussion

- https://news.ycombinator.com/item?id=36343544

## 🔬 Local development

1. `git clone` this repo
1. `cd` into the newly created directory
1. `poetry install`
1. Create a personal access token at https://github.com/settings/tokens
1. `cp .env.example .env`
1. Update `.env` with your GitHub username and personal access token that was just created
1. `poetry run coltrane play`

## Minify CSS

1. `npm install -g uncss`
1. Make sure that the regular CSS files are enabled in the template
1. Make sure the site is running in another terminal
1. `uncss http://localhost:8000 --output static/css/unsuckjs.min.css`
