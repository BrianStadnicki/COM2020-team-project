# Before

 - Start server

```sh
source .env/bin/activate
SECRET_KEY="SDART4TRGERT6454ETFEWRTETR" python manage.py runserver
```

 - open firefox seller container and load login page
 - open firefox consumer container and load login page

# After

 - Open firefox seller container
 - Login as seller demo_seller:demo_seller

 - Open firefox consumer container
 - Login as consumer demo:demo


 - Switch to seller window
 - Click create bundle
 - Fill out details
 -
 -  Name: Dog ice cream
 -  Category: Pet Food
 -  Allergens: Peanut
 -  Price: £2.00
 -  Quantity: 3
 -  Pickup window: 17:00 - 18:00
 -  Description: Going out of date today! Only for dogs!
 -   
 - Confirm 
 - Show forecast
 - Create
 - Show bundle posting

 - Switch to consumer window
 - Reload bundle postings page
 - View created bundle posting
 - Reserve bundle
 - Show claim code
 - Show streak not updated

 - Switch to seller window
 - Reload bundle postings page
 - Show claim code is the same
 - Mark as collected
 - Show status change

 - Switch to consumer window
 - Reload page by pressing enter to avoid resending data
 - Show reservation status change
 - Show streak changed

 - Switch to seller window
 - Go to analytics page
 - Show analytics data
 - Show baseline forecast evaluation (explain based off of 3-6 weeks before and eval prev 3 weeks)
