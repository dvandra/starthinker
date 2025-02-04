# Deploying StarThinker UI For Enterprise Multi User 

When multiple users need to deploy and coordinate multiple reipces for multiple clients, stand up the UI.
The UI allows each user to authenticate and manage solutions leaving the development team free to create
and maintain the technical recipe scripts.  The UI deploys on AppEngine with a distributed worker back 
end on Google Cloud Instances. Execute the following to stand up the UI:

```
git clone https://github.com/google/starthinker
```
```
cd starthinker
```
```
source install/deploy.sh
```

 1. Option 3) Enterprise Setup Menu 
 1. Option 1) Deploy App Engine UI
   - You will be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
   - You will be asked for [Service Credentials](cloud_service.md).
   - You will be asked for [Web Client Credentials](cloud_client_web.md).
   - You will be asked for a databse user and password, remember this ( database name is starthinker ).
 1. Option 2) Deploy Job Workers
   - Option 1) Test - 1 Job ( not recommended for running large jobs )
   - Option 3) Medium - 20 Jobs ( recommended for enterprise )
   - Option 5) Quit
 1. Option 3) Check Job Workers
 1. Enable backups for your [Google Cloud SQL](https://pantheon.corp.google.com/sql).
 1. Enable [Google Cloud IAP](https://pantheon.corp.google.com/security/iap) to restrict access to the UI.
 1. Start using the UI to create and deploy jobs.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_enterprise.md)

Next, learn how to [deploy a recipe](ui_recipe.md).

## Notes

 - The UI can be deployed as many times as necessary.
 - The workers can be deployed as many times as necessary but must be deleted manually.
 - Migrations are automatically run when deploying the UI.
 - Cost of an enterprise deployment UI, workers, and database, is roughly $500 / month. 
 - Google Cloud resource use such as BigQuery billing depends on the jobs run.
 

## Cloud Resources

  - [Google Cloud AppEngine](https://pantheon.corp.google.com/appengine) - where your instance will deploy.
  - [Google Cloud SQL](https://pantheon.corp.google.com/sql) - where your database will deploy.
  - [Google Cloud StackDriver Logs](https://pantheon.corp.google.com/logs/viewer) - where your logs will be written ( select StarThinker under All Logs ).
  - [Google Cloud Storage](https://pantheon.corp.google.com/storage/browser) - where your user credentials will be stored ( keep this secure ).
  - [Google Compute Engine Instances](https://pantheon.corp.google.com/compute/instances) - where your workers will be deployed.
  - [Google Cloud Credentials](https://pantheon.corp.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud IAP](https://pantheon.corp.google.com/security/iap) - where you restrict access to AppEngine.
  - [Google Cloud Billing](https://pantheon.corp.google.com/billing/linkedaccount) - examine costs in real time.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
