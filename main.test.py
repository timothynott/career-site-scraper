from project.process.scraper_runner import ScraperRunner


def scrape():
    configs = [
        {
            'company_name': 'Cornell Pump',
            'url': 'https://recruiting.ultipro.com/ROP1001ROPER/JobBoard/5635cac7-6c69-44a7-850c-cf35112ce343',
            'spider_class': 'ultipro'
        },
        # {
        #     'company_name': 'Cornell Pump II',
        #     'url': 'https://recruiting.ultipro.com/ROP1001ROPER/JobBoard/5635cac7-6c69-44a7-850c-cf35112ce343',
        #     'spider_class': 'ultipro'
        # },
        # {
        #     'company_name': 'Cornell Pump III',
        #     'url': 'https://recruiting.ultipro.com/ROP1001ROPER/JobBoard/5635cac7-6c69-44a7-850c-cf35112ce343',
        #     'spider_class': 'ultipro'
        # }
    ]

    runner_config = {
        'CONCURRENT_CRAWLS': 2
    }

    scraper = ScraperRunner(config=runner_config)
    scraper.run(configs)
    return 0


scrape()


# test_configs_simple_concurrency = [
#     {
#         'company_name': 'Cornell Pump',
#         'url': 'https://recruiting.ultipro.com/ROP1001ROPER/JobBoard/5635cac7-6c69-44a7-850c-cf35112ce343',
#         'spider_class': 'ultipro'
#     },
#     {
#         'company_name': 'Cornell Pump II',
#         'url': 'https://recruiting.ultipro.com/ROP1001ROPER/JobBoard/5635cac7-6c69-44a7-850c-cf35112ce343',
#         'spider_class': 'ultipro'
#     },
#     {
#         'company_name': 'Cornell Pump III',
#         'url': 'https://recruiting.ultipro.com/ROP1001ROPER/JobBoard/5635cac7-6c69-44a7-850c-cf35112ce343',
#         'spider_class': 'ultipro'
#     }
# ]

# test_configs = [
#     {
#         'url': 'https://jobs-cantelmedical.icims.com/jobs/search?ss=1',
#         'company_name': 'Cantel Medical',
#         'spider_class': 'icims',
#     },
#     {
#         'url': 'https://external-weatherford.icims.com/jobs/search?ss=1',
#         'company_name': 'Weatherford',
#         'spider_class': 'icims'
#     },
#     {
#         'url': 'https://globalcareers-entegrisinc.icims.com/jobs/search?ss=1',
#         'company_name': 'Entegris, Inc.',
#         'spider_class': 'icims'
#     },
#     {
#         'url': 'https://globalhub-berryglobal.icims.com/jobs/search?ss=1',
#         'company_name': 'Berry Global Inc.',
#         'spider_class': 'icims'
#     },
#     {
#         'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=08cf914d-e2d5-4aba-b95c-c33cf076da39',
#         'company_name': 'Rice Lake Weighing Systems',
#         'spider_class': 'adp_workforcenow'
#     },
#     {
#         'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=5af0373a-89ae-488e-b298-4066fdc2232a',
#         'company_name': 'SP Industries',
#         'spider_class': 'adp_workforcenow'
#     },
#     {
#         'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=66d93efd-a316-4416-9647-78a8a2fa5359',
#         'company_name': 'Tecomet Talented',
#         'spider_class': 'adp_workforcenow'
#     },
#     {
#         'url': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=82c90207-af7d-495b-b437-aa9a4c72f4e8',
#         'company_name': 'Winnebago Industries',
#         'spider_class': 'adp_workforcenow'
#     },
#     {
#         'url': 'https://recruiting2.ultipro.com/AMS1003AMSII',
#         'company_name': 'Amsted Industries',
#         'spider_class': 'ultipro'
#     },
#     {
#         'url': 'https://recruiting.ultipro.com/ARC1018',
#         'company_name': 'ARCH',
#         'spider_class': 'ultipro'
#     },
#     {
#         'url': 'https://recruiting.ultipro.com/PRO1027PROMA',
#         'company_name': 'ProMach',
#         'spider_class': 'ultipro'
#     },
#     {
#         'url': 'https://recruiting.ultipro.com/COM1037COMAR',
#         'company_name': 'Comar',
#         'spider_class': 'ultipro'
#     },
# ]
