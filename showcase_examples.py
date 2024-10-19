from gedi import cdm

if __name__ == '__main__':

    # # alternative (choice) list
    # choice_set = ['z', 'x', 'y', 'w']
    #
    # # each dictionary represents a unique vote type
    # vote_type = [
    #     {
    #     "preference": ('w', 'x', 'z', 'y'),
    #     "role": "dictator",
    #     "round": 0,
    #     "validity": True,
    #     },
    #     {
    #     "preference": ('w', 'y', 'x', 'z'),
    #     "role": "voter",
    #     "round": 0,
    #     "validity": True,
    #     },
    #     {
    #     "preference": ('x', 'y', 'z', 'w'),
    #     "role": "voter",
    #     "round": 0,
    #     "validity": True,
    #     },
    #     {
    #     "preference": ('x', 'z', 'w', 'y'),
    #     "role": "voter",
    #     "round": 0,
    #     "validity": True,
    #     },
    #     {
    #         "preference": ('y', 'w', 'x', 'z'),
    #         "role": "voter",
    #         "round": 0,
    #         "validity": True,
    #     },
    #     {
    #         "preference": ('y', 'z', 'w', 'x'),
    #         "role": "voter",
    #         "round": 0,
    #         "validity": True,
    #     },
    # ]
    # # vote counts corresponding to above dictionary
    # vote_type_count = [7, 2, 4, 5, 1, 8]



    # Another example, cited from https://en.wikipedia.org/wiki/Score_voting
    choice_set = ['Memphis', 'Nashville', 'Chattanooga', 'Knoxville']
    vote_type = [
        {
            "preference": ('Memphis', 'Nashville', 'Chattanooga', 'Knoxville'),
            "role": "dictator",
            "round": 0,
            "validity": True,
        },
        {
            "preference": ('Nashville', 'Chattanooga', 'Knoxville', 'Memphis'),
            "role": "voter",
            "round": 0,
            "validity": True,
        },
        {
            "preference": ('Chattanooga', 'Knoxville', 'Nashville', 'Memphis'),
            "role": "voter",
            "round": 0,
            "validity": True,
        },
        {
            "preference": ('Knoxville', 'Chattanooga', 'Nashville', 'Memphis'),
            "role": "voter",
            "round": 0,
            "validity": True,
        },
    ]
    vote_type_count = [42, 26, 15, 17]

    # a score-based alternation
    # choice_set = ['Memphis', 'Nashville', 'Chattanooga', 'Knoxville']
    # range_scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # vote_type = [
    #     {
    #         "preference": (10, 4, 2, 0),
    #         "round": 0,
    #         "validity": True,
    #     },
    #     {
    #         "preference": (0, 10, 4, 2),
    #         "round": 0,
    #         "validity": True,
    #     },
    #     {
    #         "preference": (0, 6, 10, 6),
    #         "round": 0,
    #         "validity": True,
    #     },
    #     {
    #         "preference": (0, 5, 7, 10),
    #         "round": 0,
    #         "validity": True,
    #     },
    # ]
    # vote_type_count = [42, 26, 15, 17]


    # aggregate test profile
    test_profile = []
    for i in range(len(vote_type_count)):
        for j in range(vote_type_count[i]):
            test_profile.append(vote_type[i])

    print('Total votes:',len(test_profile))



    # cdm execution
    # single method
    # method = 'range_voting'
    # order, tally = cdm(choice_set, test_profile, voting_system=method, scale=range_scale)
    #
    # print(f"{method} order: ", order)
    # print(f"{method} tally: ", tally)

    # test multiple methods
    for method in ["random", "blind_dictatorial", "plurality", "bucklin", "borda_count", "irv", "minimax", "ranked_pairs"]:
        order, tally = cdm(choice_set, test_profile, voting_system=method)

        print(f"{method} order: ", order)
        print(f"{method} tally: ", tally)