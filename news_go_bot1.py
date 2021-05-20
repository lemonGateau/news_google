#coding utf-8
import sys
sys.path.append('..')
import requests
from bs4 import BeautifulSoup
import config
from line_bot3 import LineNotifyBot


class NewsGo:
    def __init__(self):
        self.end_point = 'https://news.google.com/news/rss/'
        self.lang_params = 'hi=ja&gl=JP&ceid=JP:ja' # 日本語newsの場合

    def _get_requests(self, path):
        url = self.end_point + path + '?' + self.lang_params

        return requests.get(url)

    def search_topic(self, topic_name='TECHNOLOGY'):
        '''
        topic_name: WORLD, NATION, BUSINESS, TECHNOLOGY,
                    ENTERTAINMENT, SPORTS, SCIENCE, HEALTH
        '''
        path = f'headlines/section/topic/{topic_name}'

        return self._get_requests(path)

    def fetch_titles_from_res(self, res, title_num=5):
        soup = BeautifulSoup(res.text, 'html.parser')

        titles = soup.find_all('title', limit=title_num)
        titles = [t.text for t in titles]   # text化(htmlタグを削除)

        return titles

    def fetch_golink_from_res(self, res):
        ''' todo: link取得 top pageを返すか等検討'''
        soup = BeautifulSoup(res.text, 'html.parser')

        link = soup.find('link')
        link = link.text

        return link



if __name__ == '__main__':
    news_go = NewsGo()
    ln = LineNotifyBot(access_token=config.ACCESS_TOKEN)

    res    = news_go.search_topic(topic_name='TECHNOLOGY')
    link   = news_go.fetch_golink_from_res(res)
    titles = news_go.fetch_titles_from_res(res, title_num=5)

    msg = '\n' + '\n\n'.join(titles) + link

    ln.send(message=msg)
