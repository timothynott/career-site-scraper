from project.process.scraper_runner import ScraperRunner
from project.services.firestore import FirestoreService


def scrape():
    # WK: restore (and remove temp config)
    # firestore = FirestoreService()
    # configs = firestore.get_configs()

    configs = [
        {
            'company_name': 'Cornell Pump',
            'url': 'https://recruiting.ultipro.com/ROP1001ROPER/JobBoard/5635cac7-6c69-44a7-850c-cf35112ce343',
            'spider_class': 'ultipro'
        }
    ]

    scraper = ScraperRunner()
    scraper.run(configs)
    return 0


scrape()
