import typing as t

import tabulate

from shemas import BaseShema


class PrintDictsLikeTableMixin:
    _dict_for_print: dict[str, list] = {}


    def print_as_table[Shema: BaseShema](self, *args: Shema) -> None:
        shemas_type = type(args[0])

        for arg in args:
            if not isinstance(arg, shemas_type):
                raise ValueError()
            
            self._append_shema_data(arg)
        
        tabulate.tabulate(self._dict_for_print)

    
    def _append_shema_data[Shema: BaseShema](self, shema: Shema) -> None:
        for key, value in shema.model_dump():
            if key not in self._dict_for_print:
                self._dict_for_print[key] = [value]
            else:
                self._dict_for_print[key].append(value)