# for footprint in footprints:
#     print(current_date.strftime("%Y%m%d"))
#     print(first_day_of_previous_month.strftime("%Y%m%d"))
#     products = api.query(footprint.polygon.wkt,
#                          date=('20230301', '20230330'),
#                          platformname='Sentinel-2',
#                          processinglevel='Level-2A',
#                          cloudcoverpercentage=(0, 20))