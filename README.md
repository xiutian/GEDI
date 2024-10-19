# GEDI

## File Descriptions
The main processing functions are found in `gedi.py`, and `showcase_examples.py` provides example test cases to demonstrate how the system works.

- **`gedi.py`**: Contains the main vote processing functions, including the core function `cdm()`.
- **`showcase_examples.py`**: Provides test examples to showcase how to use the functions in `gedi.py`.

## Function: `cdm(A, raw_profile, voting_system, scale=None)`
### Parameters
  - A (choice set):<br>
  A list of alternatives in the format A = [a_1, a_2, ..., a_m].

    - Type: list
    - Example: A = ['apple', 'banana', 'cherry']
  
- raw_profile (vote profile): <br>
A profile of ballots P = [ballot_1, ballot_2, ..., ballot_n], where each vote is a dictionary. Each dictionary has a key 'preference', which maps to a ranked tuple of the choice set.
  - Type: list of dict
  - Example:
  ```python
  raw_profile = [
  {'preference': ('banana', 'apple', 'cherry')},
  {'preference': ('cherry', 'banana', 'apple')}
  ]
  ```
    
- voting_system (method):<br>
A string specifying the voting method to use. The following methods are currently supported:<br>["random", "range_voting", "blind_dictatorial", "plurality", "bucklin", "borda_count", "irv", "minimax", "ranked_pairs"].

- scale (optional):<br>
A numerical scale of votes, used only by the range voting method.

  - Type: list
  - Example: [0 ,1 ,2, 3, 4, 5]

###  Output
The function returns two outputs:

- tally:
A numerical count of "final scores." The meaning of these scores varies depending on the voting method used.
  - Type: dict
- order:
A preferential order dictionary, which may contain ties.
  - Type: dict
  - Example:
  ```python
  order = {'banana': 1, 'apple': 2, 'cherry': 2}
  ```