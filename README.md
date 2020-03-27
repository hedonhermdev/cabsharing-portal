# Cab Sharing Portal
 
 A portal that makes efficient groups of people trying to share cabs from frequent locations around the BITS Pilani campus (Delhi, Pilani, Loharu, Jaipur).
 

## Explanation of Models
A user must create a Listing when he wants to travel from X to Y. A listing must be given the following attributes:

    to_location
    from_location
    start
    end
Here, start and end denote the start and end of the waiting period of the user.

In words:

`A wants to travel from Pilani to Delhi on 16th May. He is ready to leave from Pilani at any time between 6pm to 9pm. `

This makes a Listing by user A. 

A Group is a group of people who will share a cab. A group can have 1-4 members (members are Listings). A group too has the following attributes:

    to_location
    from_location
    start
    end
In words:

`A cab containing 3 people will leave from Pilani for Delhi on 16th May anytime between 4pm and 8pm. `

The above makes a group containing 4 members. 

The server automatically adds a listing into an existing group or makes a new group when a new listing is created. 
A listing once created cannot be and _should not_ be changed. 

## API 

To get a list of all listings: 
```GET /api/get_listings/```

To get a list of all groups:
`GET /api/get_groups/`

To add a new listing:
`GET /api/add_listing`

## Setting up the Server
 The following steps should help you set up the server:
 
  1. `git clone https://github.com/hedonhermdev/cabsharing-portal`
 
  2. `cd cabsharing-portal`
  
  3. `pip3 install -r requirements.txt`
  
  4. `python manage.py runserver`
 
## Getting and using an Auth token
 To access the API endpoints, you will need an Auth token. Do the following to get one:

  1. Go to (Google OAuth Playground)[https://developers.google.com/oauthplayground/]. 
 
  2. In the first step, select Google OAuth2, select both user.email and user.profile. Login using BITS Mail when asked. 
  
  3. You will get a bunch of JSON data on the right side, copy the id_token from there. 
  
  4. Using this id_token, send a GET request to /auth/register endpoint. 
  
  ```bash
  curl --location --request POST '127.0.0.1:8000/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id_token": <YOUR ID_TOKEN>
}'

```
 4. You will get a JSON response that is similar to this:
 
 ```JSON
  {
   "token": <token>,
   "username": <username>,
   "email": <email>
   }
 ```
 
 5. Copy the value of the token field and save it somewhere. 

 6. Use this token in the Authorization header in all further requests. 
 
 ```JavaScript
 var myHeaders = new Headers();
myHeaders.append("Authorization", "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6ImYyMDE5MDEyMCIsImV4cCI6MTU4NTI2Mjg4NCwiZW1haWwiOiJmMjAxOTAxMjBAcGlsYW5pLmJpdHMtcGlsYW5pLmFjLmluIn0.7WdcaO6mvlNEoFAz4ds7nvOWXLKJ5crDv3aPoj0F_YQ");

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  redirect: 'follow'
};

fetch("127.0.0.1:8000/api/get_listings", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
 ```
 
## The Algorithm
  Here is a sloppy explanation of the algorithm:
  
  ### A new listing is created
  1. Look for groups that are not full having the same `to_location` and `from_location`. This forms the first potential set of listings. 
  #### Case 1. Set is not empty
  2.1. From the above set: Find groups whose time_range(`(start, end)`) overlaps with the time_range of the listing. From this set find the one with the maximum overlap. This forms the second potential set of listings.
  ##### Case 1.1 Set is not empty
  2.1.1 Find the group with maximum overlap. This is the group the listing will be added to. Change this group's time_range to its overlap with the time_range of the listing. 
  ##### Case 1.2 Set is empty
  2.1.2 Make a new group with the attributes same as that of the listing. The listing is a member of this new group. 
  #### Case 2. Set is empty
  2.2 Make a new group with the attributes same as that of the listing. The listing is a member of this new group. 
  
  Basically find the best group. If group is not found make a new group for the user. This is a greedy algorithm (?!?!?!?!)
  
  
  
  
## Contributions and Roadmap
  Contributions are welcome. If you want to contribute to this project, get it contact with me. The following is the roadmap of things to be done:
  1. Implement authentication
  2. Write more views (Sign Up, Log In, User's listings, etc)
  3. Clean up the code (The algorithmic part of the code is messy and ugly) 

  If you are a frontend developer or an app developer and are interested in making a frontend/application for this then hit me up. 
