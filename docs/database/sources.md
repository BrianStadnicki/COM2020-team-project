# The generation of synthetic seeded data

There was no publicly available data in regards to sellers, bundles, reservations and issue reports, so the seeded data will have to be generated around related data. This will be synthetic data which will try to recreate the realism from real-world scenarios.

## Seller Profiles

Generated seller profiles will be based on sellers that have signed up for the TooGoodToGo food marketplace. To find a list of TooGoodToGo merchants, a website called 'MagicBagTracker' has a list of merchants in major cities across the United States, the United Kingdom and Canada [1]. From this, we can see the following seller types that appear:

- Cafes
- Restaurants
- Grocery stores
- Supermarkets
- Bakeries
- Convenience stores

Using the TooGoodToGo app [2] also reveals more seller types:

- Hotels
- Florists
- Pet shops

As TooGoodToGo does not publish their collected data on users and sellers, because of their privacy policy and terms of service, these are the types that will be included and considered mainstream for this synthetic data.

An important attribute for seller profiles is the opening times. It will be assumed that every seller will have different opening times for weekdays and weekends as the majority of sellers implement this. The opening times will be generated based on the seller type, using a range of opening times from major businesses that operate in that category. For cafe opening times, it can be based on university cafes as they provide a list of opening times for their cafes. [3]

## Product Categories

From the TooGoodToGo app [2], some product categories are provided:

- Meals
- Bread & pastries
- Groceries
- Flowers & plants
- Pet food
- Collect now
- Collect today
- Collect tomorrow
- Vegetarian
- Vegan

It can be concluded that products can share multiple categories, which will also be implemented. These categories will be the ones used in the synthetic data.

## Pickup-time Windows

From the TooGoodToGo app [2], it can be inferred that the pickup-times are dependent on:

- the time of day (morning/afternoon/evening/night)
- the seller

A dataset of pickup-time windows is not published as it is data exclusive to the seller. So, the following assumptions are made:

- The majority of the pickup-time windows will be between one hour to three hours, sometimes even four hours for some cases.
- Some lengths will be shorter than others (up to one hour), due to constraints such as closing times. This usually happens with food that is about to expire, as companies usually have a policy to retain only fresh food.
- The majority, if not all of the pickup-time windows will be right before the closing time, e.g. one or two hours before closing time.

With these assumptions, the pickup-time windows will be set before the closing times of the seller and be randomly given a pickup-time window range.

## Bundle Postings

From the WRAP Food Waste & Food Surplus 2025 report [4], it states that the food waste for supply chains and retail are reduced per year. The TooGoodToGo Impact 2024 report [5] states that the meals saved globally increases per year. However, this does not eliminate the issue of food waste. Therefore the following assumptions are made:

- Sellers may not post bundles everyday
- The frequency of postings vary per seller
- Some days may have less frequency of postings due to problems such as weather conditions (e.g. snow)

The weather conditions can be generated based on the MET Office weather reports [6]. There were no datasets published for bundle postings, so for the synthetic data, bundles will be posted the day before or on the same day, which is how TooGoodToGo operates [2]. The attributes of the bundle posting will be randomised to an extent but kept relevant to the corresponding seller and the category it is under. For the pickup-time windows, it will be based on the generated windows for each seller. Each bundle posting will have a random number of bundles attached to it.

## Reservations

There are no published datasets for reservations, so it the following will be assumed:

- Weather conditions may affect reservations that result in a no-show or expiration.
- The shorter the pickup-time window, there will be a higher probability that it will result in a no-show.
- The longer the pickup-time window, there will be a lower probability that it will result in a no-show.

 A reservation will be linked to a bundle posting, with one of the bundles chosen. There will be percentages for collected, no-shows and expirations, so that it fits the target requirement of at least 400 reservations, 80 no-shows and 50 expirations. Variance may be added depending on the seller, time, or if its the weekend.

## Issue Reports

Issue reports will be randomly generated, with reservations that result in a no-show or expiration leading to a higher probability of returning an issue report. There is no other data that can really help with this part of the synthesised data.


# References

[1] TooGoodToGo Merchants List from MagicBagTracker <https://www.magicbagtracker.com/en/store-list>

[2] TooGoodToGo App. <https://www.toogoodtogo.com/>

[3] University cafe opening times reference:

- Exeter: <https://www.exeter.ac.uk/departments/campusservices/eatandshop/openingtimes/openinghours/>

- Southampton: <https://catering.southampton.ac.uk/catering-services>

- Oxford: <https://estates.admin.ox.ac.uk/cafe-services#collapse1204651>

- Cambridge: <https://www.catering.admin.cam.ac.uk/food-and-drink/cafes>

[4] <https://www.wrap.ngo/resources/report/uk-food-waste-food-surplus-key-facts#download-file>

[5] WRAP Food Waste & Food Surplus Report: <https://www.toogoodtogo.com/resources>

[6] Weather Reports from Met Office: <https://www.metoffice.gov.uk/research/climate/maps-and-data/data/index>


# Unused Sources:

## Statistics from Fareshare

<https://fareshare.org.uk/wp-content/uploads/2024/07/Context-Facts-and-Statistics-2024-07.pdf>

## Industry Report from The Food Foundation

<https://foodfoundation.org.uk/publication/state-nations-food-industry-report-2025>

## Food Waste Index Report from UNEP

<https://wedocs.unep.org/items/dbe2cd4c-8384-4636-8359-5847f42b9711>
