nodes = {
    1: {
        "host": "127.0.0.1",
        "port": 5001,
        "role": "leader",
        "followers": [2, 3],
    },
    2: {
        "host": "127.0.0.1",
        "port": 5002,
        "role": "follower",
        "followers": [],
    },
    3: {
        "host": "127.0.0.1",
        "port": 5003,
        "role": "follower",
        "followers": [],
    },
}
