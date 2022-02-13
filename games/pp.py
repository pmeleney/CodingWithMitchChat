import random

def personal_preferences(entries, num=4, already_chosen = []):
    # Remove already chosen items from list
    print(already_chosen)
    for item in already_chosen:
        entries.remove(item)
        print

# Ensure there are enough choices to make a list
    if len(entries) < 4:
        return {0: "Not enough choices left, add more to your lists."}, already_chosen
    else:
    # Make peronsal preferences list!
        output = {}
        for i in range(num):
            choice = random.choice(entries)
            output[i] = choice
            already_chosen.append(choice)
            # Remove items that have already appeared in lists
            entries.remove(choice)

        return output, already_chosen
