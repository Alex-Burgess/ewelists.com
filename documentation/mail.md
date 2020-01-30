# Email
Email is manually configured using AWS Workmail.  Note, when creating a user, ensure that the domain selected is the right one.

Email address: contact@ewelists.com
Web Email client: https://ewelists.awsapps.com/mail

SES is used to send emails, for signup confirmation emails, as well as welcome emails.


## Welcome Email Template
To test the template, edit welcome-template.html and view in a browser.

### Updates
To create the ses template, ensure that the html and text content is updated in the welcome.yaml CloudFormation template file.
```
aws cloudformation create-stack --stack-name Email-Template-Welcome-Test \
 --template-body file://welcome.yaml \
 --parameters ParameterKey=Environment,ParameterValue=test
```


### Updates
To update an email template:
```
aws cloudformation update-stack --stack-name Email-Template-Welcome-Test \
 --template-body file://welcome.yaml \
 --parameters ParameterKey=Environment,ParameterValue=test
```
