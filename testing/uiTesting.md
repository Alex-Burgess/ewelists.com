# UI & E2E Testing


## Setup

Install (one time activity)
```
npm install cypress --save-dev
```

Open cypress, with npm script definition:
```
npm run cypress
```

## Automate Congito User Login
The [best practices](https://docs.cypress.io/guides/references/best-practices.html#Selecting-Elements) suggest not to use the UI to login before each test and instead to programmatically log in.  This will be more efficient.

By default it is not possible to import the Amplify libraries to Cypress.  To get this to work we need to use the [Cypress Webpack Preprocessor](https://github.com/cypress-io/cypress-webpack-preprocessor) to transpile the code, so that it will run inside the browser.

* Install cypress webpack preprocessor:
```
npm install --save-dev @cypress/webpack-preprocessor
```
* Update `plugins/index.js` to require the preprocessor
```
const webpackPreprocessor = require('@cypress/webpack-preprocessor')

/**
 * @type {Cypress.PluginConfig}
 */
module.exports = (on, config) => {
  // `on` is used to hook into various events Cypress emits
  // `config` is the resolved Cypress config

  on('file:preprocessor', webpackPreprocessor())
}
```

After this we can then use the amplify library to authenticate a user, rather than using the UI.  We still perform one E2E ui test to ensure the login page is working correctly.

## Run cypress tests from CLI
Run All tests:
```
npx cypress run
```

Run a specific test:
```
npx cypress run --spec "cypress/integration/about.spec.js"
```

All snapshots should be generated in headless mode (i.e. linux).
```
CYPRESS_updateSnapshots=true npx cypress run --headless --browser chrome
```

Or just for s specific page:
```
CYPRESS_updateSnapshots=true npx cypress run --spec "cypress/integration/non-auth-pages.spec.js" --headless --browser chrome
```

## Testing flows which include email in the process

Main ideas:
1. (Mail Slurp)[https://www.mailslurp.com/examples/cypress-js/] - Didn't like that free tier limitations as felt would potentially go over those.
2. (MailHog)[https://humble.dev/testing-an-email-workflow-from-end-to-end-with-cypress] - You run your own email server on Docker.  Didn't like the extra effort this would require to integrate into the CI/CD pipeline.
3. (gmail-tester)[https://medium.com/@levz0r/how-to-poll-a-gmail-inbox-in-cypress-io-a4286cfdb888] - Requires a bit of setup, but is free forever, leverages gmail for test accounts and would extend to CI/CD pipeline easily.


Went with _gmail-tester_, which is working well. Setup:
```
node node_modules/gmail-tester/init.js ~/.google-accounts/credentials-ui-test.json ~/.google-accounts/token-ui-test.json eweuser8@gmail.com
```

Credential and token files are required for gmail tasks, which are configured in the `plugins/index.js`.



## Scripts for creating and deleting users in cognito and data in tables
Note: May need to update organisation scp to allow iam users to be created first.
```
aws organizations list-policies --filter SERVICE_CONTROL_POLICY
aws organizations update-policy --policy-id p-12345678 --content file://lists-ou-scp.json
```

Create IAM user with programmatic access.  (This was done manually, need a more automated way for staging / prod.)
*Permissions:* Need to ensure more restricted permissions on iam user.

Add keys to local profile.  Edit `.aws/config` and `.aws/credentials`.

Update profile in python script.
```
session = boto3.session.Session(profile_name='cypress-test')
cognito = session.client('cognito-idp')
dynamodb = session.client('dynamodb')
```
