data = [
    {
        "_id": {
            "$oid": "6588f8243f321abc17040aee"
        },
        "link": "https://amzn.to/3uu7iEB",
        "img": "https://simpleghar-bio-images.s3.ap-south-1.amazonaws.com/Screenshot 2023-12-25 at 5.51.19 PM.webp",
        "title": "8-in-1 Gadget Cleaning Kit",
        "index": 0,
        "modified_date": {
            "$date": "2024-02-13T14:54:44.159Z"
        },
        "youtube_title": None,
        "youtube_url": None
    },
    {
        "_id": {
            "$oid": "6588f8243f321abc17040aef"
        },
        "link": "https://amzn.to/3SXsg88",
        "img": "https://simpleghar-bio-images.s3.ap-south-1.amazonaws.com/Screenshot 2023-12-25 at 5.47.17 PM.webp",
        "title": "Smart Weighing Scale",
        "index": 0,
        "modified_date": {
            "$date": "2024-02-13T14:54:40.854Z"
        },
        "youtube_title": None,
        "youtube_url": None
    }
]

# Create a dictionary to map IDs to index numbers
id_to_index = {item['_id']['$oid']: idx for idx, item in enumerate(data)}

# Print the dictionary to see how IDs are mapped to their indexes
print("ID to Index Mapping:")
print(id_to_index)
