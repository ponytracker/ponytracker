#! /usr/bin/env python


'''
Issue Extension for Python-Markdown
==================================

Replace #1234 with link to issue 1234.

Usage
-----

    >>> import markdown
    >>> src = 'Please see issue #1234.'
    >>> html = markdown.markdown(src, ['tracker.mdx.mdx_issue'])
    >>> print(html)
    <p>Please see issue <a href="/project/issues/1234/">#1234</a>.</p>
    >>> html = markdown.markdown(src, ['tracker.mdx.mdx_issue'], {'tracker.mdx.mdx_issue': {'absolute_url': True}})
    >>> print(html)
    <p>Please see issue <a href="http://localhost:8000/project/issues/1234/">#1234</a>.</p>

Dependencies
------------

* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)
'''


import markdown
from markdown.inlinepatterns import SubstituteTagPattern
from markdown.inlinepatterns import Pattern
from markdown.util import etree

from django.urls import reverse
from django.conf import settings


ISSUE_RE = r'#([0-9]+)'


class IssuePattern(Pattern):

    def __init__(self, project_name, absolute_url=False):
        super(IssuePattern, self).__init__(ISSUE_RE)
        self.project_name = project_name
        self.absolute_url = absolute_url

    def handleMatch(self, m):
        el = etree.Element('a')
        issue_id = m.group(2)
        url = reverse('show-issue', args=[self.project_name, issue_id])
        if self.absolute_url:
            url = settings.BASE_URL + url
        el.set('href', url)
        el.text = '#{issue_id}'.format(issue_id=issue_id)
        return el


class IssueExtension(markdown.extensions.Extension):

    def __init__(self, **kwargs):
        self.config = {
            'project_name': ['project', 'Project name'],
            'absolute_url': [False, 'Use absolute URL'],
        }
        super(IssueExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        pattern = IssuePattern(self.getConfig('project_name'), self.getConfig('absolute_url'))
        md.inlinePatterns.add('issue', pattern, '<not_strong')


def makeExtension(**configs):
    return IssueExtension(configs=configs)
