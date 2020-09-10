import csv
import boto3

table_name = 'products-test'


def convert_csv_to_json_list(file):
    items = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {}
            data['productId'] = row['productId']
            data['retailer'] = row['retailer']

            items.append(data)
    return items


def batch_write(items):
    dynamodb = boto3.resource('dynamodb')
    db = dynamodb.Table('table-name')

    with db.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)


def update_table(items):
    dynamodb = boto3.client('dynamodb')

    for item in items:
        print("Updating " + item['productId'] + " with " + item['retailer'])
        dynamodb.update_item(
            TableName=table_name,
            Key={'productId': {'S': item['productId']}},
            UpdateExpression="set retailer = :r",
            ExpressionAttributeValues={
             ':r': {'S': item["retailer"]}
            },
        )


if __name__ == '__main__':
    json_data = convert_csv_to_json_list('products-prod-import.csv')
    update_table(json_data)
