# Device Testing

A full suite of tests per device is deemed excessive at this stage. The current focus for testing the application on different devices is to:
* Check pages render correctly
* Check main flows work correctly.

## UnAuthed Page Checklist

| Section | Page | Notes |
| --- | --- | --- |
| Main | Landing Page | Tablet and phone devices should have menu button. <br /> Larger devices should see individual menu items. |
| Main | Error Page | |
| Footer | Contact Us | iPad - Main content is too low. |
| Footer | About Us | Just links to About Us section on landing page. |
| Footer | Privacy | |
| Footer | Terms | |
| Footer | Facebook | Opens in new tab. |
| Footer | Twitter | Opens in new tab. |
| Footer | Instagram | Opens in new tab. |
| Auth | Login | |
| Auth | Login - reset password | |
| Auth | Signup | |
| Auth | Signup - confirmation code | |
| Blog | Gift List Ideas | |
| Blog | Travel Gear | |
| Blog | The Nursery List | |
| Blog | Bath Time | |
| Blog | Hospital Bag | |

## Main Flows

In production, test user 3 can be timb33045@gmail.com.

| User | Action | Notes |
| --- | --- | --- |
| test3 | On iPad, Sign up with own social accounts | google, amazon, facebook. FIRST LOGIN ATTEMPTS NOT WORKING (?) |
| | **SWITCH USER** | |
| test1 | Sign Up with username password | Use normal chrome browser, with device size.  |
| test1 | Create new list | |
| test1 | Edit details | Add a data, update the description and occasion |
| test1 | Add product 1, that exists in products table, with quantity 2 | Check quantity buttons |
| test1 | Add product 2, that doesn't exist in products table, with quantity 1 | Check quantity buttons |
| test1 | Add product 3, that doesn't exist, with quantity 4 | |
| test1 | Share list with user 2 - test2 | |
| test1 | Share list with user 3 - burgess.alexander@gmail.com | |
| | **SWITCH USER** | |
| test2 | On iphone, access link from email | |
| test2 | Sign Up with username and password | Should finish on list page |
| test2 | Reserve 1 of product 1 | Check quantities buttons |
| test2 | Reserve 2 of product 3 | |
| test2 | Unreserve product 1 | |
| test2 | Reserve product 2 | |
| | **SWITCH USER** | |
| test3 | On ipad, access link from email | |
| test3 | Login with social accounts | GET LANDING PAGE NOT VIEW LIST |
| test3 | Browser to view list | |
| test3 | Test product filters | |
| test3 | Reserve 1 of product 1 | |
| test3 | Reserve 2 of product 3 | |
| test3 | Update product 3 to quantity of 1 | |
| test3 | Create list | |
| test3 | Add an item with quantity of 1 | |
| test3 | Share list with user 1 | |
| | **SWITCH USER** | |
| test1 | Browse to landing page | Should see 2 lists |
| test1 | Browse to owner list | |
| test1 | View reserved details | Should see 4 reserved rows in table |
| test1 | Edit quantity of product 1 to 1 | LIMITS? |
| test1 | Edit quantity of product 3 to 3 | LIMITS? |
| test1 | Browse to shared list | |
| test1 | Reserve product 1 | |
| | **CLEAN UP** | |
| Note list Ids |||
| test1 | Delete list | |
| test3 | Delete list | |
| | Clean up User Ids from table and user pool | burgess.alexander+test1@gmail.com, burgess.alexander+test2@gmail.com, timb33045@gmail.com |
| | Double check lists and notfound tables ||


## Devices currently missing:
1. Andriod Phone
1. Older iphones


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
