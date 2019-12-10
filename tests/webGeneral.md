# Web General Tests
In this section we test the following:
* redirects
* error handling
* S3 bucket restrictions
* status page
* Robots.txt
* sitemap.xml


## Prod Environment Runbook

| Name | Command | Expected Result |
| --- | --- | --- |
| Main domain | curl -sI https://ewelists.com \| head -1 | 200 |
| http redirects | curl -sI http://ewelists.com \| head -1 | 301 Moved Permanently |
| www redirects | curl -sI http://www.ewelists.com \| head -1 <br> curl -sI https://www.ewelists.com \| head -1 | 301 Moved Permanently |
| .co.uk redirects | curl -sI http://ewelists.co.uk \| head -1 <br> curl -sI https://ewelists.co.uk \| head -1 <br> curl -sI http://www.ewelists.co.uk \| head -1 <br> curl -sI https://www.ewelists.co.uk \| head -1 | 301 Moved Permanently |
| S3 Request | curl -sI http://ewelists.com.s3-website-eu-west-1.amazonaws.com | 301 <br> Location: http://ewelists.com/ |
| S3 Request to missing file | curl -sI http://ewelists.com.s3-website-eu-west-1.amazonaws.com/nopage | 301 <br> Location: http://ewelists.com/ |
| Page missing | https://ewelists.com/nopage | 200 (404 shown in browser) |
| Status Page | https://ewelists.com/status.html | 200 |
| Robots | https://ewelists.com/robots.txt | 200 <br> Disallow: / |
| Sitemap | https://ewelists.com/sitemamp.xml | 200 <br> Disallow: / |

## Staging Environments Runbook

| Name | Command | Expected Result |
| --- | --- | --- |
| Main domain | curl -sI https://staging.ewelists.com \| head -1 | 200 |
| http redirect | curl -sI http://staging.ewelists.com \| head -1 | 301 Moved Permanently |
| www redirects | curl -sI http://www.staging.ewelists.com \| head -1 <br> curl -sI https://www.staging.ewelists.com \| head -1 | 301 Moved Permanently |
| .co.uk redirects | curl -sI http://staging.ewelists.co.uk \| head -1 <br> curl -sI https://staging.ewelists.co.uk \| head -1 <br> curl -sI http://www.staging.ewelists.co.uk \| head -1 <br> curl -sI https://www.staging.ewelists.co.uk \| head -1 | 301 Moved Permanently |
| S3 Request | curl -sI http://staging.ewelists.com.s3-website-eu-west-1.amazonaws.com | 301 <br> Location: http://staging.ewelists.com/ |
| S3 Request to missing file | curl -sI http://staging.ewelists.com.s3-website-eu-west-1.amazonaws.com/nopage | 301 <br> Location: http://staging.ewelists.com/ |
| Page missing | https://staging.ewelists.com/nopage | 200 (404 shown in browser) |
| Status Page | https://staging.ewelists.com/status.html | 200 |
| Robots | https://staging.ewelists.com/robots.txt | 200 <br> Disallow: / |
| Sitemap | https://staging.ewelists.com/sitemamp.xml | 200 <br> Disallow: / |
