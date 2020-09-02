# Blog Articles

## Create Blog Content

When creating a new blog post we would like it to be submitted in the template below, which will be a stepping stone
towards using a markup blog system.

Checklist:
1. Add content to template and review spelling and grammar with Grammerly
1. Provide image link
1. Create products and update ids in template (https://tools.ewelists.com)

To create an amazon product:
1. Find product
1. Clean up url parameters (i.e. everything including and after ?)
1. Get short text link
1. Get image (large) code and paste into tool.
1. Get Id and copy into template.

### Blog Submission Template
Blog posts will be supplied with the following template:

**Title:** New Baby Feeding
**Short Description:** Our tips to help you prepare and make feeding time easy
**Image link:** (On Shutterstock, or attach to email if not)

**Introduction:**
The first few months after your baby has arrived….

**Section Headings:**
Skip to section:
- Section Heading

**Section Heading:** Feeding in general

**Paragraph:**
There are different options when it comes to feeding…

**Products:** (List of IDs)
- fcc128c3-5e79-4671-9be2-923864b57e39

## Deploy blog post
1. Create page file:
    ```
    touch /src/views/ArticlePages/ArticleName.js
    ```
1. Add file to `Routes.js`.
1. Update `sitemap.xml`.
1. Add template content, which can be taken from: [Template](#template)
  1. Update blog name with article key
  1. Add introduction
  1. Add section headings
  1. Add content and product keys
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
1. Copy images to s3 buckets:
    ```
    aws s3 cp Downloads/images/ s3://test.ewelists.com-images/images/ --recursive
    aws s3 cp Downloads/images/ s3://staging.ewelists.com-images/images/ --recursive
    aws s3 cp Downloads/images/ s3://ewelists.com-images/images/ --recursive
    ```
1. Commit web to master, to deploy web content via pipeline


## Updating blog article content or products
1. Update the content in the article page.
1. Update any product Ids.
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
