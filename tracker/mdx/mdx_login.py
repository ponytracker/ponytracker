#! /usr/bin/env python


'''
Login Extension for Python-Markdown
===================================

Add tooltip on @uid.

Usage
-----

    >>> import markdown
    >>> src = 'Thanks @uid!'
    >>> html = markdown.markdown(src, ['tracker.mdx.mdx_login'])
    >>> print(html)
    <p>Thanks <span>@<b>uid</b></span>!</p>

Dependencies
------------

* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)
'''


import markdown
from markdown.inlinepatterns import SubstituteTagPattern
from markdown.inlinepatterns import Pattern
from markdown.util import etree

from django.conf import settings

from accounts.models import User


LOGIN_RE = r'@([a-z]+)'


class LoginPattern(Pattern):

    def __init__(self, project_name, absolute_url=False):
        super(LoginPattern, self).__init__(LOGIN_RE)
        self.project_name = project_name
        self.absolute_url = absolute_url

    def handleMatch(self, m):
        uid = m.group(2)
        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            span = etree.Element('span')
            b = etree.SubElement(span, 'b')
            b.text = uid
            span.text = '@'
            return span
        url = user.url(self.project_name)
        a = etree.Element('a')
        a.set('href', url)
        span = etree.SubElement(a, 'span')
        span.text = '@'
        b = etree.SubElement(span, 'b')
        b.set('data-toggle', 'tooltip')
        b.set('data-placement', 'bottom')
        b.set('title', user.fullname)
        b.text = uid
        return a


class LoginExtension(markdown.extensions.Extension):

    def __init__(self, **kwargs):
        self.config = {
            'project_name': ['project', 'Project name'],
            'absolute_url': [False, 'Use absolute URL'],
        }
        super(LoginExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        pattern = LoginPattern(self.getConfig('project_name'), self.getConfig('absolute_url'))
        md.inlinePatterns.add('login', pattern, '_end')


def makeExtension(**configs):
    return LoginExtension(configs=configs)
