from .process.scraper_runner import ScraperRunner
from .services.firestore import Firestore


def scrape():
    firestore = Firestore()
    configs = firestore.get_configs()

    scraper = ScraperRunner()
    scraper.run(configs)
    return 0


scrape()
