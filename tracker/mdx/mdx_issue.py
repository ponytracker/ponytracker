#! /usr/bin/env python


'''
Issue Extension for Python-Markdown
==================================

Replace #1234 with link to issue 1234.

Usage
-----

    >>> import markdown
    >>> src = 'Please see issue #1234.'
    >>> html = markdown.markdown(src, ['issue'])
    >>> print(html)
    <p>Please see issue <a href="/project/issue/1234/">#1234</a>.</p>

Dependencies
------------

* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)
'''


import markdown
from markdown.inlinepatterns import SubstituteTagPattern
from markdown.inlinepatterns import Pattern
from markdown.util import etree


ISSUE_RE = r'#([0-9]+)'


class IssuePattern(Pattern):

    def __init__(self, base_url='{issue_id}'):
        super().__init__(ISSUE_RE)
        self.base_url = base_url

    def handleMatch(self, m):
        el = etree.Element('a')
        issue_id = m.group(2)
        el.set('href', self.base_url.format(issue_id=issue_id))
        el.text = '#{issue_id}'.format(issue_id=issue_id)
        return el


class IssueExtension(markdown.extensions.Extension):

    def __init__(self, **kwargs):
        self.config = {'base_url': ['/project/issue/{issue_id}/', 'URL format']}
        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('issue', IssuePattern(self.getConfig('base_url')), '<not_strong')


def makeExtension(configs={}):
    return IssueExtension(configs=dict(configs))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
