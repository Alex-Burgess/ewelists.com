# Monitoring

We backup dynamodb data and cognito user pool, so that in the event of a complete disaster we would have everything we would need to rebuild from scratch.

*Note:* Could think about storing backups in another region for more options.


## DynamoDB
Point-in-time-recovery provides continuous backups of the table data, for the last 35 days.  See [Documentation](https://aws.amazon.com/dynamodb/backup-restore/) for more detail.

## Cognito
Cognito does not have a backup option.

There are two independent tools:
- https://www.npmjs.com/package/cognito-backup
- https://www.npmjs.com/package/cognito-backup-restore

Both seem to perform backup and restore.  Using cognito-backup for now.

Install:
```
npm install -g cognito-backup
```

Get user pool ids:
```
aws cognito-idp list-user-pools --max-results 10
```

Backup:
```
cognito-backup backup-users eu-west-1_vqox9Z8q7 --region eu-west-1 --file userpool-test-`date +"%Y-%m-%d"`.json
```

Copy backup to s3 bucket:
```
aws s3 cp userpool-test-2019-11-29.json s3://cognito-ewelists-backups-test
```
