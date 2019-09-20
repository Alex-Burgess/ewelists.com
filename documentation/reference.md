# Reference
### AWS Cli Authentication
To generate a session for the required AWS profile:
```
. aws-auth --profile_name ListsMain --token_code 123456 [--duration 18000]
```

### Github Administration
The master branch will be the latest working code. To clone the project:
```
git clone git@github.com:Alex-Burgess/ewelists.com.git
```

Versioning is used to track changes to config, code and procedures. To create a version tag:
```
git tag -a v0.0.1 -m "Tag description..."
git push origin v0.0.1
```

### CloudFront Cache Invalidations
Cloudfronts default cache is set to 1 day.  if you have updated content you need to “invalidate the objects” that are currently being server by the cache.  To do this for a file, specific /index.html, or for the whole site, /*

```
aws cloudfront list-distributions --query 'DistributionList.Items[*].{ID:Id, DomainName:Origins.Items[*].DomainName}'
aws cloudfront create-invalidation --distribution-id ABCDEFGHIJK12 --paths '/*'
aws cloudfront wait invalidation-completed --distribution-id ABCDEFGHIJK12 --id ABCDEFG1234567
```

Or with file:
```
aws cloudfront create-invalidation --distribution-id EPHRMSYQN7X62 --invalidation-batch file://all.html
```

Check status of invalidation:
```
aws cloudfront get-invalidation --distribution-id ABCDEFGHIJK12 --id ABCDEFG1234567 --query 'Invalidation.Status'
```

### React
```
REACT_APP_STAGE=test npm start
REACT_APP_STAGE=test npm run build
aws s3 sync build/ s3://test.ewelists.com --delete
aws cloudfront list-distributions --query "DistributionList.Items[?AliasICPRecordals[?CNAME=='test.ewelists.com']].{ID:Id}" --output text
aws cloudfront create-invalidation --paths '/*' --distribution-id ABCDEFGHIJK12
aws cloudfront wait invalidation-completed --distribution-id ABCDEFGHIJK12 --id IJKLMNOPQRSTUV
```
