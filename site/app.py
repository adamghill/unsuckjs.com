#!/usr/bin/env python

from coltrane import initialize, run

COMPRESS_FILTERS = {
    "css": [
        "refreshcss.filters.RefreshCSSFilter",
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.rJSMinFilter"],
}

wsgi = initialize(COMPRESS_FILTERS=COMPRESS_FILTERS, COMPRESS_ENABLED=True)

if __name__ == "__main__":
    run()
