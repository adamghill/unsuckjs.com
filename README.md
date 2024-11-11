# unsuckjs.com / unsuckcss.com

Progressively enhance HTML with lightweight JavaScript/CSS libraries. No build tools and no compiling necessary. Most libraries should be 10 KB or less (minified).

## 🤨 Why?

Sometimes you don't need an entire SPA framework just to load a progress spinner.

## 🙋 Shouldn't this just be an `awesome` repo?

Yeah, probably.

## 🛠️ Add a new library

1. Fork this repo
1. Update `data/js.json` or `data/css.json` following the current examples
1. Make a PR
1. ???
1. Profit!

## 🤓 Why use [coltrane](https://coltrane.adamghill.com) to build this site?

[unsuckjs.com](https://unsuckjs.com) and [unsuckcss.com](https://unsuckcss.com) look like static sites (and they mostly are), but I wanted to fetch repository metadata dynamically without having to re-run a static site generator on a schedule. So, I used [coltrane](https://coltrane.readthedocs.io) which gives the flexibility of using Django `templatetags` for server-side functionality. It's the best of both worlds.

Also... because it's my site and I wanted to. 🥹

## 🔬 Local development

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
1. `git clone` this repo
1. `cd` into the newly created directory
1. Create a personal access token at https://github.com/settings/tokens
1. `cp .env.example .env`
1. Update `.env` with your GitHub username and personal access token that was just created
1. `uv run coltrane play`; note: this will take a while on the first load because it loads a lot of data from the GitHub API
