# unsuckjs.com

Progressively enhance HTML with lightweight JavaScript libraries. No build tools and no compiling necessary. Most libraries should be 10 KB or less (minified).

## 🤨 Why?

Sometimes you don't need an entire SPA framework just to load a progress spinner.

## 🙋 Shouldn't this just be an `awesome` repo?

Yeah, probably.

## 🛠️ Add a new library

1. Fork this repo
2. Update `data/libraries.json` following the current examples
3. Make a PR
4. ???
5. Profit!

## 🤓 Why use `coltrane` to build this site?

unsuckjs.com looks like a static site (and it mostly is), but I wanted to fetch repository metadata dynamically without having to re-run a static site generator on a schedule. So, I used my personal static site framework, [coltrane](https://coltrane.readthedocs.io) to write most of the content in Markdown, but still have the flexibility of using Django `templatetags` for server-side functionality. It's the best of both worlds.

Also, because it's my site and I wanted to. 🥹

## Hacker News Discussion

- https://news.ycombinator.com/item?id=36343544

## 🔬 Local development

1. Clone this repo
2. `cd` into newly created directory
3. `poetry install`
4. `poetry run coltrane play`
