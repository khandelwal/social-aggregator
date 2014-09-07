import time
import random

import pytumblr
import yaml
from bs4 import BeautifulSoup

def operating_countries():
    """ Read in the list of countries PeaceCorps is active in. Express those
    names as tags and return that list. """

    with open('countries.txt', 'r') as countries_file:
        countries = countries_file.readlines()
        countries = [c.replace('\n', '').lower() for c in countries]

        space_removed = [c.replace(' ', '') for c in countries if ' '  in c]
        return countries + space_removed

def before_threshold(days=5):
    """ Return a UNIX timestamp n days before right now. """
    return int(time.time() - (days * 86400))

def read_api_oauth():
    with open('secrets.yaml') as secrets:
        tokens = yaml.safe_load(secrets)
        return tokens

def get_tagged_posts(tag, multiples=3):
    tokens = read_api_oauth()

    client = pytumblr.TumblrRestClient(
        tokens['tumblr_consumer_key'],
        tokens['tumblr_secret_key'], 
        tokens['tumblr_token'], 
        tokens['tumblr_token_secret'])

    last_timestamp = before_threshold()
    results = []

    for _ in range(0, multiples):
        results.extend(client.tagged(tag, before=last_timestamp))
        last_timestamp = results[-1]['timestamp']

    return results

def pick_paragraph(post_body):
    """ We're going to randomly pick one paragraph to display out of many.  """
    pbs = BeautifulSoup(post_body)
    paragraphs = pbs.find_all('p')
    paragraphs = [p for p in paragraphs if len(p.find_all('img')) == 0]
    paragraph = paragraphs[random.randrange(0, len(paragraphs))]
    return paragraph

def pick_photo(photos):
    photo = photos[random.randrange(0, len(photos))]
    return photo

def select_posts(posts):
    """ Given a list of peacecorps tagged posts, select some content for
    publication. This uses a heuristic to select which posts are worth
    considering. """
    country_tags = operating_countries()
    selected = []
    for p in posts:
        tagged_country = [c.lower() for c in p['tags'] if c.lower() in country_tags]
        if len(tagged_country) > 0 and p['note_count'] > 0:
            if 'body' in p:
                paragraph = pick_paragraph(p['body'])
                p['selected_paragraph'] = paragraph.contents[0]
            elif 'photos' in p:
                photo = pick_photo(p['photos'])
                p['selected_photo'] = photo

            p['country'] = tagged_country[0]
            selected.append(p)
    return selected
            
if __name__ == '__main__':
    posts  = get_tagged_posts('peacecorps')
    select_posts(posts)
