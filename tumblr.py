import time

import pytumblr
import yaml

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

def select_posts(posts):
    """ Given a list of peacecorps tagged posts, select some content for
    publication. This uses a heuristic to select which posts are worth
    considering. """
    country_tags = operating_countries()
    for p in posts:
        tagged_country = [c.lower() for c in p['tags'] if c.lower() in country_tags]
        if len(tagged_country) > 0 and p['note_count'] > 0:
            print p
            
if __name__ == '__main__':
    posts  = get_tagged_posts('peacecorps')
    select_posts(posts)
