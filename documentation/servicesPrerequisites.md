# Service Prerequisites

## Create Authentication Setup
A one time task of configuring the API Gateway CloudWatch log role must be performed before any of the services can be created.

1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name ApiGatewayCloudwatch-Role --template-body file://api-logging.yaml \
     --enable-termination-protection \
     --capabilities CAPABILITY_NAMED_IAM
    ```
