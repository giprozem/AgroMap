```
📂 **AgroMap**
│
├── 📁 account
│   ├── 📁 admin
│   │   └── 📄 account.py
│   ├── 📁 migrations
│   ├── 📁 models
│   │   └── 📄 account.py
│   ├── 📁 serializers
│   │   └── 📄 authenticated.py
│   ├── 📁 tests
│   │   ├── 📄 factories.py
│   │   ├── 📄 test_admin.py
│   │   └── 📄 tests.py
│   ├── 📁 views
│   │   └── 📄 authenticated.py
│   ├── 📄 apps.py
│   ├── 📄 authentication.py
│   ├── 📄 translation.py
│   └── 📄 urls.py
│
├── 📁 ai
│   ├── 📁 admin
│   │   ├── 📄 create_dataset.py
│   │   ├── 📄 predicted_contour.py
│   │   └── 📄 productivity.py
│   ├── 📁 migrations
│   ├── 📁 culture_AI
│   │   └── 📄 predict_culture.py
│   ├── 📁 models
│   │   ├── 📄 create_dataset.py
│   │   ├── 📄 predicted_contour.py
│   │   └── 📄 productivity.py
│   ├── 📁 productivity_funcs
│   │   └── 📄 predicting.py
│   ├── 📁 serializers
│   │   ├── 📄 create_dataset.py
│   │   ├── 📄 predicted_contour.py
│   │   └── 📄 productivity.py
│   ├── 📁 tests
│   │   ├── 📄 factories.py
│   │   └── 📄 tests.py
│   ├── 📁 views
│   │   ├── 📄 create_dataset.py
│   │   ├── 📄 heat_map_ndvi.py
│   │   ├── 📄 predict_culture.py
│   │   ├── 📄 predicted_contour.py
│   │   └── 📄 productivity.py
│   ├── 📁 utils
│   │   ├── 📄 create_dataset.py
│   │   └── 📄 predicted_contour.py
│   ├── 📄 apps.py
│   ├── 📄 signals.py
│   ├── 📄 translation.py
│   └── 📄 urls.py
│
├── 📁 auditlog
│   ├── 📁 management
│   │   └── 📁 commands
│   │       ├── 📄 auditlogflush.py
│   │       └── 📄 auditlogmigratejson.py
│   ├── 📁 migrations
│   ├── 📄 admin.py
│   ├── 📄 apps.py
│   ├── 📄 cid.py
│   ├── 📄 conf.py
│   ├── 📄 context.py
│   ├── 📄 diff.py
│   ├── 📄 filters.py
│   ├── 📄 middleware.py
│   ├── 📄 mixins.py
│   ├── 📄 models.py
│   ├── 📄 receivers.py
│   ├── 📄 registry.py
│   ├── 📄 signals.py
│
├── 📁 config
│   ├── 📄 asgi.py
│   ├── 📄 settings.py
│   ├── 📄 urls.py
│   └── 📄 wsgi.py
│
├── 📁 culture_model
│   ├── 📁 admin
│   │   ├── 📄 common.py
│   │   └── 📄 pasture_culture.py
│   ├── 📁 migrations
│   ├── 📁 models
│   │   ├── 📄 decade.py
│   │   ├── 📄 index_plan.py
│   │   ├── 📄 pasture_culture.py
│   │   ├── 📄 phase.py
│   │   └── 📄 vegetation_index.py
│   ├── 📁 serializers
│   │   └── 📄 index.py
│   ├── 📁 tests
│   │   ├── 📄 factories.py
│   │   └── 📄 tests.py
│   ├── 📁 views
│   │   └── 📄 veg_indexes.py
│   ├── 📄 apps.py
│   ├── 📄 translation.py
│   └── 📄 urls.py
│
├── 📁 gip
│   ├── 📁 admin
│   │   ├── 📄 base.py
│   │   ├── 📄 contact_information.py
│   │   ├── 📄 conton.py
│   │   ├── 📄 contour.py
│   │   ├── 📄 crop_yield.py
│   │   ├── 📄 culture.py
│   │   ├── 📄 district.py
│   │   ├── 📄 farmer.py
│   │   ├── 📄 region.py
│   │   └── 📄 soil.py
│   ├── 📁 migrations
│   ├── 📁 exceptions
│   │   └── 📄 shapefile_exceptions.py
│   ├── 📁 models
│   │   ├── 📄 base.py
│   │   ├── 📄 contact_information.py
│   │   ├── 📄 conton.py
│   │   ├── 📄 contour.py
│   │   ├── 📄 crop_yield.py
│   │   ├── 📄 culture.py
│   │   ├── 📄 district.py
│   │   ├── 📄 farmer.py
│   │   ├── 📄 region.py
│   │   └── 📄 soil.py
│   ├── 📁 pagination
│   │   └── 📄 contour_pagination.py
│   ├── 📁 serializers
│   │   ├── 📄 contact_information.py
│   │   ├── 📄 conton.py
│   │   ├── 📄 contour.py
│   │   ├── 📄 crop_yield.py
│   │   ├── 📄 culture.py
│   │   ├── 📄 district.py
│   │   ├── 📄 land_use.py
│   │   ├── 📄 landtype.py
│   │   ├── 📄 region.py
│   │   └── 📄 soil.py
│   │
│   ├── 📁 services
│   │   └── 📄 shapefile.py
│   ├── 📁 tests
│   │   ├── 📄 factories.py
│   │   ├── 📄 polygon.py
│   │   ├── 📄 test_additional_views.py
│   │   └── 📄 tests.py
│   ├── 📁 views
│   │   ├── 📄 contact_information.py
│   │   ├── 📄 conton.py
│   │   ├── 📄 contour.py
│   │   ├── 📄 culture.py
│   │   ├── 📄 district.py
│   │   ├── 📄 handbook_contour.py
│   │   ├── 📄 landtype.py
│   │   ├── 📄 polygon_and_point_in_polygon.py
│   │   ├── 📄 region.py
│   │   ├── 📄 shapefile.py
│   │   ├── 📄 soil.py
│   │   ├── 📄 statistics.py
│   │   └── 📄 ...
│   ├── 📄 apps.py
│   ├── 📄 signals.py
│   ├── 📄 translation.py
│   └── 📄 urls.py
│
├── 📁 hub
│   ├── 📁 admin
│   │   ├── 📄 category_type_list.py
│   │   ├── 📄 document_type_list.py
│   │   ├── 📄 land_info.py
│   │   ├── 📄 land_type_list.py
│   │   └── 📄 property_type_list.py
│   ├── 📁 migrations
│   ├── 📁 models
│   │   ├── 📄 base.py
│   │   ├── 📄 category_type_list.py
│   │   ├── 📄 document_type_list.py
│   │   ├── 📄 land_info.py
│   │   ├── 📄 land_type_list.py
│   │   └── 📄 property_type_list.py
│   ├── 📁 serializers
│   │   └── 📄 land_info.py
│   ├── 📁 tests
│   │   ├── 📄 test_zem_balance.py
│   │   ├── 📄 tests_authenticated.py
│   │   └── 📄 tests_land_info.py
│   ├── 📁 views
│   │   ├── 📄 authenticated.py
│   │   ├── 📄 elevation_and_soil.py
│   │   ├── 📄 handbook_asr.py
│   │   ├── 📄 land_info.py
│   │   ├── 📄 veterinary_service.py
│   │   ├── 📄 zem_balance_api.py
│   │   └── 📄 ...
│   ├── 📄 apps.py
│   └── 📄 urls.py
│
├── 📁 scripts
│   ├── 📄 create_veg_indexes_ai.py
│   ├── 📄 create_veg_indexes_gip.py
│   ├── 📄 cron_ai_geoserver.py
│   ├── 📄 cron_download_S2_Copernicus.py
│   ├── 📄 cron_geoserver.py
│   ├── 📄 heat_map_ndvi.py
│   ├── 📄 kafka_consumer.py
│   ├── 📄 productivity_contour.py
│   └── 📄 ...
│
├── 📄 docker-compose.yml
├── 📄 Dockerfile
├── 📄 .env
├── 📄 .envExample
├── 📄 .gitignore
├── 📄 .dockerignore
└── 📄 requirements.txt
```