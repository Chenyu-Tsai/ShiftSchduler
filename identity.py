from dataclasses import dataclass, field
from typing import List, Optional
import os
import csv

@dataclass
class StaffInfo():
    name: str
    designated_off: List[str]
    designated_on: List[str]
    max_duty_days: int
    on_duty_but_not_count: Optional[List[str]] = None

    yesterday_off: int = 1
    identity: int = 0
    is_opt: int = 0
    serial_day: int = 0
    duty_days: int = 0
    annual_leave: int = 0

class DataProcessor:

    @classmethod
    def _load_staff_info(cls, file_name):
        with open(file_name, "r", encoding="utf-8-sig") as f:
            return list(csv.reader(f))

class StaffInfoProcessor(DataProcessor):
    def get_staff_info(self, file_name):
        lines = self._load_staff_info(file_name)
        infos = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            name = line[0]
            identity = int(line[1])
            is_opt = int(line[2])

            designated_off = line[3].split(',')
            if designated_off != ['']:
                designated_off = [int(i) for i in designated_off]

            designated_on = line[4].split(',')
            if designated_on != ['']:
                designated_on = [int(i) for i in designated_on]

            on_duty_but_not_count = line[5].split(',')
            if on_duty_but_not_count != ['']:
                on_duty_but_not_count = [int(i) for i in on_duty_but_not_count]

            annual_leave = line[6].split(',')
            if annual_leave != ['']:
                annual_leave = [int(i) for i in annual_leave]
            max_shift = 22 if identity != 4 else 10
            # max_duty_days = max_shift - (0 if len(annual_leave) <= 3 else (len(annual_leave) - 3)) \
            #             if identity != 4 else max_shift - (0 if len(annual_leave) <= 3 else (len(annual_leave) - 3))
            max_duty_days = max_shift - (0 if annual_leave == [''] else len(annual_leave))
            infos.append(StaffInfo(name=name, 
                                   identity=identity, 
                                   is_opt=is_opt, 
                                   designated_off=designated_off, 
                                   designated_on=designated_on,
                                   on_duty_but_not_count=on_duty_but_not_count,
                                   annual_leave=annual_leave, 
                                   max_duty_days=max_duty_days,))
        return infos
            
