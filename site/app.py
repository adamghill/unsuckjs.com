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

SITES = {
    "unsuckjs": [
        "0.0.0.0:80",  # default for healthcheck
        "0.0.0.0:8024",
        "localhost:8024",
        "unsuckjs.localhost",
        "unsuckjs.com",
        "unsuckjs.adamghill.com",
    ],
    "unsuckcss": [
        "0.0.0.0:8025",
        "localhost:8025",
        "unsuckcss.localhost",
        "unsuckcss.com",
        "unsuckcss.adamghill.com",
    ],
}

wsgi = initialize(COMPRESS_FILTERS=COMPRESS_FILTERS, COMPRESS_ENABLED=True, COLTRANE_SITES=SITES)

if __name__ == "__main__":
    run()
