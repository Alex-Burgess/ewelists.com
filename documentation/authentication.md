# User Authentication
Useful AWS documentation: [Adding Social Identity Providers to a User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)

## Create Authentication Setup
1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name Auth-Test \
     --template-body file://auth.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=Environment,ParameterValue=test \
     --enable-termination-protection
    ```
1. Configure UserPool:
  1. Callback URL(s): http://localhost:3000/
  1. Sign out URL(s): http://localhost:3000/
  1. Allowed OAuth Flows: Authorization code grant
  1. Allowed OAuth Scopes: email, openid, aws.cognito.signin.user.admin, profile.
  1. Domain Name: test-ewelists
1. Configuring social authentication with LoginWithAmazon.
  1. Create [Amazon](https://developer.amazon.com/login-with-amazon) developer account.
  1. Create Security Profile - [Steps](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)
  1. Update app ID, secret and scope in Identity providers.
1. Configuring social authentication with Google
  1. Create [Google](https://console.developers.google.com) developer account.
  1. Create OAuth client IDs - [Steps](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)
  1. Update app ID, secret and scope in Identity providers.
1. Configuring social authentication with Facebook
  1. Create [Facebook](https://developers.facebook.com/) developer account.
  1. Create App ID - [Steps](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)
  1. Update app ID, secret and scope in Identity providers.
1. Enable all Identity Providers in App Client Settings and select Allowed OAuth Flows and Scopes (console).
1. Update Attribute mappings for the email attribute for each identity provider.
1. Add the configuration to the config.js file in the React Web App.
1. Create SSM parameter with user pool ID, which is specified as an environment variable in the cf template for the signup lambda function.
    ```
    aws ssm put-parameter --name /CognitoUserPoolId/test --type String \
     --value "eu-west-1_abcd123e4"
    ```
