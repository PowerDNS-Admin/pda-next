from app.model.mutables import Mutable


class Task(Mutable):
    """A class representing a monitored task."""

    id: str or None = None
    _name: str or None = None
    result: bool or None = None

    @property
    def name(self) -> str:
        """The name of the task."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name of the task."""
        self._name = value

    def to_dict(self) -> dict:
        """Convert the task to a JSON-serializable dict."""
        return {
            'id': self.id,
            'name': self.name,
            'result': self.result,
        }

    def __str__(self):
        return f'id: {self.id}; name: {self.name};'

    def __repr__(self):
        return self.__str__()


class TaskGroup(Mutable):
    """A class representing groups of executed tasks."""

    _name: str or None = None
    """The name of the operation of the task group."""

    _tasks: list[Task] or None = None
    """A list of tasks monitored by the task group."""

    complete: bool = False
    """Whether or not the task group is complete."""

    success: bool or None = None
    """Whether or not the task group was completely successful."""

    @property
    def name(self) -> str:
        """The name of the operation of the task group."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name of the operation of the task group."""
        self._name = value

    @property
    def tasks(self) -> list[Task]:
        """A list of tasks monitored by the task group."""
        return self._tasks

    @tasks.setter
    def tasks(self, value: list[Task or dict]):
        tasks: list[Task] = []

        for task in value:
            if isinstance(task, Task):
                tasks.append(task)
            elif isinstance(task, dict):
                tasks.append(Task(**task))
            else:
                raise TypeError(f'Expected Task or dict; got {type(task)}')

        self._tasks = tasks

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'tasks' not in kwargs:
            self._tasks = []

    def __str__(self):
        return f'name: {self.name}; tasks: {self.tasks};'

    def __repr__(self):
        return self.__str__()

    def to_dict(self) -> dict:
        """Convert the task group to a JSON-serializable dict."""
        return {
            'name': self.name,
            'tasks': [task.to_dict() for task in self.tasks],
            'complete': self.complete,
            'success': self.success,
        }

    def get_task_by_id(self, task_id: str) -> Task or None:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task

        return None

    def get_task_by_name(self, task_name: str) -> Task or None:
        """Get a task by name."""
        for task in self.tasks:
            if task.name == task_name:
                return task

        return None

    def create_task(self, name: str, task_id: str):
        self._tasks.append(Task(name=name, id=task_id))
