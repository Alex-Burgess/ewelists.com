# Testing - Authentication

## Test Account (With google, amazon and facebook accounts.)
Name: Tim BL
Email: timb33045@gmail.com

## Preparation
1. Delete user account from lists-staging table.
1. Delete user account from cognito.

## Signup Tests
| Page | Test Details | Notes |
| --- | --- | --- |
| Sign up | Terms Link | Opens in new tab. |
| Sign up | Privacy Policy Link | Opens in new tab. |
| | **Username and Password** | |
| Sign up | Sign up button disabled, until name, Username and Password entered. |  |
| Sign up | Password validation 1 | Message: *Password does not contain any lower case letters.* |
| Sign up | Password validation 2 | Message: *Password does not contain any upper case letters.* |
| Sign up | Password validation 3 | Message: *Password does not contain any numbers.* |
| Sign up | Password validation 4 | Message: *Password does not contain any symbols.* |
| Confirmation page | Bad confirmation code. | Message: *Invalid verification code provided, please try again.* |
| Confirmation page | Confirmation code page. | Completes sign up, redirected to dashboard |
| Sign up | Re enter email | Message: *An account with the given email already exists.* |
| | **Amazon** | |
| Sign up | Click amazon icon | |
| Amazon login | Complete signin | "Ewelists would like to access to: Profile" message show.<br> Link to privacy policy on Allow decision page. |
| Sign up | Login complete and redirected to dashboard | |
| | **Google** | |
| Sign up | Click google icon |
| Sign up | Complete signin | Login page should have logo as well as working link to privacy policy and terms of service. |
| Sign up | Login complete and redirected to dashboard. | |
| | **Facebook** | |
| Sign up | Click facebook icon. | |
| Sign up | Complete signin | After login see "Ewelists will receive..." message.<br> After "Continue as ..." |
| Sign up | Login complete and redirected to dashboard | |

## Login Tests
| Page | Test Details | Notes |
| --- | --- | --- |
| | **Username and Password** | |
| Login | Enter name, Username and Password | Login and redirected to dashboard |
| Login | Bad user | Message: *User does not exist.* |
| Login | Bad password | Message: *Incorrect username or password.* |
| Login | Forgot password | Links to reset password |
| Reset | Wrong code | Message: *Invalid verification code provided, please try again.* |
| Reset | Invalid password | Message: *Password does not conform to policy: Password must have lowercase characters.* |
| Reset | Correct code and valid, matching passwords | Reset complete. |
| | **Amazon** | |
| Sign up | Click amazon icon | |
| Amazon login | Complete signin | "Ewelists would like to access to: Profile" message show.<br> Link to privacy policy on Allow decision page. |
| Sign up | Login complete and redirected to dashboard | |
| | **Google** | |
| Sign up | Click google icon |
| Sign up | Complete signin | Login page should have logo as well as working link to privacy policy and terms of service. |
| Sign up | Login complete and redirected to dashboard. | |
| | **Facebook** | |
| Sign up | Click facebook icon. | |
| Sign up | Complete signin | After login see "Ewelists will receive..." message.<br> After "Continue as ..." |
| Sign up | Login complete and redirected to dashboard | |
