import des_oop

cust_entry = des_oop.GenerateEntityUniformDistribution(low=0,high=3)
cust_counter = des_oop.EntityCounter()
cust_leave = des_oop.TerminateEntity()

cust_entry.set_target(cust_counter)
cust_counter.set_target(cust_leave)

simulation = des_oop.Simulation([cust_entry])
simulation.run(stop_after=(cust_leave,10))  # Stop when 10 customers have left.
print(cust_counter.total_count(),"customers were simulated.")