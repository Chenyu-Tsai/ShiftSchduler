import csv
import argparse
from identity import StaffInfoProcessor
import random
import calendar
import numpy as np
import pandas as pd
from utils import handle_duty_but_not_count, handle_designated_on, to_min_opt, to_min_rank12, to_min_rank1, to_max_shift, fill_rest_shift,to_min_shift

def generate_day_shift(args, staffs, day, max_shift):
    # sort the staffs by duty_days
    arrange_priority = []
    for (i, staff) in enumerate(staffs):
        arrange_priority.append((i, staff.duty_days))
    arrange_priority = sorted(arrange_priority, key=lambda arrange_priority: arrange_priority[1], reverse=False)
    arrange_priority = [arrange_priority[i][0] for i in range(len(arrange_priority))]
    if day[0] == 1:
        random.shuffle(arrange_priority)

    # If there is a PT, use this to randomize the PTs shift
    # pop_pt = random.randint(0, 1)
    # if pop_pt == 1:
    #     arrange_priority.remove(len(staffs)-1)
    #     staffs[-1].yesterday_off = 1

    # check if weekend
    weekend = False if day[1] != 1 else True
    #max_shift = 14 if weekend or args.national_holiday is not None else 8
    max_shift = max_shift
    min_shift = 9 if weekend or args.national_holiday is not None else 6
    opt_min = 4 if weekend or args.national_holiday is not None else 3
    rank1_min = 1
    rank12_min = 3
    arrange_priority, shifts = handle_duty_but_not_count(arrange_priority, staffs, day)
    arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num = handle_designated_on(arrange_priority, staffs, day, shifts)
    arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num = to_min_rank1(arrange_priority, staffs, day, shifts, person_num, opt_num, rank1_num, rank12_num, opt_min, min_shift)
    arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num = to_min_rank12(arrange_priority, staffs, day, shifts, person_num, opt_num, rank1_num, rank12_num, opt_min, min_shift)
    arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num = to_min_opt(arrange_priority, staffs, day, shifts, person_num, opt_num, rank1_num, rank12_num, opt_min, min_shift)
    arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num = to_min_shift(arrange_priority, staffs, day, shifts, person_num, opt_num, rank1_num, rank12_num, opt_min, min_shift)
    arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num = to_max_shift(arrange_priority, staffs, day, shifts, person_num, opt_num, rank1_num, rank12_num, opt_min, max_shift)
    #arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num = fill_rest_shift(arrange_priority, staffs, day, shifts, person_num, opt_num, rank1_num, rank12_num, opt_min, max_shift)   

    for i in arrange_priority:
        staffs[i].yesterday_off = 1
        staffs[i].serial_day = 0

    day_detail = []
    day_detail.append([max_shift, person_num, opt_num, rank1_num, rank12_num])
    #print(max_shift, person_num, opt_num, rank1_num, rank12_num)

    return shifts, day_detail

def get_date_info(args, total_shifts):
    cal = calendar.Calendar()
    total_days = calendar.monthrange(args.year, args.month)[1]
    month = cal.itermonthdays2(args.year, args.month)
    day_and_week = [date+1 for date in range(total_days)]
    day_infos = []
    # for assigned day as holiday shift
    assigned_date = [1, 2, 9]

    for day in month:
        if day[0] in day_and_week:
            date = day[0]
            weekend = 0 if day[1] != 5 and day[1] != 6 else 1
            """
            Handle assigned holiday
            """
            if date in assigned_date:
                weekend = 1
            else:
                pass
            day_infos.append((date, weekend))

    day_infos_with_shift = []
    total_shift = total_shifts
    for day in day_infos:
        if day[1] == 0:
            num = args.day_min_num
        else:
            num = args.end_min_num
        day_infos_with_shift.append((day[0], day[1], num))
    # for day in day_infos:
    #     num = 0
    #     if day[1] == 0:
    #         if total_shift >= args.day_max_num:
    #             num = random.randint(args.day_min_num, args.day_max_num)
    #             total_shift -= num
    #         else:
    #             num = total_shift
    #             total_shift -= num
    #     elif day[1] == 1:
    #         if total_shift >= args.end_max_num:
    #             num = random.randint(args.end_min_num, args.end_max_num)
    #             total_shift -= num
    #         else:
    #             num = total_shifts
    #             total_shift -= num
    #     day_infos_with_shift.append((day[0], day[1], num))
    # diff = sum([i[2] for i in day_infos_with_shift])
    # new_day_infos_with_shift = []

    # for day_info in day_infos_with_shift:
    #     new_day_infos_with_shift.append(day_info)
    #     if diff == total_shifts:
    #         continue
    #     date = day_info[0]
    #     weekend = day_info[1]
    #     if weekend == 0 and day_info[2] < args.day_max_num:
    #         shift = day_info[2] + 1
    #         new_day_infos_with_shift.pop()
    #         new_day_infos_with_shift.append((date, weekend, shift))
    #         diff += 1
    #     elif weekend == 1 and day_info[2] < args.end_max_num:
    #         if day_info[2] <= args.end_max_num-3:
    #             shift = day_info[2] +2
    #             new_day_infos_with_shift.pop()
    #             new_day_infos_with_shift.append((date, weekend, shift))
    #             diff += 2
    #         else:
    #             shift = day_info[2] + 1
    #             new_day_infos_with_shift.pop()
    #             new_day_infos_with_shift.append((date, weekend, shift))
    #             diff += 1
    #     else:
    #         pass
    
    return day_infos_with_shift
        

def get_staff_info(args):
    processor = StaffInfoProcessor()
    infos = processor.get_staff_info(file_name=args.file_name)

    return infos

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--file_name", default='shift.csv', type=str)
    parser.add_argument("--national_holiday", type=int)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, required=True)
    parser.add_argument("--day_min_num", type=int, default=6)
    parser.add_argument("--day_max_num", type=int, default=8)
    parser.add_argument("--end_min_num", type=int, default=11)
    parser.add_argument("--end_max_num", type=int, default=12)

    args = parser.parse_args()
    staff_infos = get_staff_info(args)
    total_shifts = sum([i.max_duty_days for i in staff_infos])
    duty_not_count = sum([len(i.on_duty_but_not_count) for i in staff_infos if len(i.on_duty_but_not_count) != 1])
    total_shifts = total_shifts - duty_not_count
    #print(total_shifts)

    day_infos = get_date_info(args, total_shifts)
    arrange_shift = sum([day[2] for day in day_infos])
    #print(arrange_shift)

    shifts = []
    day_details = []
    check = []
    for day_info in day_infos:
        day = (day_info[0], day_info[1])
        max_shift = day_info[2]
        day, day_detail = generate_day_shift(args, staff_infos, day=day, max_shift=max_shift)
        shifts.append(day)
        day_details.append(day_detail)
        check.append(day_detail[0][0] == day_detail[0][1])
    
    shifts = np.array(shifts)
    shifts = shifts.transpose()
    df_shifts = pd.DataFrame(shifts, columns=[i + 1 for i in range(len(day_infos))], index=[i + 5 for i in range(len(staff_infos))])

    day_details = np.array(day_details)
    day_details = day_details.squeeze()
    day_details = day_details.transpose()
    df_day_details = pd.DataFrame(day_details, columns=[i + 1 for i in range(len(day_infos))], index=[i for i in range(5)] )
    df_shift_infos = pd.concat([df_day_details, df_shifts], axis=0)
    

    staff_duty_days = ([''] * 5) + [staff.duty_days for staff in staff_infos]
    staff_max_duty_days = ([''] * 5) +  [staff.max_duty_days for staff in staff_infos]
    duty_infos = []
    duty_infos.append(staff_duty_days)
    duty_infos.append(staff_max_duty_days)
    duty_infos = np.array(duty_infos).transpose()
    df_duty_infos = pd.DataFrame(duty_infos, columns=['Actual', 'Expected'])
    
    staff_name = [staff.name for staff in staff_infos]
    info_col = ['Expecte1d', 'Actual', 'Opt', 'RankA', 'RankA&B'] + staff_name
    df_info_col = pd.DataFrame(info_col, columns=['Name'])
    
    df_info_col = pd.concat([df_info_col, df_duty_infos], axis=1)
    final_df = pd.concat([df_info_col, df_shift_infos], axis=1)
    final_df.to_csv('Shift_Result.csv', encoding="utf-8-sig", index=False)
    #check = [staff.duty_days == staff.max_duty_days for staff in staff_infos]
    final_check = True if False not in check else False

    return final_df, final_check 
if __name__ == "__main__":
    # df.to_csv('Shift_Result.csv', encoding="utf-8-sig", index=False)

    # while True:
    #     df, check = main()
    #     if check == True:
    #         df.to_csv('Shift_Result.csv', encoding="utf-8-sig", index=False)
    #         break
    #     else:
    #         pass
    main()

# python3 main.py --year 2020 --month 6