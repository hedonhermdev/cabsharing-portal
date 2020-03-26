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
