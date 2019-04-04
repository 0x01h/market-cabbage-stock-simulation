import des

trial = 20
# Generic stop_after conditions:
# - total_cus_arrived
# - happy_cus_left
# - sad_cus_left
# - time
stop_after = ('total_cus_arrived', 200)
stock_range = (3, 30)

# des.simulation(stock, stop_after)
test_results = des.test(trial, stock_range, stop_after)
minimum_rott_cabbage, best_stock_size = des.draw(test_results, stock_range)

print('Trials for each simulation:', trial)
print('Stop condition:', stop_after)
print('Stock range to simulate:', stock_range)
print('Best stock size:', best_stock_size)
print('Minimum total number of rotten cabbages:', minimum_rott_cabbage)