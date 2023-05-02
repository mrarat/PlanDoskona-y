# PlanDoskonaly
Project is prepared to be deployed on [Heroku](https://www.heroku.com)

## Configuration in heroku dashboard:
In heroku dashboard set buildpacks to (order matters) :
1. heroku/nodejs
2. heroku/python

Set environment variables (config vars) : 
- `DJANGO_DEBUG` = FALSE
- `SECRET_KEY` = \<your secret key\>
- `VITE_API_URL` = \<link to your website\>

## Link
Hosted on : https://plandoskonaly.herokuapp.com/