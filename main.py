from project.process.scraper_runner import ScraperRunner
from project.services.firestore import Firestore


def scrape():
    firestore = Firestore()
    configs = firestore.get_configs()

    # WK: temp
    url = 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=5af0373a-89ae-488e-b298-4066fdc2232a'
    configs = list(filter(lambda c: c['url'] == url, configs))
    print('\n\n')
    print(configs)
    print('\n\n')

    scraper = ScraperRunner()
    scraper.run(configs)
    return 0


scrape()
