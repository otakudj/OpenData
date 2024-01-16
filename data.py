from datetime import datetime

now = datetime.now()
year = now.year
month = now.month
date_gen = []
for ele in range(36):
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1

    date_gen.append(f'{year}{month:02d}')

# reference:
# http://www.pbc.gov.cn/diaochatongjisi/resource/cms/
social_financing = [
    13.0, 13.3, 12.3, 11.7, 11.0, 11.0, 10.7, 10.3, 10.0, 10.0, 10.1, 10.3,
    10.5, 10.2, 10.5, 10.2, 10.5, 10.8, 10.7, 10.5, 10.6, 10.3, 10.0, 9.6,
    9.4, 9.9, 10.0, 10.0, 9.5, 9.0, 8.9, 9.0, 9.0, 9.3, 9.4, 9.5,
]

