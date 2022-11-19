# g-data-exercise

## Architecture
This solution heavily relies on docker containers and compose.

For each endpoint it will trigger a different container, all of them connected.
The postgres container has a init script that sets the table required per the required description.

## Pre requisites
Have docker and docker compose installed

## Steps to initialize applications
Run `docker compose up -d` at the root of the repository.

Applications endpoints:
```
 - localhost:5001/upload := endpoint to upload data
 - localhost:5002/backup := endpoint to create a backup
 - localhost:5002/backup := endpoint to restore a backup
 - localhost:5003/metric1 := endpoint to get metric #1
 - localhost:5003/metric2 := endpoint to get metric #2
```

## Steps to upload data
Once docker compose is up and running, you can run the following command from the root of the repo:

```bash
curl --location --request POST 'localhost:5001/upload' \ --form 'file=@"test/departments.csv"'
```

If everything is ok, you should receive a similar message, as the one below:
```json
{
  "response": "successfully saved the file and processed it with status: 0"
}
```

## Steps to take a backup or restore one
Once docker compose is running and there is data in the database, you can run the following command to take a backup:

```bash
curl --location --request POST 'localhost:5002/backup'
```

If everything is ok, you should receive a similar message, as the one below:

```json
{
    "response": "backups were taken sucessfully"
}
```

Similar, for restore a backup, you can run the following:

```bash
curl --location --request POST 'localhost:5002/restore'
```

Please consider the backup will restore tables with a 2 at the end, e.g: jobs2 instead of job, for comparisson purposes.

## Steps to get the metrics:
For get the metrics for challenge #2, you can run the following
```bash
 - curl --location --request POST 'localhost:5003/metric1'
 - curl --location --request POST 'localhost:5003/metric2'
```

## Visualization
Additionally, the docker compose file contains a Metabase image with the two metrics plotted in the link `http://0.0.0.0:3000/dashboard/1-globant`.
There is a persistance file which is being used by the container.

## Room to improve
 - Code can be improved, packages can be created to hold common functions.
 - Code should be unit tested in order to assure the quality and handling different scenarios.
 - For backup and restore, if the database growth its size, would greatly benefit from using a distributed framework such as Spark or Sqoop.
 - Endpoints would benefit its security in having both authentication and documentation for its usage.

## Tests done
 - Upload files, correctly and incorrectly, with chunk size 1. For logs, there is a table called error_log which holds the rows that failed.
 - Backup and restore all tables.
 - Get metrics through the endpoints.
 - See the visuals done by the requirement.