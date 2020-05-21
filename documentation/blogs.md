# Blog Articles

## Create a new blog post
1. Create page file:
    ```
    touch /src/views/ArticlePages/ArticleName.js
    ```
1. Add template content, which can be taken from: [Template](#template)
  1. Update blog name with article key
  1. Update product data file path
  1. Add introduction
  1. Add section headings
  1. Add content and product keys
1. Create products file:
    ```
    touch /src/views/ArticlePages/Products/ArticleName.json
    ```
1. Create products with json template:
    ```
    {
      "productId": "12345678-prod-b001-1234-abcdefghijkl",
      "brand": "Product brand",
      "retailer": "amazon",
      "details": "Product description",
      "imageUrl": "//ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=B00JYD5SEM...",
      "productUrl": "https://www.amazon.co.uk/dp/B00JYD5SEM/..."
    }
    ```
1. Add article data to `PageDetails.json`:
    ```
    "article-name-key": {
      "category": "TYPE",
      "title": "Article Page Title",
      "url": "/list-ideas/article-name",
      "img": "article-name-key",
      "description_short": "Roughly 40 characters.",
      "beginning_content": "Roughly 200 characters."
    }
    ```
1. Each article requires a number of image files.
  1. Main image (1000 X 650): `article-name.jpg`
  1. Mobile image (550 X 400): `article-name.mob.jpg`
      ```
      convert article-name.jpg -resize 550x400 article-name.mob.jpg
      ```
  1. Tile image (300 X 225): `article-name.tile.jpg`
      ```
      convert article-name.jpg -resize 300x225 article-name.tile.jpg
      ```
  1. Compressed main image: `article-name.webp`
      ```
      cwebp article-name.jpg -o article-name.webp
      ```
  1. Compressed tile image: `article-name.tile.webp`
      ```
      cwebp article-name.tile.jpg -o article-name.tile.webp
      ```
1. Add file to `Routes.js`.
1. Update `sitemap.xml`.
1. Review spelling and grammar with Grammerly


To deploy blog:
1. Copy images to s3 buckets:
    ```
    aws s3 cp Downloads/images/ s3://test.ewelists.com-images/images/ --recursive
    aws s3 cp Downloads/images/ s3://staging.ewelists.com-images/images/ --recursive
    aws s3 cp Downloads/images/ s3://ewelists.com-images/images/ --recursive
    ```
1. Add product data to products tables
    ```
    cd ewelists.com/scripts/
    python load_blog_data.py products-test ~/Development/ewelists.com-web/src/views/ArticlePages/Products/ArticleName.json
    python load_blog_data.py products-staging ~/Development/ewelists.com-web/src/views/ArticlePages/Products/ArticleName.json
    python load_blog_data.py products-prod ~/Development/ewelists.com-web/src/views/ArticlePages/Products/ArticleName.json
    ```
1. Commit web to master, to deploy web content via pipeline


## Updating blog article content or products
1. Update products in the json file.
1. Update the content in the article page.
1. Load the whole product data to products tables
    ```
    cd ewelists.com/scripts/
    python load_blog_data.py products-test ~/Development/ewelists.com-web/src/views/ArticlePages/Products/BabyEssentials.json
    python load_blog_data.py products-staging ~/Development/ewelists.com-web/src/views/ArticlePages/Products/BabyEssentials.json
    python load_blog_data.py products-prod ~/Development/ewelists.com-web/src/views/ArticlePages/Products/BabyEssentials.json
    ```
1. Deploy web content via pipeline



## Template
```
import React, { useState, useEffect } from 'react';
// custom components
import { getUsersLists } from "custom/Article/GetUsersLists";
import SectionHeading from "custom/Article/SectionHeading.js";
import SectionHeadings from "custom/Article/SectionHeadings.js";
import ListArticle from "custom/Article/ListArticle.js";
import Products from "custom/Article/Products.js";

// Blog Data
const name = 'outdoor-play'
const productData = require('./Products/OutdoorPlay.json');

export default function OutdoorPlay(props) {
  const [lists, setLists] = useState({});

  const content = (
    <div>
      <div>
        <p>
          Introduction content.
        </p>
      </div>
      <SectionHeadings
        headings={[
          {"name": "clothing", "text": "The essential clothing list"},
          {"name": "nursery", "text": "The essential nursery list"},
          {"name": "feeding", "text": "The essential feeding list"},
          {"name": "outandabout", "text": "The essential out and about list"}
        ]}
      />
      <div>
        <SectionHeading name="clothing" text="The essential clothing list" />
        <p>
          First products content.
        </p>
      </div>
      <Products
        products={[
          "12345678-blog-e001-1234-abcdefghijkl"
        ]}
        data={productData}
        lists={lists}
        isAuthenticated={props.isAuthenticated}
      />
    </div>
  );

  useEffect( () => {
    async function getLists(){
      const lists = await getUsersLists();
      setLists(lists);
    }

    if (props.isAuthenticated) {
      getLists();
    }
  }, [props.isAuthenticated]);

  return (
    <ListArticle
      isAuthenticated={props.isAuthenticated}
      user={props.user}
      name={name}
      content={ content }
      setTitle={props.setTitle}
    />
  );
}
```
