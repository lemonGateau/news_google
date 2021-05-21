#coding utf-8
import sys
from bs4.builder import TreeBuilder
sys.path.append('..')
import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import config
from line_bot3 import LineNotifyBot


class NewsGo:
    def __init__(self):
        self.end_point = 'https://news.google.com/news/rss'
        self.lang_params = '&hi=ja&gl=JP&ceid=JP:ja' # 日本語news対象

    def _get_requests(self, path, contains_query=False):
        ''' contains_query: pathに既にクエリが含まれているか '''
        if contains_query:
            url = self.end_point + path + self.lang_params
        else:
            url = self.end_point + path + '?' + self.lang_params

        return requests.get(url)

    def search_by_topic(self, topic_name='TECHNOLOGY'):
        '''
        topic_name: WORLD, NATION, BUSINESS, TECHNOLOGY,
                    ENTERTAINMENT, SPORTS, SCIENCE, HEALTH
        '''
        path = f'/headlines/section/topic/{topic_name}'

        return self._get_requests(path, contains_query=False)

    def search_by_geolocation(self, location='Japan'):
        ''' geo: country等、詳細非公開 '''
        path = f'/headlines/section/geo/{location}'

        return self._get_requests(path, contains_query=False)

    def search_by_query(self, query):
        '''　query: some words　'''
        path = f'/search?q={query}'

        return self._get_requests(path, contains_query=True)

    def search_by_media(self, media_url):
        ''' media_url: 'https://www.nhk.or.jp', 'itmedia.co.jp', etc.'''
        path = f'/search?q=inurl:{media_url}'

        return self._get_requests(path, contains_query=True)

    def search_by_period(self, after, before=date.today()):
        '''
        GMT表記 日本と9時間時差(ToDo: 地域時差を考慮?)
        after, before: 年-月-日(年/月/日)のどちらかで指定
            例: after  = '2002-02-03'
                before = '2021/5/21'
        '''
        path = f'/search?q=after:{after}, before:{before}'

        return self._get_requests(path, contains_query=True)

    def res_to_some_titles(self, res, title_num=5):
        soup = BeautifulSoup(res.text, 'html.parser')

        titles = soup.find_all('title', limit=title_num)
        titles = [t.text for t in titles]   # text化(htmlタグを削除)

        return titles

    def res_to_golink(self, res):
        ''' ToDo: soup.find('link')が動かないためsplitで代用 '''
        link = res.text.split('<link>')[1].split('</link>')[0]  # <link></link>で囲まれたurlを取得
        link = link.split('?')[0]   # クエリ文字列(?以降)を削除

        return link


if __name__ == '__main__':
    news_go = NewsGo()
    ln = LineNotifyBot(access_token=config.ACCESS_TOKEN)

    #res    = news_go.search_by_topic(topic_name='TECHNOLOGY')
    #res    = news_go.search_by_geolocation(location='us')
    #res    = news_go.search_by_query(query='コロナ')
    #res    = news_go.search_by_media(media_url='itmedia.co.jp')
    #res    = news_go.search_by_period(after='2021-05-20')

    titles = news_go.res_to_some_titles(res, title_num=5)
    link   = news_go.res_to_golink(res)

    msg = '\n' + '\n\n'.join(titles) + '\n' + link

    ln.send(message=msg)
