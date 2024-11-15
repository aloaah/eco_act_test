## To run
* j'ai utiliser python 3.10.6 pendant le developpement.  
* setup venv
* install requirements
* Si vous voulez utiliser postegreSQL, il faut remplir le .env et rajouter un field ENVIRONMENT dans les variables d'environements. Une database emission_data doit être presente sur le server postgres (non tester)

* pour run l'appli dash: `python dash_app/app.py`
* pour fill la database `python -m src.init_database`
* pour run le server fastapi: `uvicorn src.main:app` on a besoin du fichier de db 

### Overall Improvements
* Clean the instalation process, using poetry as the dependecy manager, have a pyproject.toml
* Add tests for upload/clean data/rest endpoints
* Add posibilty to change the path of the file being loaded
* type hints/ docstrings
* better cleaning, think there is value in some columns that I did not use such as code_de_la_categorie/tags_français (could be used for REST Api filtering)
* some refining of the database models/ normalization of the database
* add logging for the databases insertions
* Add error handling on the database insertions
* Decoupling ETL and Rest api
  

### Improvements dash_app
* for simplicity, i used the xlsx directly, using the cleaned data, directly from the db would be better
* add css themes etc
* better graph to allow for comparaison between categories of elements

### Improvement fastApi
* Database should be filled only if it's not already filled with the data
* Handling of conflict in create element
* Define status code for errors
* Add pagination

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
