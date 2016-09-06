from hog import hogtimus_prime

# rp[swapped][reroll][num_roll][target_score][pig_out]:
#       The raw probabilty of getting TARGET_SCORE score when using dice [SWAPPED][REROLL] and throwing NUM_ROLL dices
#
# rp[swapped][reroll][num_roll][target_score][False]:
#       For dice [SWAPPED][REROLL], chance of getting TARGET_SCORE score without triggering pig out.
# rp[swapped][reroll][num_roll][target_score][True]:
#       For dice [SWAPPED][REROLL], chance of getting TARGET_SCORE ones by throwing NUM_ROLL dices.

rp = [[[[[0 for o in range(1 + 1)]
         for t in range(60 + 1)]
        for n in range(10 + 1)]
       for r in range(1 + 1)]
      for s in range(1 + 1)]

def find_rp(side, reroll):
    def calc_chance(d):
        if reroll:
            if d % 2 != 0:
                return 1 / (2 * side)
            else:
                return 1 / side + 1 / (2 * side)
        else:
            return 1 / side

    a = [[[0 for o in range(1 + 1)]
          for t in range(60 + 1)]
         for n in range(10 + 1)]

    # Init for PIG_OUT = False
    for t in range(2, side + 1):
        a[1][t][False] = calc_chance(t)
    # Calculate for PIG_OUT = False
    for n in range(2, 10 + 1):
        for t in range(1, 60 + 1):
            for d in range(2, side + 1): # D as in DELTA_SCORE
                if t - d >= 0:
                    a[n][t][False] += calc_chance(d) * a[n - 1][t - d][False]

    # Init for PIG_OUT = True
    a[1][1][True] = calc_chance(1)
    a[1][0][True] = 1 - a[1][1][True]
    # Calculate for PIT_OUT = True
    for n in range(2, 10 + 1):
        for t in range(1, 60 + 1):
            a[n][t][True] += (1 - calc_chance(1)) * a[n - 1][t][True]
            a[n][t][True] += calc_chance(1) * a[n - 1][t - 1][True]
        a[n][0][True] = 1
        for t in range(1, 60 + 1):
            a[n][0][True] -= a[n][t][True]

    return a

# p[0][0], six_sided
rp[0][0] = find_rp(6, False)

# p[0][1], six_sided_reroll
rp[0][1] = find_rp(6, True)

# p[1][0], four_sided
rp[1][0] = find_rp(4, False)

# p[1][1], four_sided_reroll
rp[1][1] = find_rp(4, True)

# Combining results and testing for Hogtimus Prime and When Pigs Fly
# p[swapped][reroll][num_roll][target_score]:
#       The final probabilty of getting TARGET_SCORE turn result when using dice [SWAPPED][REROLL] and throwing NUM_ROLL dices
p = [[[[0 for t in range(25 + 1)]
       for n in range(10 + 1)]
      for r in range(1 + 1)]
     for s in range(1 + 1)]

for s in range(0, 1 + 1):
    for r in range(0, 1 + 1):
        for n in range(1, 10 + 1):
            for t in range(1, 60 + 1):
                score = t
                chance = rp[s][r][n][t][False] + rp[s][r][n][t][True]

                score = hogtimus_prime(score)
                score = min(score, 25 - n)

                p[s][r][n][score] += chance

# Printing
for s in range(1 + 1):
    for r in range(1 + 1):
        print('[', end='')
        for n in range(10 + 1):
            if n != 0:
                print('\t\t   ', end='')
            print('[', end='')
            for t in range(25 + 1):
                # print('({0}, {1})'.format(rp[s][r][n][t][0], rp[s][r][n][t][1]), end='')
                print(p[s][r][n][t], end='')
                if t != 25:
                    print(', ', end='')
            print(']', end='')
            if n != 10:
                print(',', end='')
            print()
        print('\t\t   ]')
        print()
        print()
