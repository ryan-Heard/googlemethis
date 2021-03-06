#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from GoogleScraper import scrape_with_config, GoogleSearchError
import logging

formatter = "%(asctime) - %(name) - %(levelname) - %(message)"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('error.log')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def basic_usage(q):
    config = {
        'use_own_ip': True,
        'keyword': q,
        'search_engines': ['google'],
        'num_pages_for_keyword': 1,
        'scrape_method': 'selenium',
        'sel_browser': 'chrome',
        'do_caching': False
    }

    try:
        search = scrape_with_config(config)
        logger.info("Search using {}".format(config))
    except GoogleSearchError as e:
        logger.debug("Failed to get search Error: {}".format(e))

    return prioritize_response(search.serps[0].links)

    # for serp in search.serps:
    #    print(serp)
    #    print(serp.search_engine_name)
    #    print(serp.scrape_method)
    #    print(serp.page_number)
    #    print(serp.requested_at)
    #    print(serp.num_results)
    #    # ... more attributes ...
    #    for link in serp.links:
    #        print(link.snippet.encode("utf-8"))
    #        print(link.title.encode("utf-8"))


def prioritize_response(links):
    base = ""

    for link in links:
        if "wikipedia" in link.link:
            base = "Wikipedia says: " + link.snippet + '\n\n'

    base += "\nThese may be useful links: " + '\n'

    for link in links:
        base += link.link + '\n'

    base += '\n\n if you see an error or an improvement please contact my'
    base += ' Robo Father /u/DeadStarman'

    return base
