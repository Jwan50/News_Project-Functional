import time

import schedule
from news_scraping.berlingske import scrape_berlingske

runEvery = 5
runType = 2

def run_berlingski():
    try:
        print('Berlingski is running every {} seconds ... '.format(runEvery))
        scrape_berlingske(runType)

    except Exception as e:
        print('Problem running Berlingski scheduler: ', e)


schedule.every(runEvery).seconds.do(run_berlingski)

while True:
    schedule.run_pending()
    time.sleep(1)
