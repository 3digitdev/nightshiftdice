import json
import os

from dataclasses import dataclass, field
from typing import Dict

from .helper_class import HelperClass


@dataclass
class Bar:
    name: str
    max_value: int = field()
    current: int = field(default=0)

    def __post_init__(self):
        self.current = int(self.current)
        self.max_value = int(self.max_value)
        if self.current > self.max_value:
            self.current = self.max_value

    def __str__(self):
        parts = min(50, self.max_value)
        filled = self.current
        if parts == 50:
            filled = int(filled / self.max_value * parts)
        return f'{"█" * filled}{"▒" * (parts - filled)} ({self.current}/{self.max_value})'

    def inc(self):
        self.current += 1
        if self.current > self.max_value:
            self.current = self.max_value

    def dec(self):
        self.current -= 1
        if self.current < 0:
            self.current = 0

    def to_json(self):
        return {'name': self.name, 'current': self.current, 'max_value': self.max_value}

    @classmethod
    def from_json(cls, data):
        return cls(name=data['name'], current=data['current'], max_value=data['max_value'])


class Progress(HelperClass):
    __cmd_macro__ = '/prog(?:ress)?'
    bars: Dict[str, Bar]

    def retrieve(self) -> None:
        if not os.path.exists('progress.json'):
            self.bars = {}
            self.save()
        with open('progress.json', 'r') as f:
            data = json.load(f)
        self.bars = {k: Bar.from_json(v) for k, v in data.items()}

    def save(self):
        with open('progress.json', 'w') as f:
            json.dump({k: v.to_json() for k, v in self.bars.items()}, f)

    def add(self, name: str, max_value: str) -> str:
        self.bars[name] = Bar(name, max_value)
        self.save()
        return f'Progress tracker `{name}` added with {max_value} steps'

    def show(self, name: str) -> str:
        return f'**{name}**:\n```{self.bars[name]}```'

    def up(self, name: str, val: str = '1') -> str:
        for _ in range(int(val)):
            self.bars[name].inc()
        self.save()
        return f'**{name}**:\n```{self.bars[name]}```'

    def down(self, name: str, val: str = '1') -> str:
        for _ in range(int(val)):
            self.bars[name].dec()
        self.save()
        return f'**{name}**:\n```{self.bars[name]}```'

    def reset(self, name: str) -> str:
        self.bars[name].current = 0
        self.save()
        return f'**{name}** reset to 0'

    def rm(self, name: str) -> str:
        del self.bars[name]
        self.save()
        return f'**{name}** removed'

    def list(self) -> str:
        if not self.bars:
            return 'No progress trackers'
        return '\n'.join([f'**{k}**: {v.current}/{v.max_value}' for k, v in self.bars.items()])

    async def cmd(self) -> None:
        self.retrieve()
        if self.cmd_str == 'help':
            await self._say("""**Progress Controls**
```
/prog[ress] add <name> #     Add a new progress tracker with X steps
/prog[ress] show <name>      Show the current progress of the tracker
/prog[ress] up <name>[ #]    Move the tracker forward one step
/prog[ress] down <name>[ #]  Move the tracker back one step
/prog[ress] reset <name>     Reset the tracker to 0
/prog[ress] rm <name>        Remove the tracker entirely
/prog[ress] list             List all progress trackers
```""")
            return
        cmd, *args = self.cmd_str.split(' ')
        try:
            msg = getattr(self, cmd)(*args)
        except AttributeError:
            msg = f'Invalid progress command `{cmd}`'
        except KeyError:
            msg = f'Progress tracker `{args[0]}` not found'
        except TypeError:
            msg = f'Invalid arguments for `{cmd}`: `{args}`'
        await self._say(msg)
