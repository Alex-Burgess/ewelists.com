import csv
import boto3

table_name = 'products-test'


def convert_csv_to_json_list(file):
    items = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {
                'productId': {'S': row['productId']},
                'retailer': {'S': row['retailer']},
                'brand': {'S': row['brand']},
                'details': {'S': row['details']},
                'productUrl': {'S': row['productUrl']},
                'imageUrl': {'S': row['imageUrl']}
            }

            if 'price' in row:
                if len(row['price']) > 0:
                    data['price'] = {'S': row['price']}

            if 'priceCheckedDate' in row:
                if len(row['priceCheckedDate']) > 0:
                    data['priceCheckedDate'] = {'S': row['priceCheckedDate']}

            if 'createdAt' in row:
                if len(row['createdAt']) > 0:
                    data['createdAt'] = {'N': row['createdAt']}

            # print("Item: " + str(data))

            items.append(data)
    return items


def batch_write(items):
    dynamodb = boto3.resource('dynamodb')
    db = dynamodb.Table(table_name)

    with db.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)


def update_table(items):
    dynamodb = boto3.client('dynamodb')

    for item in items:
        dynamodb.put_item(TableName=table_name, Item=item)


if __name__ == '__main__':
    json_data = convert_csv_to_json_list('products-staging.csv')
    update_table(json_data)
    # batch_write(json_data)
