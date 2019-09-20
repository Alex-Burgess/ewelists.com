# Monitoring
Route53 Health Checks can be used to monitoring the availability of the website.  Combining this with CloudWatch Alarms and SNS, it is then possible to send emails when issues occur.  In addition to basic availability monitoring, we also monitor requests received by the CloudFront distribution.

We want to monitor a page that has no cache, so that we alerted if there is an issue with underlying static website (i.e. on s3) a.s.a.p.  As files can be cached for days, there could be an issue and we wouldn't find out for hours, which would also be at the same time that users find out about the issue.  To facilitate this, we use a static html page with no cache.  For staging and production the buildspec file takes cache of copying this file with the correct no-cache metadata.

## Creating Monitoring
1. **CloudFront ID:** Get the Primary CloudFront Distribution ID
    ```
    aws cloudformation describe-stacks --stack-name Web-Test \
     --query 'Stacks[].Outputs[?OutputKey==`WebCloudFrontID`].OutputValue' --output text
    ```

1. **Health Checks:** Create the health checks stack (us-east-1)
    ```
    aws cloudformation create-stack --region us-east-1 --stack-name Web-HealthChecks-Test --template-body file://web-healthchecks.yaml \
     --parameters ParameterKey=Environment,ParameterValue=test \
      ParameterKey=CloudFrontId,ParameterValue=12345678910
    ```
1. **Confirm Subscription:** An email requesting confirmation of the subscription for the email address will be sent.  Click on the link to confirm the subscription.
