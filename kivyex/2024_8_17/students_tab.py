from typing import Literal, TypedDict, Tuple, List, cast

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.properties import (
    ListProperty,
    NumericProperty,
    StringProperty,
    ObjectProperty,
    AliasProperty)

from .... import get_students_with_class_info
from ....student import Student
from ....klass import Class
from ..util import load_layout
from ..behaviors import BackgroundColorBehavior, BorderBehavior
from .common import MGridLayout, MBoxLayout

load_layout(__file__)

class RowDict(TypedDict):
    id: int
    first_name: str
    last_name: str
    klass: str

def _return_true(*_args, **_kwargs) -> Literal[True]:
    return True

def _to_row_dict(t: Tuple[Student, Class]) -> RowDict:
    student, klass = t
    return RowDict({
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "klass": f"{klass.year} {klass.group}"
    })

def _get_students_fr(self) -> List[RowDict]:
    from ..app import ServiceApp
    app = cast(ServiceApp, App.get_running_app())
    storage = app.service.storage
    return list(map(_to_row_dict, get_students_with_class_info(storage)))

def _get_students(self) -> List[RowDict]:
    from ..app import ServiceApp
    app = cast(ServiceApp, App.get_running_app())
    if app.demo:
        return [
            RowDict(
                id=(i * 10 + j),
                first_name=f"{chr(ord('A') + i)}{chr(ord('A') + j)}",
                last_name=f"{chr(ord('A') + 5 + i)}{chr(ord('A') + 5 + j)}",
                klass=f"{10 + j // 7} {chr(ord('A') + (j % 5))}")
            for i in reversed(range(1, 2))
            for j in reversed(range(1, 10))]
    else:
        return _get_students_fr(self)

class StudentsTab(Screen):
    students = AliasProperty(_get_students, _return_true)
    table_grid = ObjectProperty()

    def __init__(self, *args, **kwargs) -> None:
        super(StudentsTab, self).__init__(*args, **kwargs)

        def make_table_grid(self, *_args):
            self.table_grid.clear_widgets()
            for s in self.students:
                print(f"{s=}")
                row = StudentsTableRow()
                row.id = s["id"]
                row.first_name = s["first_name"]
                row.last_name = s["last_name"]
                row.klass = s["klass"]
                self.table_grid.add_widget(row)

        self.bind(students=make_table_grid)
        make_table_grid(self)

class StudentsTableRow(MBoxLayout):
    id = NumericProperty()
    first_name = StringProperty()
    last_name = StringProperty()
    klass = StringProperty()

class StudentsRecycleGrid(
    BackgroundColorBehavior,
    BorderBehavior,
    RecycleGridLayout
):
    pass
