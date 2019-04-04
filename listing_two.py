import des_oop

first_cabbages = des_oop.GenerateAtStart(num=3)  # For 3 cabbages in stock.
cabbages_on_shelf = des_oop.AdvanceTimeUniformDistribution(low=7,high=12)
cabbage_rotten_cntr = des_oop.TerminateEntity()
cabbage_reorder_proc = des_oop.AdvanceTimeUniformDistribution(low=1,high=15)
cabbages_to_stock = des_oop.EntityCounter()

first_cabbages.set_target(cabbages_on_shelf)
cabbages_on_shelf.set_target(cabbage_rotten_cntr)
cabbage_rotten_cntr.set_target(cabbage_reorder_proc)
cabbage_reorder_proc.set_target(cabbages_to_stock)

simulation = des_oop.Simulation([first_cabbages])
simulation.run(stop_after=(cabbage_rotten_cntr,10))  # Stop after 10 go rotten.
print(cabbage_rotten_cntr.total_count(),"cabbages went rotten.")
