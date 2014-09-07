from django.template import loader, Context
import django
import tumblr
from django.conf import settings

def render(data):
    """ Use Django templates to render the output HTML. """
    settings.configure(
        DEBUG=True, TEMPLATE_DEBUG=True,
        TEMPLATE_DIRS=('/vagrant/code/social-aggregator/templates',))
    django.setup()
    t = loader.get_template('output.html')
    c = Context({'data':data})
    l = t.render(c)
    print l.strip('\n')   

def process_for_output(posts):
    processed_posts = []
    for p in posts:
        if 'selected_paragraph' in p:
            processed_posts.append({
                'country': p['country']
                'paragraph': p['selected_paragraph']
                })
    return processed_posts

if __name__ == '__main__':
    tumblr_posts = tumblr.get_tagged_posts('peacecorps')
    tumblr_posts = tumblr.select_posts(tumblr_posts)
    posts = process_for_output(tumblr_posts)
    render(posts)
