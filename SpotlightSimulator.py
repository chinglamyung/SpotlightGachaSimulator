import random

#HYPERPARAMETERS - FEEL FREE TO TWEAK

DEBUG_STATEMENTS = True # feel free to change this to True and TRIALS to 1 to run a single simulation.

TRIALS = 1 # number of trials to run. the higher the number, the more accurate the simulation, but runs for longer.

NUM_OF_STEPS = 10 # 12k gems spent is five steps, for each over step you spend 3k more.
# 10 steps is 27k gems, the same amount as 11-step on an arcana banner.
# 17 steps is 48k gems spent, a.k.a. the point at which spark is guaranteed.

SET_1_NON_EXCELLENT_WEIGHT = 5
# ^probability to get any non-excellent prize is the probability to get any excellent prize multiplied by the weight

FIRST_THREE_STEPS_NON_EXCELLENT_WEIGHT = 10 # Data evidence suggests steps 1-3 have even lower rates for excellents

SET_1_EXCELLENT_NOT_GIRL_WEIGHT = 2
# ^probability of any non-stage-girl excellent prize is the probability to get the stage-girl prize multiplied by the weight
# if this number is 2, then each excellent prize will have equal chance to appear on the very first excellent prize roll.

SET_2_NON_EXCELLENT_WEIGHT = 6
# ^probability to get any non-excellent prize is the probability to get any excellent prize multiplied by the weight

SET_2_EXCELLENT_NOT_GIRL_WEIGHT = 3
# ^probability of any non-stage-girl excellent prize is the probability to get any stage-girl prize multiplied by the weight
# for example, if this number is 2, then - even though there are two slots for lovers,
# you still only have 33.3% chance to get Lover on the very first excellent prize roll.

# END OF HYPERPARAMETER DELCARATIONS

CURRENT_SET = 1; CURRENT_STEP = 1; SET1 = list(); SET2 = list()

def reset_trial():
    global CURRENT_SET; global CURRENT_STEP; global SET1; global SET2
    CURRENT_SET = 1
    CURRENT_STEP = 1
    SET1 = list(["stage girl", "excellent", "excellent", "garbage","garbage","garbage","garbage","garbage","garbage"])
    SET2 = list(["lover", "lover", "excellent", "garbage","garbage","garbage","garbage","garbage","garbage"])
    
def acquire_Excellent_Prize (pool):
    if CURRENT_SET == 1:
        if ("excellent" not in pool):
            return pool.pop(pool.index("stage girl"))
        roll_range = 1 + SET_1_EXCELLENT_NOT_GIRL_WEIGHT
        if ("stage girl" in pool and random.random() * roll_range < 1):
            return pool.pop(pool.index("stage girl"))
    else: # CURRENT_SET == 2
        if ("excellent" not in pool):
            return pool.pop(pool.index("lover"))
        roll_range = 1 + SET_2_EXCELLENT_NOT_GIRL_WEIGHT
        if (random.random() * roll_range < 1):
            return pool.pop(pool.index("lover"))
    return pool.pop(pool.index("excellent"))

def simulate(): # Simulate a single step. returns True if it succeeds in getting Lovers.
    global CURRENT_SET; global CURRENT_STEP; global SET1; global SET2
    
    if DEBUG_STATEMENTS:
        print(f"step: {CURRENT_STEP}, ", end="")
    
    # first, roll the 0.2% rate gacha "normally". chance of getting 1 or more copies of lovers in one 10x pull is 1.9821%
    if random.random() < 0.019821:
        if DEBUG_STATEMENTS:
            print ("Obtained in 0.2% gacha normally")
        return True
    
    # next, roll for a spotlight prize.
    roll_range = 0
    if (CURRENT_SET == 1):
        if (CURRENT_STEP != 4):
            if (CURRENT_STEP <= 3): # steps 1-3
                roll_range = 1 + FIRST_THREE_STEPS_NON_EXCELLENT_WEIGHT
            else: #steps 5-9
                roll_range = 1 + SET_1_NON_EXCELLENT_WEIGHT
            if ("garbage" not in SET1 or random.random() * roll_range < 1):
                if acquire_Excellent_Prize(SET1) == "stage girl":
                    if (random.random() < 0.4):
                        if (DEBUG_STATEMENTS):
                            print("Obtained in box1 stage girl excellent prize")
                        return True
                    if DEBUG_STATEMENTS:
                        print("Received: OLD stage girl")
                else:
                    if DEBUG_STATEMENTS:
                        print("Received: ordinary excellent prize")
            else: # failed to get an excellent prize
                SET1.pop(SET1.index("garbage"))
                if DEBUG_STATEMENTS:
                    print("Received: garbage")
        else: # CURRENT_STEP == 4
            if acquire_Excellent_Prize(SET1) == "stage girl":
                if (random.random() < 0.4):
                    if (DEBUG_STATEMENTS):
                        print("Obtained in box1 stage girl excellent prize")
                    return True
                if DEBUG_STATEMENTS:
                    print("Received: OLD stage girl")
            else:
                if DEBUG_STATEMENTS:
                    print("Received: ordinary excellent prize")
        # check if all three excellent prizes have been acquired in SET1
        if "stage girl" not in SET1 and "excellent" not in SET1:
            if (DEBUG_STATEMENTS):
                print ("changing set to BOX 2")
            CURRENT_SET = 2

    else: # CURRENT_SET == 2
        roll_range = 1 + SET_2_NON_EXCELLENT_WEIGHT
        if ("garbage" not in SET2 or random.random() * roll_range < 1):
            if acquire_Excellent_Prize(SET2) == "lover":
                if (DEBUG_STATEMENTS):
                    print("Obtained in box2 stage girl excellent prize")
                return True
            if DEBUG_STATEMENTS:
                print("Received: ordinary excellent prize")
        else: # failed to get an excellent prize
            SET2.pop(SET2.index("garbage"))
            if DEBUG_STATEMENTS:
                print("Received: garbage")
    
    CURRENT_STEP += 1
    
    if DEBUG_STATEMENTS:
        print("WHAT'S LEFT IN BOX: ", end="")
        print(SET1) if CURRENT_SET == 1 else print(SET2)
        print()
    
    return False

success = 0

for i in range(TRIALS):
    reset_trial()
    if DEBUG_STATEMENTS:
        print("NEW TRIAL STARTED. FRESH BOX1 CONTENTS:")
        print(SET1)
        print()
    
    for j in range(NUM_OF_STEPS):
        if simulate() == True:
            success += 1
            break

Chance_at_getting = success / TRIALS * 100
print()
print(f"AFTER RUNNING {TRIALS} TRIALS WITH {NUM_OF_STEPS} STEPS EACH,")
print(f"The simulated probability of getting Lover is {Chance_at_getting}%")