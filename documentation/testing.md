# Testing

## Initial Web Setup Tests

| Name | Command | Expected Result |
| --- | --- | --- |
| Main domain success | curl -sI https://test.ewelists.com | 200 |
| http to https redirect | curl -sI http://test.ewelists.com | 301 Moved Permanently |
| www to root redirects | curl -sI http://www.test.ewelists.com <br> curl -sI https://www.test.ewelists.com | 301 Moved Permanently |
| .co.uk redirects | curl -sI http://test.ewelists.co.uk <br> curl -sI https://test.ewelists.co.uk <br> curl -sI http://www.test.ewelists.co.uk <br> curl -sI https://www.test.ewelists.co.uk | 301 Moved Permanently |
| Page missing | https://test.ewelists.com/nopage | 200 (404 shown in browser) |
| S3 Request | curl -sI http://test.ewelists.com.s3-website-eu-west-1.amazonaws.com | 301 <br> Location: http://test.ewelists.com/ |
| S3 Request to missing file | curl -sI http://test.ewelists.com.s3-website-eu-west-1.amazonaws.com/nopage | 301 <br> Location: http://test.ewelists.com/ |
| Status Page | curl -sI https://test.ewelists.com/status.html | 200 |

## Robots Files
| Name | Command | Expected Result |
| --- | --- | --- |
| Test File | curl -sI https://test.ewelists.com/robots.txt | 200 <br> Disallow: / |
| Staging File | curl -sI https://staging.ewelists.com/robots.txt | 200 <br> Disallow: / |
| Prod File | curl -sI https://ewelists.com/robots.txt | 200 <br> Disallow: |

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

## Display on Device Checklist

Browsers (versions?):
* Chrome
* Safari
* Firefox
* IE

Devices (Portrait and Landscape):
* iPad Pro 12"
* iPad Pro 10"
* iPad
* iPhone 10
* iPhone Plus sizes
* iPhone 5/6/7/8

| Page | Checked |
| --- | --- |
| Landing Page | &#9744; |
| Login | &#9744; |
| Sign Up | Main: &#9744; <br> Validation: &#9744; <br> Confirmation: &#9744; |
| Reset Password | Main: &#9744; <br> Validation: &#9744; <br> Success: &#9744;  |
| Contact Us | &#9744; |
| Error | &#9744; |
| Terms | &#9744; |
| Privacy | &#9744; |
| Gift List Ideas | &#9744; |
| Gift List Article | &#9744; |
| Add more....  | &#9744; |
