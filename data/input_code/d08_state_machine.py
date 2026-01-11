class State:
    def __init__(self, name, on_enter=None, on_exit=None):
        self.name = name
        self.on_enter = on_enter
        self.on_exit = on_exit

class Transition:
    def __init__(self, trigger, source, dest, condition=None):
        self.trigger = trigger
        self.source = source
        self.dest = dest
        self.condition = condition

class StateMachine:
    def __init__(self, initial=None):
        self.states = {}
        self.transitions = {}
        self.current = None
        self.initial = initial
        self.history = []
    
    def add_state(self, name, on_enter=None, on_exit=None):
        self.states[name] = State(name, on_enter, on_exit)
        if self.initial is None:
            self.initial = name
    
    def add_transition(self, trigger, source, dest, condition=None):
        t = Transition(trigger, source, dest, condition)
        if trigger not in self.transitions:
            self.transitions[trigger] = []
        self.transitions[trigger].append(t)
    
    def start(self):
        if self.initial and self.initial in self.states:
            self.current = self.states[self.initial]
            if self.current.on_enter:
                self.current.on_enter()
            self.history.append(self.initial)
    
    def trigger(self, event):
        if event not in self.transitions:
            return False
        for t in self.transitions[event]:
            if t.source == self.current.name:
                if t.condition is None or t.condition():
                    return self._execute(t)
        return False
    
    def _execute(self, t):
        if self.current.on_exit:
            self.current.on_exit()
        self.current = self.states[t.dest]
        if self.current.on_enter:
            self.current.on_enter()
        self.history.append(t.dest)
        return True
    
    def can_trigger(self, event):
        if event not in self.transitions:
            return False
        for t in self.transitions[event]:
            if t.source == self.current.name:
                if t.condition is None or t.condition():
                    return True
        return False
    
    @property
    def state(self):
        return self.current.name if self.current else None
    
    def reset(self):
        self.history = []
        self.current = None
        self.start()
