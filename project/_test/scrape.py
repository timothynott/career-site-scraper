# WK: update this to run without import error
# https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure
# https://docs.python.org/3/library/unittest.html

from ..process.scraper_runner import ScraperRunner

test_configs = [
    {
        'url': 'https://jobs-cantelmedical.icims.com/jobs/search?ss=1',
        'company_name': 'Cantel Medical',
        'spider_class': 'icims',
    },
    {
        'url': 'https://external-weatherford.icims.com/jobs/search?ss=1',
        'company_name': 'Weatherford',
        'spider_class': 'icims'
    },
    {
        'url': 'https://globalcareers-entegrisinc.icims.com/jobs/search?ss=1',
        'company_name': 'Entegris, Inc.',
        'spider_class': 'icims'
    },
    {
        'url': 'https://globalhub-berryglobal.icims.com/jobs/search?ss=1',
        'company_name': 'Berry Global Inc.',
        'spider_class': 'icims'
    },
    {
        'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=08cf914d-e2d5-4aba-b95c-c33cf076da39',
        'company_name': 'Rice Lake Weighing Systems',
        'spider_class': 'adp_wfn'
    },
    {
        'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=5af0373a-89ae-488e-b298-4066fdc2232a',
        'company_name': 'SP Industries',
        'spider_class': 'adp_wfn'
    },
    {
        'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=66d93efd-a316-4416-9647-78a8a2fa5359',
        'company_name': 'Tecomet Talented',
        'spider_class': 'adp_wfn'
    },
    {
        'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=82c90207-af7d-495b-b437-aa9a4c72f4e8',
        'company_name': 'Winnebago Industries',
        'spider_class': 'adp_wfn'
    },
    {
        'url': 'https://recruiting2.ultipro.com/AMS1003AMSII',
        'company_name': 'Amsted Industries',
        'spider_class': 'ultipro'
    },
    {
        'url': 'https://recruiting.ultipro.com/ARC1018',
        'company_name': 'ARCH',
        'spider_class': 'ultipro'
    },
    {
        'url': 'https://recruiting.ultipro.com/PRO1027PROMA',
        'company_name': 'ProMach',
        'spider_class': 'ultipro'
    },
    {
        'url': 'https://recruiting.ultipro.com/COM1037COMAR',
        'company_name': 'Comar',
        'spider_class': 'ultipro'
    },
]


def scrape():
    configs = test_configs[:1]

    scraper = ScraperRunner()
    scraper.run(configs)
    return 0


scrape()
