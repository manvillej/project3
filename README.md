# Project 3

Web Programming with Python and JavaScript

## Project description
This project is built entirely around the orders app. It borrows some of the content from the original site on the main home page.
There are several different url paths, URLs were tested against the staff, anonynomous, and non staff users both by navigating from the form and accessing with just the URL.

I heavily used the django documentation, Stackoverflow, and this set of tutorials for this project: https://www.youtube.com/watch?v=b8RpVs7bSgo

### Models
There are several Models. The basic DB architecture started off with the ItemType which included Pizza, Sicilian Pizza, Subs, Pasta, Salds, and Dinner Platters
Items are individual food choices in the respective Item Type.
Sizes are sizes that the choices are available in.
Toppings are individual options the choices are available in. These are associated with the item, but I think a future enhancement would be to have a true many to many relationship between item and toppings
Toppings and Sizes both have actual Price values. Other models use the @property to generate prices. This is extremely helpful when calculating total cost as I didn't require a large formula, but rather a
a few smaller calculations that could be called at any level

on top of the basic architecture are three other models
Cart - a model that contains all the relationships of the ordered items, the customer, and the cart's state
OrderedItem - a model that associates the Item, size, and ordered toppings with that item
OrderedToppings - a bridge table between OrderedItem and Toppings. I manually created it to add the price funcition property.

### Forms
There are seven forms. The UserForm is for user registration, each of the 5 food forms is for a different number of topping options
The Checkout form is a placeholder form for the submission and completion of carts. It doesn't do anything, but I wanted the option to add fields incase I implemented creditcard processing

### Templates
Similar to my flask projects, I broke the templates into top level html and a components directory with lower level templates

### Templates
Similar to my flask projects, I broke the templates into top level html and a components directory with lower level templates

### Views
Views is a fairly complicated file. There are two different ways I used for Views. I used the Class style for forms and the function style for get only pages.
Its worth noting that the BasicFoodFormView dynamically switches between forms based on the Item's number of toppings. This allowed me to have the same URL, but different form fields.

## Other

I also had to modify the settings.py file to add the modifications to the user login/logout redirect properties.

I had planned on doing a lot more documentation based on Realpython's recent post: https://realpython.com/documenting-python-code/
I didn't get to it unfortunately.


## SuperUser credentials
username = tesstAdmin
password = tester1234