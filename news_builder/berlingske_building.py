import bs4 as bs
import datetime
import requests
from news.concrete_news_builder import Concrete_news_builder
from news_queries import news_saving, app_init_news


class ber_concretenews_building(Concrete_news_builder):
    provider = 'berlingske'
    categories = {'politik', 'sport', 'internationalt', 'samfund'}
    data_name = 'berlingske'

    def __init__(self, runType):
        super().__init__()
        self.runType = runType

    def getNews_berlingske(self):
        global headline, category, content, date, news
        urlbase = 'https://www.berlingske.dk/nyheder/'
        scrap_date = datetime.datetime.now()
        for category in self.categories:
            urlbase_category = urlbase + category
            try:
                urltxt = requests.get(urlbase_category)
                urltxt = urltxt.content
                soup = bs.BeautifulSoup(urltxt, 'html.parser')
                headers = soup.findAll('div', {'class': 'teaser-container'})
                for header in reversed(headers):
                    header_date = header.find('span', {'class': 'text-uppercase font-s2'}).text.lower()
                    if 'i går' in header_date.lower() or '/' in header_date:
                        continue
                    hm = header_date.split(':')
                    h = int(hm[0])
                    m = int(hm[1])
                    date = scrap_date.replace(hour=h, minute=m, second=0, microsecond=0)
                    date = date.strftime('%Y-%m-%d')
                    date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    headline = header.find('h4', {'class': 'teaser__title d-inline-block font-s4'}).text.strip()
                    hrefs = header.find('h4', {'class': 'teaser__title d-inline-block font-s4'})('a')[0]['href']
                    link_to_more = 'https://www.berlingske.dk' + hrefs
                    link_urltxt = requests.get(link_to_more)
                    link_urltxt = link_urltxt.content
                    soup = bs.BeautifulSoup(link_urltxt, 'lxml')
                    unwanted = soup.find('aside', {'class': 'embedded-element embedded-factbox position-relative'})
                    if unwanted:
                        unwanted.extract()
                    if not (soup.find('div', {'class': 'article-body'})):
                        continue
                    contents = soup.findAll('div', {'class': 'article-body'})[0]('p')

                    content = ''
                    for text in contents:
                        text = text.text.strip()
                        if 'ritzau' in text:
                            break
                        content = content + ' ' + text
                        if 'Fold sammen' in content:
                            content = content.split('Fold sammen')
                            content = content[0]
                    news = super().setCategory(category).setHeadline(headline).setContent(content).setDate(
                        date).setProvider(provider=self.provider).build()

                    if self.runType > 1:
                        init_app = app_init_news.Init_news()

                        news_saving_ber = news_saving.news_saving(news.provider, news.headline, news.content, news.date,
                                                                  news.category, self.data_name)
                        try:
                            init_app.is_app_init_news()
                            news_saving_ber.news_save()
                        except Exception as e:
                            print(e)
                    print(" --News source: {}, --Category: {}, -- Headline: {},  --Date: {}".format(news.provider,
                                                                                                    news.category,
                                                                                                    news.headline,
                                                                                                    news.date))
            except Exception as e:
                print(e)
