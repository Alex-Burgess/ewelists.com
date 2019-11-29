# Monitoring

We backup dynamodb data and cognito user pool, so that in the event of a complete disaster we would have everything we would need to rebuild from scratch.

*Note:* Could think about storing backups in another region for more options.


## DynamoDB
Point-in-time-recovery provides continuous backups of the table data, for the last 35 days.  See [Documentation](https://aws.amazon.com/dynamodb/backup-restore/) for more detail.
