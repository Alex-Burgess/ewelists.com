# Blog Articles
## Create a new blog post
1. Create page using template in views/ArticlePages
1. Review spelling and grammar with Grammerly
1. Create json file of product data in views/ArticlePages/Products/
1. Update Gift ideas main
1. Update main landing page
1. Update sitemap.xml
1. Add product data to products tables
    ```
    cd ewelists.com/scripts/
    python load_blog_data.py products-test ~/Development/ewelists.com-web/src/views/ArticlePages/Products/BabyEssentials.json
    python load_blog_data.py products-staging ~/Development/ewelists.com-web/src/views/ArticlePages/Products/BabyEssentials.json
    python load_blog_data.py products-prod ~/Development/ewelists.com-web/src/views/ArticlePages/Products/BabyEssentials.json
    ```
1. Deploy web content via pipeline


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
