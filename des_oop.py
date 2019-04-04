import random

class Entity:
    def __init__(self):
        self.next = None

    def run(self):
        return 0

    def set_target(self, instance):
        print('set_target', self.__dir__)
        self.next = instance

class GenerateEntityUniformDistribution(Entity):
    def __init__(self, low, high):
        self.next = None
        self.total = 0
        self.low = low
        self.high = high
        self.processing_time = random.uniform(low, high)
        print('processing_time', self.processing_time)

    def run(self):
        print('run GenerateEntityUniformDistribution')
        self.total += 1
        self.processing_time = random.uniform(self.low, self.high)
        print('processing_time', self.processing_time)
        return self.processing_time

    def state(self):
        return 'SOURCE'

class AdvanceTimeUniformDistribution(GenerateEntityUniformDistribution):
    def run(self):
        print('run AdvanceTimeUniformDistribution')
        self.total += 1
        self.processing_time = random.uniform(self.low, self.high)
        return self.processing_time

    def state(self):
        return 'SOURCE'

class GenerateAtStart(Entity):
    stock = 0

    def __init__(self, num):
        GenerateAtStart.stock = num
        self.processing_time = 0

    def state(self):
        return 'SOURCE'

class DisplaceEntity(Entity):
    def __init__(self, incoming, outgoing):
        incoming.run()
        outgoing.run()
        GenerateAtStart.stock -= 1

    def add_transition(self, main, alternative):
        if (GenerateAtStart.stock > 0):
            main.run()
        else:
            alternative.run()

    def state(self):
        return 'DISPLACE'

class EntityCounter(Entity):
    def __init__(self):
        self.next = None
        self.counter = 0

    def run(self):
        print('run EntityCounter')
        self.counter += 1

    def reset(self):
        print('reset EntityCounter')
        self.counter = 0

    def total_count(self):
        return self.counter

    def count(self):
        return self.counter

    def state(self):
        return 'COUNTER'

class TerminateEntity(Entity):
    def __init__(self):
        self.next = None
        self.counter = 0

    def run(self):
        print('run TerminateEntity')
        self.counter += 1

    def reset(self):
        print('reset TerminateEntity')
        self.counter = 0

    def total_count(self):
        return self.counter

    def count(self):
        return self.counter

    def state(self):
        return 'TERMINATOR'

class Simulation:
    def __init__(self, starting_entities):
        self.fel = []
        self.current_time = 0
        for starting_entity in starting_entities:
            self.fel.append([starting_entity, starting_entity.processing_time])

    def run(self, stop_after):
        print('run Simulation')
        terminator = stop_after[0]
        terminate_after = stop_after[1]
        print(self.fel)

        for event in self.fel:
            cur_event = event[0]
            event_time = event[1]
            self.current_time = event_time

            if (terminator.counter >= terminate_after):
                print('terminator break')
                break
            elif (cur_event.state() == 'SOURCE'):
                print('source block')
                source_event = cur_event
                while (cur_event.next):
                    cur_event = cur_event.next
                    event_time = self.current_time
                    self.fel.append([cur_event, event_time])
                self.current_time = self.current_time + source_event.run()
                self.fel.append([source_event, self.current_time])
            elif (cur_event.state() == 'TERMINATOR'):
                print('terminator block')
                cur_event.run()
            else:
                print('non terminator and source block')
                cur_event.run()

    def state(self):
        return 'SIMULATION'

