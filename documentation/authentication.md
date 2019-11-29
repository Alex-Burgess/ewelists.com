# User Authentication
Useful AWS documentation: [Adding Social Identity Providers to a User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)

## Create Authentication Setup
1. Add social identity providers to parameter store:
    ```
    aws ssm put-parameter --name /ewelists.com/test/Facebook/ClientId --type String --value "123456789012345"
    aws ssm put-parameter --name /ewelists.com/test/Facebook/ClientSecret --type String --value "123456789012345"

    aws ssm put-parameter --name /ewelists.com/test/Google/ClientId --type String --value "123456789012345"
    aws ssm put-parameter --name /ewelists.com/test/Google/ClientSecret --type String --value "123456789012345"

    aws ssm put-parameter --name /ewelists.com/test/Amazon/ClientId --type String --value "123456789012345"
    aws ssm put-parameter --name /ewelists.com/test/Amazon/ClientSecret --type String --value "123456789012345"
    ```
1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name Auth-Test \
     --template-body file://auth.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --enable-termination-protection \
     --parameters ParameterKey=Environment,ParameterValue=test
    ```

1. Create SSM parameter with user pool ID, which is specified as an environment variable in the cf template for the signup lambda function.
    ```
    aws ssm put-parameter --name /CognitoUserPoolId/test --type String \
     --value "eu-west-1_abcd123e4"
    ```

## Update stack (BACKUP COGNITO FIRST)
*NOTE:* Backup the user pool before performing an update.  Just in case a "replace" resource action has on userpool and user data is lost.

Get user pool ids:
```
aws cognito-idp list-user-pools --max-results 10
```

Backup:
```
cognito-backup backup-users <USERPOOL_ID> --region eu-west-1 --file userpool-<ENV>-`date +"%Y-%m-%d"`.json
```

Copy backup to s3 bucket:
```
aws s3s cp userpool-<ENV>-2019-11-29.json s3://cognito-ewelists-backups-<ENV>
```

Update stack (BACKUP COGNITO FIRST):
```
aws cloudformation update-stack --stack-name Auth-Test \
 --template-body file://auth.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --parameters ParameterKey=Environment,ParameterValue=test
```

## Checklist (May be outdated)
1. Callback Url(s)
1. Signout Url(s)
1. Allowed OAuth Flows: Authorization code grant
1. Allowed OAuth Scopes: email, openid, aws.cognito.signin.user.admin, profile.
1. Domain Name
1. Social Authentication providers (Facebook, Google, LoginWithAmazon), with attribute mappings.
1. React config.js
1. Lambda triggers
1. Email configuration
