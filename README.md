```
git clone -b main git@gitlab.com:gip-python/plot.git
```

```
docker-compose up -d --build
```

```
docker-compose exec web ./manage.py createsuperuser
```

Start unit test
```
sudo docker-compose exec web python manage.py test
```

Start django test coverage
```
sudo docker-compose exec web coverage report
```