# Testing - Authentication

## Signup And Login Flows
| File | Test Details | Expected Result |
| --- | --- | --- |
| Sign up - links | Click on Terms and Conditions Link | Terms and Conditions page shown in new tab. |
| Sign up - links | Click on Privacy Policy Link | Privacy Policy page shown in new tab. |
| Sign up | Enter name, Username and Password | Confirmation code page shown.<br> Email with code sent. |
| Sign up - confirmation page | Enter confirmation code | Sign up complete, redirected to dashboard |
| Sign up - amazon | Click amazon icon.<br> Get login to amazon page.<br> Enter password and complete process. | "Ewelists would like to access to: Profile" message show.<br> Link to privacy policy on Allow decision page.<br>Login complete and redirected to dashboard. |
| Sign up - google | Click google icon.<br> Get login to google page.<br> Enter password and complete process. | Login page should have logo as well as working link to privacy policy and terms of service.<br>Login complete and redirected to dashboard. |
| Sign up - facebook | Click facebook icon.<br> Get login to facebook page.<br> Enter password and complete process. | After login see "Ewelists will receive..." message.<br> After "Continue as ..." login completed and redirected to dashboard page. |
| Login - links | Click on Terms and Conditions Link | Terms and Conditions page shown in new tab. |
| Login - links | Click on Privacy Policy Link | Privacy Policy page shown in new tab. |
| Login | Enter name, Username and Password | Login and redirected to dashboard |
| Login - amazon | Click amazon icon.<br> Get login to amazon page.<br> Enter password and complete process. | "Ewelists would like to access to: Profile" message show.<br> Link to privacy policy on Allow decision page.<br>Login complete and redirected to dashboard. |
| Login - google | Click google icon.<br> Get login to google page.<br> Enter password and complete process. | Login page should have logo as well as working link to privacy policy and terms of service.<br>Login complete and redirected to dashboard. |
| Login - facebook | Click facebook icon.<br> Get login to facebook page.<br> Enter password and complete process. | After login see "Ewelists will receive..." message.<br> After "Continue as ..." login completed and redirected to dashboard page. |
| Sign out - amazon | Click sign out link | Get redirected to login page |
| Sign out - google | Click sign out link | Get redirected to login page |
| Sign out - facebook | Click sign out link | Get redirected to login page |


Sign up Form Validation:

| File | Test Details | Expected Result |
| --- | --- | --- |
| Sign up - Validation | No name, or valid email or password > 5 | Form cannot be submitted |
| Sign up - Validation | Email already exists | An account with the given email already exists. |
| Sign up - Validation | Bad password | Password did not conform with policy: Password not long enough |
| Confirmation page - Validation | Bad confirmation code | Invalid verification code provided, please try again. |

Login Page Form Validation:

| File | Test Details | Expected Result |
| --- | --- | --- |
| Login - Validation | No valid email or password > 5 | Form cannot be submitted |
| Login - Validation | Incorrect email | User does not exist |
| Login - Validation | Incorrect password | Incorrect username or password. |

Reset Page Form Validation:

| File | Test Details | Expected Result |
| --- | --- | --- |
| Request - Validation | No valid email | Form cannot be submitted |
| Request - Validation | Email does not exist | User does not exist |
| Reset  - Validation | No confirmation code, no password, no confirmation password and password and confirmation password don't match | Form cannot be submitted |
| Reset - Validation | Bad confirmation code, or bad password syntax | Appropriate Error message |
| Success - Complete | Success | Success message with link to log in. |
