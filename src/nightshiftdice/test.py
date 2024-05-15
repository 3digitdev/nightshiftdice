from dataclasses import dataclass, field


@dataclass
class Bar:
    name: str
    max: int = field()
    value: int = field(default=0)

    def __post_init__(self):
        self.value = int(self.value)
        self.max = int(self.max)
        if self.value > self.max:
            self.value = self.max

    def __str__(self):
        parts = min(50, self.max)
        filled = self.value
        if parts == 50:
            filled = int(filled / self.max * parts)
        return f'{"█" * filled}{"▒" * (parts - filled)} ({self.value}/{self.max})'

    def inc(self):
        self.value += 1
        if self.value > self.max:
            self.value = self.max

    def dec(self):
        self.value -= 1
        if self.value < 0:
            self.value = 0

    def to_json(self):
        return {'name': self.name, 'value': self.value, 'max': self.max}

    @classmethod
    def from_json(cls, data):
        return cls(data['name'], data['value'], data['max'])

    def run(self, cmd, args):
        print(cmd, args)
        getattr(self, cmd)(*args)


b = Bar('Max', '100', '0')
b.run('inc', [])
print(b)
