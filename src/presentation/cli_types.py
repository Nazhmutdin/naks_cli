from pathlib import Path
from typing import Optional

from click import Context, Parameter
from click.types import ParamType


class OptionalPath(ParamType):
    name = "path"

    def convert(self, value: Optional[str], param: Optional[Parameter], ctx: Optional[Context]) -> Path | None:
        if value in [None, "None"]:
            return None
        
        path = Path(value)

        if not path.exists():
            self.fail(f"invalid path ({value})", param, ctx)

        return path
