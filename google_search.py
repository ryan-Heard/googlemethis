#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from GoogleScraper import scrape_with_config, GoogleSearchError

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
        search =  scrape_with_config(config)
    except GoogleSearchError as e:
        print("errors")

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
            base = "Wikipedia says: " + link.snippet+ '\n\n'

    base += "These may be useful links: \n"

    for link in links:
        base +=  link.link + '\n'

    return base;
