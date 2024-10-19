import random
import numpy as np


# a function to according to the tally
def tally_to_order(tally, order):
    # order list
    initial_order = 0
    previous_vote_num = -0.1
    for alternative in tally:

        if previous_vote_num != tally[alternative]:
            initial_order += 1

        order[alternative] += initial_order

        # record current, consider ties
        previous_vote_num = tally[alternative]

    # sort order by rank in ascending
    order = {k: v for k, v in sorted(order.items(), key=lambda x: x[1], reverse=False)}
    return order

# a function to check the validity of a ballot
def check_ballot(A, ballot, dataset, scale=None,):
    ballot_validity = True

    A.sort()
    ballot_prefer_sorted = list(ballot["preference"])
    ballot_prefer_sorted.sort()

    if dataset == 'single_select':
        if ballot_prefer_sorted[0] not in A:
            ballot_validity = False

    elif dataset == 'range':
        for score in ballot["preference"]:
            if score not in scale:
                ballot_validity = False

    #  ballot must complete and identical to the choice set
    elif A != ballot_prefer_sorted:
        ballot_validity = False
        # print("Ballot is not valid for incomplete")

    return ballot_validity


def cdm(A, raw_profile, voting_system, scale=None,):
    # initialize order and tally dicts
    order = {}
    tally = {}
    for alternative in A:
        order[alternative] = 0
        tally[alternative] = 0

    # assign a [0,9] range scale if not specified
    if scale is None:
        scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # some methods quire unique vote format
    method2data = {
        "range_voting": 'range',
        "random": 'base',
        "blind_dictatorial": 'base',
        "plurality": 'base',
        "bucklin": 'base',
        "borda_count": 'base',
        "irv": 'base',
        "minimax": 'base',
        "ranked_pairs": 'base',
    }

    # filter out invalid votes
    profile = []
    for ballot in raw_profile:
        if check_ballot(A, ballot, method2data[voting_system], scale):
            profile.append(ballot)
        else:
            continue

    if voting_system == 'blind_dictatorial':

        # randomly assign a dictator
        dictatorial_ballot = random.choice(profile)
        # print(dictatorial_ballot["preference"])

        for i in range(len(A)):
            order[dictatorial_ballot["preference"][i]] = i+1

        return order, tally

    elif voting_system == 'single_select':

        # randomly assign a dictator
        random_order = A.copy()
        random.shuffle(random_order)

        sole_ballot = random.choice(profile)

        random_order.remove(sole_ballot["preference"][0])

        # print(random_order)
        if type(sole_ballot["preference"]) is str:
            sole_ballot["preference"] = [sole_ballot["preference"]]

        for i in range(len(random_order)):
            sole_ballot["preference"].append(random_order[i])

        for i in range(len(sole_ballot["preference"])):
            order[sole_ballot["preference"][i]] = i+1

        return order, tally

    elif voting_system == 'random':
        random_ballot = {}
        # print(random_ballot["preference"])
        random_order = A.copy()
        random.shuffle(random_order)

        for i in range(len(A)):
            order[random_order[i]] = i+1

        return order, tally

    elif voting_system == 'plurality':
        top_rank = []

        # count vote
        for ballot in profile:
            top_rank.append(ballot["preference"][0])

        for alt in A:
            tally[alt] = top_rank.count(alt)

        # reorder tally by vote in descending order
        tally = {k: v for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True)}

        order = tally_to_order(tally, order)

        return order, tally

    elif voting_system == "borda_count":

        # build borda point
        borda_point = []
        for i in range(len(A)):
            borda_point.append(i)
        borda_point.sort(reverse=True)
        # print(borda_point)

        for ballot in profile:
            for alternative in A:
                # count score with weight
                tally[alternative] += borda_point[ballot["preference"].index(alternative)]

        # reorder tally by vote in descending order
        tally = {k: v for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True)}
        order = tally_to_order(tally, order)
        return order, tally

    elif voting_system == "range_voting":

        for ballot in profile:
            for i in range(len(A)):
                # count scores
                tally[A[i]] += ballot["preference"][i]

        # reorder tally by vote in descending order
        tally = {k: v for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True)}

        order = tally_to_order(tally, order)
        return order, tally

    elif voting_system == "bucklin":

        absolute_majority = False

        for runs in range(len(A)):
            # count run-th choice vote until an absolute majority is found
            for alt in A:
                for ballot in profile:
                    if ballot["preference"][runs] == alt:
                        tally[alt] += 1
                    if tally[alt] > len(profile)/2:
                        absolute_majority = True

            if absolute_majority:
                break

        # reorder tally by vote in descending order
        tally = {k: v for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True)}
        order = tally_to_order(tally, order)

        return order, tally

    elif voting_system == "irv":

        eliminated_alt = []

        # repeat until m-1 alts are eliminated
        while len(eliminated_alt) < len(A):
            round = 0 # early stop
            top_rank = []
            # count first-order vote,
            for ballot in profile:
                for preference in ballot["preference"]:
                    # if eliminated, count next preference
                    if preference in eliminated_alt:
                        continue
                    else:
                        top_rank.append(preference)
                        break

            temp_vote_list = []
            for alt in A:
                if alt not in eliminated_alt:
                    tally[alt] = top_rank.count(alt)
                    temp_vote_list.append(tally[alt])

            # print("temp_vote_list: ", temp_vote_list)

            # eliminate least-favored vote
            for alt in A:
                if alt not in eliminated_alt:
                    if tally[alt] == min(temp_vote_list):
                        eliminated_alt.append(alt)

            if len(A) - len(eliminated_alt) == 1:
                break
            else:
                for alt in A:
                    # renew tally
                    if alt not in eliminated_alt:
                        tally[alt] = 0

            # print("eliminated_alt: ", eliminated_alt)

            # early stopping
            round += 1
            if round == len(A):
                break

        # reorder tally by vote in ascending order
        tally = {k: v for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True)}
        order = tally_to_order(tally, order)

        return order, tally

    elif voting_system == "minimax":

        rank_pairs = []
        for ballot in profile:
            for i in range(len(ballot["preference"]) - 1):
                for j in range(len(ballot["preference"]) - i - 1):
                    rank_pairs.append((ballot["preference"][i], ballot["preference"][i+j+1]))

        # create a dict for matrix cell corresponding to alts
        matrix_dict = {}
        for i in range(len(A)):
            matrix_dict[A[i]] = i

        tally_matrix = np.zeros((len(A), len(A)))
        for pair in rank_pairs:
            tally_matrix[matrix_dict[pair[0]]][matrix_dict[pair[1]]] += 1
            tally_matrix[matrix_dict[pair[1]]][matrix_dict[pair[0]]] -= 1

        # print(tally_matrix)

        # calculate the worst defeat
        for alt in A:
            tally[alt] = max(tally_matrix[:, matrix_dict[alt]]) * -1

        # print(tally)
        # reorder tally by put the 'minimum' worst defeat first order
        tally = {k: v for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True)}
        order = tally_to_order(tally, order)

        return order, tally

    elif voting_system == "ranked_pairs":

        rank_pairs = []
        for ballot in profile:
            for i in range(len(ballot["preference"]) - 1):
                for j in range(len(ballot["preference"]) - i - 1):
                    rank_pairs.append((ballot["preference"][i], ballot["preference"][i+j+1]))

        # print(rank_pairs)

        pairs_count = {}
        for pair in rank_pairs:
            if pair in pairs_count:
                pairs_count[pair] += 1
            else:
                pairs_count[pair] = 1

            if pair[::-1] in pairs_count:
                pairs_count[pair[::-1]] -= 1
            else:
                pairs_count[pair[::-1]] = -1

        pairs_count = {k: v for k, v in sorted(pairs_count.items(), key=lambda x: x[1], reverse=True)}
        # print(pairs_count)

        compare_matrix = np.zeros((len(A), len(A)))

        matrix_dict = {}
        for i in range(len(A)):
            matrix_dict[A[i]] = i

        for pair in pairs_count:
            # check only positive pairs due to symmetry
            if pairs_count[pair] > 0:
                # skip already decided cells
                if compare_matrix[matrix_dict[pair[0]]][matrix_dict[pair[1]]] != 0:
                    continue
                else:
                    compare_matrix[matrix_dict[pair[0]]][matrix_dict[pair[1]]] = 1
                    compare_matrix[matrix_dict[pair[1]]][matrix_dict[pair[0]]] = -1

                    # transitive
                    for alt in A:
                        if alt not in pair:
                            if compare_matrix[matrix_dict[pair[1]]][matrix_dict[alt]] == 1:
                                compare_matrix[matrix_dict[pair[0]]][matrix_dict[alt]] = 1
                                compare_matrix[matrix_dict[alt]][matrix_dict[pair[0]]] = -1

                            if compare_matrix[matrix_dict[alt]][matrix_dict[pair[0]]] == 1:
                                compare_matrix[matrix_dict[alt]][matrix_dict[pair[1]]] = 1
                                compare_matrix[matrix_dict[pair[1]]][matrix_dict[alt]] = -1

                # print(compare_matrix)
            else:
                continue

        for alt in A:
            tally[alt] = sum(compare_matrix[matrix_dict[alt]])

        # reorder tally by vote in ascending order
        tally = {k: v for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True)}
        order = tally_to_order(tally, order)

        return order, tally