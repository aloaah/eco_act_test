## To run
* setup venv
* install requirements
* Si vous voulez utiliser postegreSQL, il faut remplir le .env et rajouter un field ENVIRONMENT dans les variables d'environements. Une database emission_data doit être presente sur le server postgres (non tester)

* run: `python -m src.main`
* cela devrait créer un fichier data/cleaned_data_dev_python.csv

* ce fichier est utiliser pour l'appli dash.

* pour run l'appli dash: `python dash_app/app.py`


### Improvements src
* Clean the instalation process, using poetry as the dependecy manager, have a pyproject.toml
* Add tests for upload/clean data
* Add posibilty to pass a path to the main script
* type hints/ docstrings
* better cleaning, think there is value in some columns that I did not use such as code_de_la_categorie/tags_français (could be used for REST Api filtering)
* some refining of the database models 

* the fast_api server could be built along side the etl, as all the models are already defined there.

### Improvements dash_app
* for simplicity, i used the csv directly, but puting it in a db would be better
* add css themes etc
* better graph to allow for comparaison between categories of elements


## Exposing the data
* we could follow the current database models and having for exemple:

#### Element
- `GET /elements/`
- `GET /elements/{element_id}`
- `POST /elements/`
- `PUT /elements/{element_id}`
- `DELETE /elements/{element_id}`
- `GET /elements/{element_id}/emissions`
- `GET /elements?localisation={localisation}`

#### Emission Data
- `GET /emission-data/`
- `GET /emission-data/{emission_id}`
- `POST /emission-data/`
- `PUT /emission-data/{emission_id}`
- `DELETE /emission-data/{emission_id}`

#### Quality Metrics
- `GET /quality-metrics/`
- `GET /quality-metrics/{quality_id}`
- `POST /quality-metrics/`
- `PUT /quality-metrics/{quality_id}`
- `DELETE /quality-metrics/{quality_id}`
- `GET /emission-data/{emission_id}/quality-metrics`

#### Process Types
- `GET /process-types/` 
- `GET /process-types/{process_id}` 
- `POST /process-types/`
- `PUT /process-types/{process_id}`
- `DELETE /process-types/{process_id}`
- `GET /emission-data/{emission_id}/process-types`
