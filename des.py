import numpy as np
import matplotlib.pyplot as plt
from random import uniform


def order_cabbage():
    order_time = uniform(1, 15)  # Order arrival time for coming cabbages
    return order_time


def order_arrived(available_cabbages):
    available_cabbages += 1
    rotten_time = uniform(7, 12)  # Rotten time for arrived cabbages
    return available_cabbages, rotten_time


def cus_entry(available_cabbages, happy_cus_left, sad_cus_left):
    cus_arr_time = uniform(0, 3)  # Customer arrival time after one customer left
    
    if (available_cabbages > 0):
        available_cabbages -= 1
        happy_cus_left += 1
        return available_cabbages, happy_cus_left, sad_cus_left, cus_arr_time
    else:
        sad_cus_left += 1
        return available_cabbages, happy_cus_left, sad_cus_left, cus_arr_time


def simulation(stock, terminators, verbose_fel=False, test_mode=False):
    # Initial assignments
    stock = stock
    available_cabbages = stock
    total_rotten = 0
    total_cus_arrived = 0
    sad_cus_left = 0
    happy_cus_left = 0
    time = 0
    iterator = 0
    sim_vars = {'sad_cus_left': sad_cus_left, 'happy_cus_left': happy_cus_left,
    'total_cus_arrived': total_cus_arrived, 'total_rotten': total_rotten,
    'time': time, 'iterator': iterator}
    
    fel = [['cus_entry', time]]  # Future event list
    init_rotten_cabbage_events = []
    for _ in range(0, stock):
        init_rotten_time = uniform(7, 12)
        init_rotten_cabbage_events.append(['rotten_cabbage', init_rotten_time])
    init_rotten_cabbage_events.sort(key=lambda x: x[1])  # Sort by time
    fel = fel + init_rotten_cabbage_events  # Populated and ready future event list

    termination = terminators[1]
    terminator_id = terminators[0]
    terminator = sim_vars[terminator_id]

    print('BEGINNING OF THE SIMULATION!',end='\n\n') if (not test_mode) else None
    if (verbose_fel and not test_mode):
        print('Starting FEL:')
        print(fel,end='\n\n')

    while (True):
        # Simulation termination check
        if (terminator >= termination):
            print('Simulation was terminated!',end='\n\n') if (not test_mode) else None
            break

        curr_event_id = fel[iterator]
        current_event = curr_event_id[0]
        time = curr_event_id[1]

        if (not test_mode):
            print('\nCurrent Event ID:')
            print(curr_event_id,end='\n\n')

        if (current_event == 'cus_entry'):
            if (not test_mode):
                print('Customer arrived!')
                print('Available cabbages:', str(available_cabbages))
            total_cus_arrived += 1
            ac, h_cus, s_cus, arr_time = cus_entry(available_cabbages, happy_cus_left, sad_cus_left)
            if ac < available_cabbages:
                print('Happy customer! :)') if (not test_mode) else None
                for curr_it in range(iterator+1, len(fel)):
                    if (fel[curr_it][0] == 'rotten_cabbage'):
                        fel.pop(curr_it)
                        print('Future rotten cabbage event was removed from FEL!') if (not test_mode) else None
                        break
            else:
                print('Sad customer! :(') if (not test_mode) else None
            happy_cus_left = h_cus
            sad_cus_left = s_cus
            next_cus_time = time + arr_time
            available_cabbages = ac
            if (not test_mode):
                print('Updated number of cabbages:', str(available_cabbages))
                print('Order cabbage added to FEL!')
                print('Customer entry added to FEL!')
            fel.append(['order_cabbage', time])
            fel.append(['cus_entry', next_cus_time])

        elif (current_event == 'order_cabbage'):
            print('Order cabbage!') if (not test_mode) else None
            order_time = order_cabbage()
            print('Order arrived added to FEL!') if (not test_mode) else None
            fel.append(['order_arrived', time + order_time])

        elif (current_event == 'order_arrived'):
            print('Order arrived! :)') if (not test_mode) else None
            available_cabbages, rotten_time = order_arrived(available_cabbages)
            print('Updated number of cabbages:', str(available_cabbages)) if (not test_mode) else None
            print('Rotten cabbage added to FEL!') if (not test_mode) else None
            fel.append(['rotten_cabbage', time + rotten_time])

        elif (current_event == 'rotten_cabbage'):
            print('Cabbage went rotten!') if (not test_mode) else None
            total_rotten += 1
            available_cabbages -= 1
            print('Available cabbages:', str(available_cabbages)) if (not test_mode) else None
            order_time = order_cabbage()
            print('Order cabbage added to FEL!') if (not test_mode) else None
            fel.append(['order_cabbage', time + order_time])
            
        else:
            print('Simulation Error: Undefined Event!')

        fel.sort(key=lambda x: x[1])
        iterator += 1
        sim_vars = {'sad_cus_left': sad_cus_left, 'happy_cus_left': happy_cus_left,
        'total_cus_arrived': total_cus_arrived, 'total_rotten': total_rotten,
        'time': time, 'iterator': iterator}
        terminator = sim_vars[terminator_id]

        if (verbose_fel):
            print('Current FEL:')
            print(fel,end='\n\n')

    if (not test_mode):
        print('END OF THE SIMULATION!',end='\n\n')
        print('Total number of customers arrived:',total_cus_arrived)
        print('Total happy customers left:',happy_cus_left)
        print('Total sad customers left:',sad_cus_left)
        print('Total time elapsed: ' + str(time) + ' days.')
        print('Total rotten cabbages:',total_rotten)
        print('Boundary for sad customer rate:',3/1000)
        print('Sad customer rate:',sad_cus_left/total_cus_arrived)
        print('SUCCESS ON HAPPY CUSTOMER RATE!') if (3/1000 > sad_cus_left/total_cus_arrived) else print('FAILURE ON HAPPY CUSTOMER RATE!')
        print('Total number of iterations in event list:',iterator,end='\n\n')
    if (verbose_fel):
        print('Final FEL:')
        print(fel)
    return sim_vars


def test(trial, stock_range, stop_after):
    if (stock_range[0] < 1 or stock_range[1] < 1 and not (stock_range[0] <= stock_range[1])):
        return print('Give a valid stock range!')

    print('BEGINNING OF THE TEST',end='\n\n')
    print('Number of trials:',trial)
    total_cus_arrived, happy_cus_left, sad_cus_left, time, total_rotten = (0,) * 5
    trial_results = [-1] * stock_range[1]
    test_results = trial_results
    valid_trials = 0
    remaning_sim = (stock_range[1] - stock_range[0]) * trial - 1
    is_valid = False

    print('REMAINING SIMULATION')
    for curr_stock in range(stock_range[0], stock_range[1]):
        for _ in range(0, trial):
            print('          ',end='\r')  # Clear counter
            print(remaning_sim,end='\r')
            remaning_sim -= 1
            sim_vars = simulation(curr_stock, stop_after, test_mode=True)
            total_cus_arrived = sim_vars['total_cus_arrived']
            happy_cus_left = sim_vars['happy_cus_left']
            sad_cus_left = sim_vars['sad_cus_left']
            time = sim_vars['time']
            total_rotten = sim_vars['total_rotten']
            sad_cus_rate = sad_cus_left/total_cus_arrived
            # Valid or invalid trials to calculate
            if (3/1000 > sad_cus_rate):
                if (not is_valid):
                    is_valid = True
                    trial_results[curr_stock] = 0
                valid_trials += 1
                trial_results[curr_stock] += total_rotten
            else:
                continue

        is_valid = False
        if (valid_trials != 0):
            test_results[curr_stock] /= valid_trials
            valid_trials = 0

    test_results = test_results[stock_range[0]:]
    print('\n\nEND OF THE TEST!',end='\n\n')
    return test_results


def draw(test_results, stock_range):
    test_results = test_results
    x_labels = []
    for stock in range(stock_range[0], stock_range[1]):
        x_labels.append(str(stock))

    invalid_results = []
    for it in range(0, len(test_results)):
        if (test_results[it] == -1):
            invalid_results.append(it)

    for invalid_result in sorted(invalid_results, reverse=True):
        del x_labels[invalid_result]

    test_results = list(filter(lambda a: a != -1, test_results))

    ind = np.arange(len(test_results))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, test_results, width,
                color='IndianRed', label='Average of Total Rotten Cabbages')

    ax.set_xlabel('Stock Sizes')
    ax.set_ylabel('Average of Total Rotten Cabbages')
    ax.set_title('Simulation Results for Accepted Trials')
    ax.set_xticks(ind)
    ax.set_xticklabels(x_labels)
    ax.legend()
    plt.show()

    minimum_rott_cabbage = x_labels[0]
    best_stock_size = test_results[0]

    for it in range(0, len(minimum_rott_cabbage)):
        if (minimum_rott_cabbage < x_labels[it]):
            minimum_rott_cabbage = x_labels[it]
            best_stock_size = test_results[it]

    return best_stock_size, minimum_rott_cabbage