# To run project use following command
    uvicorn main:app --reload


`/etc/supervisor/conf.d/fastapi-app.conf`


`sudo supervisorctl status fastapi-app`

`sudo supervisorctl start fastapi-app`

`sudo supervisorctl restart fastapi-app`


test data to test post request http://0.0.0.0:8000
```json
{
    "number_of_rooms": 10,
    "floor": 1,
    "number_of_floors": 6,
    "sub_district": "Mirzo Ulugbek",
    "repair": "full",
    "area": "150",
    "landmark": "test",
    "price": "55000",
    "description": "test description",
    "photos": ["https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_640.jpg", "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_640.jpg"]
}
```

 systemctl daemon-reload
 sudo systemctl restart fastapi-app
 sudo systemctl status fastapi-app
