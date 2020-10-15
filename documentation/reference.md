# Reference
## AWS Cli Authentication
To generate a session for the required AWS profile:
```
. aws-auth --profile_name ListsDev --token_code 123456 [--duration 18000]
```

## Github Administration
The master branch will be the latest working code. To clone the project:
```
git clone git@github.com:Ewelists/ewelists.com.git
```

Versioning is used to track changes to config, code and procedures. To create a version tag:
```
git tag -a v0.0.1 -m "Tag description..."
git push origin v0.0.1
```

## CloudFront Cache Invalidations
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

## React
```
REACT_APP_STAGE=test npm start
REACT_APP_STAGE=test npm run build
aws s3 sync build/ s3://test.ewelists.com --delete
aws cloudfront list-distributions --query "DistributionList.Items[?AliasICPRecordals[?CNAME=='test.ewelists.com']].{ID:Id}" --output text
aws cloudfront create-invalidation --paths '/*' --distribution-id ABCDEFGHIJK12
aws cloudfront wait invalidation-completed --distribution-id ABCDEFGHIJK12 --id IJKLMNOPQRSTUV
```

## Postman
The [Postman API documentation](https://docs.api.getpostman.com/?version=latest) has useful information on finding the collection and environment Ids.

Set a local environment variable for the Postman API key:
```
export POSTMAN=??????
```

To find your collection uid:
```
curl https://api.getpostman.com/collections?apikey=$POSTMAN
```

To find your environment uid:
```
curl https://api.getpostman.com/environments?apikey=$POSTMAN
```

Install Newman:
```
npm i newman -g;
```

Test a collection:
```
newman run https://api.getpostman.com/collections/<Collection UID>?apikey=$POSTMAN --environment https://api.getpostman.com/environments/<Environment UID>?apikey=$POSTMAN
```

## Cognito Useful Commands
```
aws cognito-idp admin-disable-provider-for-user --user-pool-id eu-west-1_vqox12345--user ProviderName=Google,ProviderAttributeName=Cognito_Subject,ProviderAttributeValue=109769169322789408080

aws cognito-idp admin-link-provider-for-user --user-pool-id eu-west-1_vqox12345 --destination-user ProviderName=Cognito,ProviderAttributeName=Username,ProviderAttributeValue=e371f5fc-14ef-404f-bca8-ab9a55cbee6e --source-user ProviderName=Google,ProviderAttributeName=Cognito_Subject,ProviderAttributeValue=109769169322789408080

aws cognito-idp list-users --user-pool-id eu-west-1_vqox12345
```

## How to Handle Not Found Product
1. Locate the item in the NotFound table and record the productId, e.g. `0e0c8f35-0e8b-44cf-8440-16e46ce21bce`
1. Open the Tools collection in Postman.
1. Create a POST API request to the `/tools/products/{id}` API method.  The body should contain the brand, details, retailer and imageUrl:
    ```
    {
        "brand": "Ravensburger",
        "details": "Disney Pixar Toy Story 4, 4 in a Box (12, 16, 20, 24pc) Jigsaw Puzzles",
        "retailer": "Amazon",
        "imageUrl": "//ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B07MG8FRR2&Format=_SL250_&ID=AsinImage&MarketPlace=GB&ServiceVersion=20070822&WS=1&tag=ewelists-21&language=en_GB"
    }
    ```
1. After sending the POST API request the following happens:
  1. A new item is created for the product in Products table.
  1. The list is updated with new product and reservation items in the Lists table.
  1. The old notfound product and reservation items are deleted from the lists table.
  1. The old notfound product item is deleted from the notfound table.
1. If the product is an Amazon gift, need to update the product Url in the products table.

## Export prod data for testing in test or staging

The tools for this procedure are in the [scripts](/scripts) directory.

1. Query for data with list id: e.g. 5282f07f-7c09-485d-a580-95d4e049b69b
    ```
    python get_data.py -e prod -l 5282f07f-7c09-485d-a580-95d4e049b69b alex-prod-list
    ```
1. Check the files created in the Downloads directory:
    ```
    alex-prod-list_lists.json   alex-prod-list_notfound.json   alex-prod-list_products.json
    ```
1. Updates
  1. Change list ID to something recognisable - Replace all 5282f07f-7c09-485d-a580-95d4e049b69b with 12345678-test-alex-1234-abcdefghijkl
  1. Change list owner / user id to id for environment - Replace all ea9fca5e-fec7-4984-bf17-6030e6ebf5c1 with 6c9b0a41-9a92-490c-98f8-c51f280c557f
  1. Update images if test (e.g. https://test.ewelists.com/images/birthday-default.jpg)
1. Upload data (uses a prefix to load all necessary data.)
    ```
    python load_data.py -e test alex-prod-list
    ```
1. Data updates as part of upgrade to data model 2
  1. Add state to main list item.  State: closed.
  1. Add closed image url.
  1. Add purchased to product items.
  1. Delete shared items
  1. Change reserved to reservation
      1. Create reservation item
      1. Delete reserved item
1. Test final pages
  1. landing page
  1. Edit list page
  1. view list page

## How to produce browser/device screen shots.
https://smartmockups.com
https://www.screely.com
