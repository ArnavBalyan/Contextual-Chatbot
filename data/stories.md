## Direct Search
* inform{"keyword":"sulphur"}
 - action_database_search
 - slot{"keyword" : "something"}

## Direct Search 2
* search
 - utter_askdata
* inform{"keyword":"machine learning"}
 - action_database_search
 - slot{"fetch_data" : "something"}

## search database happy path
* greet
 - utter_how_can_i_help
* inform{"keyword":"sulphur"}
 - action_database_search
 - slot{"keyword" : "something"}
* thanks
 - utter_goodbye

## describe search path
* greet
 - utter_how_can_i_help
* describe
 - utter_describe
* inform{"keyword":"DESIDOC"}
 - action_database_search
 - slot{"keyword" : "something"}
* thanks
 - utter_goodbye


## search database + entity
* greet
 - utter_how_can_i_help
* search
 - utter_askdata
* inform{"keyword":"machine learning"}
 - action_database_search
 - slot{"fetch_data" : "something"}
* thanks
 - utter_goodbye

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy
  - utter_how_can_i_help

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_sorry
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## poor quality
* poorquality
  - utter_sorry

## Only Greet
* greet
  - utter_greet