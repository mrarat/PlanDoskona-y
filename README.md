# PlanDoskonaly
[![codecov](https://codecov.io/gh/mrarat/PlanDoskonaly/branch/main/graph/badge.svg?token=RSMF9W3TF7)](https://codecov.io/gh/mrarat/PlanDoskonaly)

Project is prepared to be deployed on [Heroku](https://www.heroku.com)

## Configuration in heroku dashboard:
In heroku dashboard set buildpacks to (order matters) :
1. heroku/nodejs
2. heroku/python

Set environment variables (config vars) : 
- `DJANGO_DEBUG` = False
- `SECRET_KEY` = \<your secret key\>
- `VITE_API_URL` = \<link to your website\>
- `HEROKU` = True

## Link
Hosted on : https://plandoskonaly.herokuapp.com/