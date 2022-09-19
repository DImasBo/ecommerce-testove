# MyEcommerce

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).


### How to get started on a project

* Start the stack with Docker Compose:

```bash
docker-compose up --build -d
```
* make migration

```bash
docker-compose run --rm backend  alembic upgrade head
```

* init first data for test API

```bash
docker-compose run --rm backend python app/initial_data.py
```

![image](https://user-images.githubusercontent.com/52758126/191000389-239c50da-0162-473e-a52b-a14944733891.png)

* after than we can open swagger-UI http://localhost:8888/api/v1/docs

* can use collection `MyEcommerce.postman_collection.json` for Postman



## Defaults, we have 4 users 

*Super User(Admin):*

login:
 `admin@example.com` 
password: `changethis`


*sales-consultant(Продавець-консультант):*

login:
 `sales-consultant@example.com` 
password: `changethis`

*Cashier(Касир):*

login:
 `cashier@example.com` 
password: `changethis`


*Accountant(Бугалтер): *

login:
 `accountant@example.com` 
password: `changethis`

for login some user
need use autoraize button from swagger-UI
![image](https://user-images.githubusercontent.com/52758126/191001935-dd1ce0a4-512e-4dfb-a557-3fd1fa32e251.png)


## Test Workflow Manual 
![image](https://user-images.githubusercontent.com/52758126/191022004-af158678-6eb9-4736-bb13-d6d5fa16f93a.png)
#### Test 1
- [x]  кассир получает заказ от клиента. В одном заказе может быть только один продукт
  - [x] добавляет этот заказ в базу данных

1. Cashier login to Swagger-UI

![image](https://user-images.githubusercontent.com/52758126/191020466-b007fbd8-8430-4d14-8334-43f12dd1d11b.png)

2. Cashier reads products

![image](https://user-images.githubusercontent.com/52758126/191020513-36de50ae-1730-49d4-b073-d2d84b72a9ba.png)

3. Cashier create order

![image](https://user-images.githubusercontent.com/52758126/191020561-c9fd1c29-8463-48e2-b6a8-ef7ccf90ed78.png)

#### Test 2

- [x] продавец-консультант может видеть созданный заказ 
  - [x] обрабатывает его и затем изменяет его статус на «выполнено»

1. login sales-consultant in system 

![image](https://user-images.githubusercontent.com/52758126/191020643-9852e16f-9e9e-495c-99d9-e56838f8fcfb.png)

2. sales-consultant reads orders

![image](https://user-images.githubusercontent.com/52758126/191020704-d05e9cd6-5ce8-4fde-939d-50b552da202f.png)

3. sales-consultant picks up some order

![image](https://user-images.githubusercontent.com/52758126/191020733-85309ed3-53c2-4c12-985d-fcf3ccc3a025.png)

4. sales-consultant updates status order to READY

![image](https://user-images.githubusercontent.com/52758126/191020777-0b522c81-a895-44c1-9166-422b16351986.png)

#### Test 3

- [x] После этого:
  - [x] кассир может сгенерировать счет 
  - [x] принять оплату от клиента и изменить статус заказа на «оплачен»

1. Cashier login to system

![image](https://user-images.githubusercontent.com/52758126/191020466-b007fbd8-8430-4d14-8334-43f12dd1d11b.png)

2. Cashier creates bill for Order

![image](https://user-images.githubusercontent.com/52758126/191020900-2139a779-f2b3-46e8-ac57-6007cd3ff9fb.png)

3. Cashier makes bill to PAID

![image](https://user-images.githubusercontent.com/52758126/191020932-2387d907-e489-4b87-a78b-320ac44954b6.png)

#### Test 4
- [x]
В любое время бухгалтер может видеть все заказы, их статусы, дату, скидку и тд.
Бухгалтер указывает промежуток дат по которым необходимо вывести данные о заказах.
Например: показать все заказы с 01.07.2019 до 31.07.2019

1. Accountant login to system

![image](https://user-images.githubusercontent.com/52758126/191021749-27e3a558-f191-4daf-98c6-440ae2d146e0.png)

2. Then Accountant can read some orders, produtcs, bills 

![image](https://user-images.githubusercontent.com/52758126/191022346-7a4e9238-b8a2-438f-a386-ba8e99a0eabf.png)

for example:

![image](https://user-images.githubusercontent.com/52758126/191022274-8cdb3046-c300-407c-8438-1b8508ecf3bc.png)

## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose up --build -d
```

* Now you can open your browser and interact with these URLs:

Frontend, built with Docker, with routes handled based on the path: http://localhost:8888

Backend, JSON based web API based on OpenAPI: http://localhost:8888/api/v1/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8888/api/v1/docs


**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```


### Local tests

Start the stack with this command:

```Bash
DOMAIN=backend sh ./test-local.sh
```
![image](https://user-images.githubusercontent.com/52758126/191039228-d3d26fb0-c399-47c0-a6dc-d999f0f2116e.png)

### Migrations

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

* Start an interactive session in the backend container:

```console
$ docker-compose exec backend bash
```

* If you created a new model in `./backend/app/app/models/`, make sure to import it in `./backend/app/app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.
