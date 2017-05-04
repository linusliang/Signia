import numpy as np
import random

def print_investments(investments, amazing_percent, good_percent, okay_percent, fail_percent):
    amazing_count, good_count, okay_count, fail_count = 0, 0, 0, 0
    for i in range(investments.shape[0]):
        if investments[i] <= amazing_percent:
            amazing_count += 1
        elif investments[i] > amazing_percent and investments[i] <= amazing_percent + good_percent:
            good_count += 1
        elif investments[i] > good_percent and investments[i] <= amazing_percent + good_percent + okay_percent:
            okay_count += 1
        else:
            fail_count += 1
    print "amazing: %i, good: %i, okay: %i, fail: %i" % (amazing_count, good_count, okay_count, fail_count)
    return

#############################################################################
#                                                                           #
#                                                                           #
#                                                                           #
#               SIGNIA MONTE CARLO INVESTMENT SIMULATOR                     #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################

# Set global variables Here
#
num_investments = 20
num_simulations = 5

# Intialize Variables
investments = np.zeros(shape=(num_simulations, num_investments))
returns = np.zeros(shape=(num_simulations, num_investments))
dd_returns = np.zeros(shape=(num_simulations, num_investments))
double_down_flag = 1

for sim in range(num_simulations):

    # first determine the % outcomes for the fund
    #
    amazing_percent = random.randint(1,2)
    good_percent = random.randint(10,20)
    okay_percent = random.randint(15,25)
    fail_percent = 100 - amazing_percent - good_percent - okay_percent
    #print "amazing: %i%%, good: %i%%, okay: %i%%, fail: %i%%" % (amazing_percent, good_percent, okay_percent, fail_percent)

    # next make the investments
    #
    for i in range(num_investments):
        dice_roll = random.randint(1,100)
        investments[sim, i] = dice_roll
    #print_investments(investments[sim], amazing_percent, good_percent, okay_percent, fail_percent)

    # calculate returns
    #
    for i in range(num_investments):
        if investments[sim, i] <= amazing_percent:
            returns[sim,i] = 50
        elif investments[sim, i] > amazing_percent and investments[sim, i] <= amazing_percent + good_percent:
            returns[sim,i] = random.uniform(10.0, 20.0)
        elif investments[sim, i] > good_percent and investments[sim, i] <= amazing_percent + good_percent + okay_percent:
            returns[sim,i] = random.uniform(2.0, 5.0)
        else:
            returns[sim,i] = random.uniform(0.0, 1.0)
    #print "Fund Return:", np.around(returns[sim].mean(), decimals = 2)

    #  calculate returns with double down
    #
    if double_down_flag == 1:
        num_failed = (investments[sim] > amazing_percent + good_percent + okay_percent).sum()
        failed_weight = (.5 / num_investments)
        if num_failed == num_investments:
            dd_weight = failed_weight
        else:
            dd_weight = (.5 / num_investments) + (.5 / (num_investments-num_failed))
        for i in range(num_investments):
            if investments[sim, i] <= amazing_percent:
                dd_returns[sim,i] = 50 * dd_weight
            elif investments[sim, i] > amazing_percent and investments[sim, i] <= amazing_percent + good_percent:
                dd_returns[sim,i] = returns[sim,i] * dd_weight
            elif investments[sim, i] > good_percent and investments[sim, i] <= amazing_percent + good_percent + okay_percent:
                dd_returns[sim,i] = returns[sim,i] * dd_weight
            else:
                dd_returns[sim,i] = returns[sim,i] * failed_weight
        #print "DD Fund Return:", np.around(dd_fund_returns[sim].sum(), decimals = 2)

print "after %i simulations, the mean fund return is   :" % returns.shape[0], np.around(returns.mean(), decimals = 2)
if double_down_flag == 1: print "after %i simulations, the mean DD fund return is:" % returns.shape[0], np.around(dd_returns.sum(axis=1).mean(), decimals = 2)

print "after %i simulations, the median fund return is   :" % returns.shape[0], np.around(np.median(np.mean(returns, axis=1)), decimals = 2)
if double_down_flag == 1: print "after %i simulations, the median DD fund return is:" % returns.shape[0], np.around(np.median(dd_returns.sum(axis=1)), decimals = 2)
