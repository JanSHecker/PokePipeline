i. Project Description

This fastAPI project utilizes the PokeAPI to populate a postgres database with Pokemon, their types and their moves. The app also has a frontend where the pipeline is started and data is displayed.
The app has graphQL endpoints that can also be accessed through the strawberry WebUI and the contents of the database can be accessed through adminer.

ii. How to run

To run the app type "docker compose -up" in the console (Docker must be running).
You can then access the frontendpage on http://localhost:80
You can access adminer on http://localhost:8080 (login with postgres/postgres)
You can access the strawberry graphQL WebUI on http://localhost:8000/graphql

iii. Design Choices

At the core of my databse schema i created 3 tables for Pokemon, Types and Moves. I choose those 3 as base because they have the most interesting relationship between each other. Each Pokemon has both moves and types. Each Type has both Pokemon and moves. And each move has Pokemon its learned by and a type.
I use graphql to access the pokeAPI which allows me to already pre-filter the response I will receive. That makes it more easy to feed the relevant data into the database. I also use graphql to communicate with my frontend which allows me to only have one endpoint. Additionally, it enables us to use the starwberry webUI as another pathway to review the contents of the database.

iv. Assumptions

One assumption ive made is that the total number of pokemon in the PokeAPI is 1118 this number could change when the API is updated to includes Pokemon released with future games.
Entrees of Pokemon are considered as their type of pokemon not an instance of a Pokemon. Alternatively it would be possible for the same type of pokemon to appear twice just with a different Id (this would necessitate to save the pokeAPI id as a extra column independent of our databses id)

v. Future Additions

The pipeline could be expanded in the future by including more columns into the database.
Also the frontend could be expanded possibly using a framework like react. This includes allowing for advanced sorting and filtering etc.
