## Preprocessing ##

* Convert `review.json` to csv

* Randomly sample a number of reviews for studying the dialects
    - sample a number of rows inputing the total row size
    - for each sample, write `review_id`, `business_id`, `text` into a new csv file

* Data Cleaning
    - Remove punctuations from `review_text`
    - lowercase all text

* Match review text with location
    - for each piece of review text in `yelp_review_cleaned.csv`, we extract `business_id`
    to match it with `city` and `state` from the business data
    - costruct a new csv file with columns `business_id`, `text`, `city`, `state`
    - group cities/states into more general regions (e.g. Southwest, Northeast)
    - Add a new column to our csv file: `region`

## Counting Frequencies ##


