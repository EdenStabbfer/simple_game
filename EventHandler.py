import pygame as pg


class EventHandler:
    def __init__(self):
        self.other_events = []
        self.key_down_events = []
        self.key_up_events = []

    def handle(self):
        for event in pg.event.get():
            # Handle exit event
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Handle key down events
            if event.type == pg.KEYDOWN:
                for func in self.key_down_events:
                    func(event)
            # Handle key up events
            if event.type == pg.KEYUP:
                for func in self.key_up_events:
                    func(event)
            # Handle other events
            for func in self.other_events:
                func(event)

    def bind(self, func, type=None):
        if type == pg.KEYDOWN:
            self.key_down_events.append(func)
        elif type == pg.KEYUP:
            self.key_up_events.append(func)
        else:
            self.other_events.append(func)

    def remove(self, func):
        if func in self.key_down_events:
            self.key_down_events.remove(func)
        elif func in self.key_up_events:
            self.key_up_events.remove(func)
        elif func in self.other_events:
            self.other_events.remove(func)
