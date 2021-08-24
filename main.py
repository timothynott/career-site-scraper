from project.process.scraper_runner import ScraperRunner
from project.services.firestore import FirestoreService


def scrape():
    firestore = FirestoreService()
    configs = firestore.get_configs()

    scraper = ScraperRunner()
    scraper.run(configs)
    return 0


scrape()
