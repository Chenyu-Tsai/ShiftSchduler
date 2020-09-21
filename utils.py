def handle_duty_but_not_count(arrange_priority, staffs, day):
    shifts = ['OFF'] * len(staffs)
    remove_lst = []

    for i in arrange_priority:
        if day[0] in staffs[i].on_duty_but_not_count:
            shifts[i] = 2
            staffs[i].serial_day += 1
            staffs[i].duty_days += 1
            staffs[i].yesterday_off = 0
            remove_lst.append(i)

    for i in remove_lst:
        arrange_priority.remove(i)

    return arrange_priority, shifts

def handle_designated_on(arrange_priority, staffs, day, shifts):
    person_num = 0
    opt_num = 0
    rank1_num = 0
    rank12_num = 0
    remove_lst = []


    for i in arrange_priority:
        if day[0] in staffs[i].designated_on:
            shifts[i] = 1
            staffs[i].serial_day += 1
            staffs[i].duty_days += 1
            staffs[i].yesterday_off = 0
            person_num += 1
            # track staff identity
            if staffs[i].identity == 1:
                rank1_num += 1
                rank12_num += 1
            elif staffs[i].identity == 2:
                rank12_num += 1
            else:
                pass
            # track the is_opt staff
            if staffs[i].is_opt == 1:
                opt_num += 1
            remove_lst.append(i)
            
    for i in remove_lst:
        arrange_priority.remove(i)

    return arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num

def to_min_rank1(
    arrange_priority,
    staffs,
    day, 
    shifts, 
    person_num, 
    opt_num, 
    rank1_num, 
    rank12_num,
    opt_min,
    min_shift,
):
    remove_lst = []
    # check serial day
    for i in arrange_priority:
        # if staffs[i].yesterday_off == 1:
        #     staffs[i].serial_day = 0
        if staffs[i].yesterday_off == 0 and staffs[i].serial_day >= 4:
            staffs[i].serial_day = 0
            remove_lst.append(i)
        else:
            pass
    for i in arrange_priority:
        if staffs[i].duty_days >= staffs[i].max_duty_days:
            remove_lst.append(i)
        else:
            pass

    for i in arrange_priority:
        if day[0] in staffs[i].designated_off or day[0] in staffs[i].annual_leave:
            remove_lst.append(i)
        else:
            pass
    remove_lst = set(remove_lst)

    for i in remove_lst:
        arrange_priority.remove(i)

    remove_lst = []

    if rank1_num < 1:
        for i in arrange_priority:
            if rank1_num >= 1:
                break

            if staffs[i].identity == 1:
                shifts[i] = 1
                staffs[i].serial_day += 1
                staffs[i].duty_days += 1
                staffs[i].yesterday_off = 0
                person_num += 1
                rank1_num += 1
                rank12_num += 1
                if staffs[i].is_opt == 1:
                    opt_num += 1
                else:
                    pass
                remove_lst.append(i)
    else:
        pass
    for i in remove_lst:
        arrange_priority.remove(i)

    return arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num

def to_min_rank12(
    arrange_priority,
    staffs,
    day, 
    shifts, 
    person_num, 
    opt_num, 
    rank1_num, 
    rank12_num,
    opt_min,
    min_shift,
):
    remove_lst = []

    if rank12_num < 3:
        for i in arrange_priority:
            if rank12_num >= 3:
                break

            if staffs[i].identity == 1 or staffs[i].identity == 2:
                shifts[i] = 1
                staffs[i].serial_day += 1
                staffs[i].duty_days += 1
                staffs[i].yesterday_off = 0
                person_num += 1
                if staffs[i].identity == 1:
                    rank1_num += 1
                    rank12_num += 1
                else:
                    rank12_num += 1
                if staffs[i].is_opt == 1:
                    opt_num += 1
                else:
                    pass

                remove_lst.append(i)
    else:
        pass

    for i in remove_lst:
        arrange_priority.remove(i)

    return arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num



def to_min_opt(
    arrange_priority,
    staffs,
    day, 
    shifts, 
    person_num, 
    opt_num, 
    rank1_num, 
    rank12_num,
    opt_min,
    min_shift,
):
    remove_lst = []

    if opt_num < opt_min:
        for i in arrange_priority:
            if opt_num >= opt_min:
                break

            if staffs[i].is_opt == 1 and staffs[i].identity != 1:
                shifts[i] = 1
                staffs[i].serial_day += 1
                staffs[i].duty_days += 1
                staffs[i].yesterday_off = 0
                person_num += 1
                opt_num += 1
                # track staff identity
                if staffs[i].identity == 1:
                    rank1_num += 1
                    rank12_num += 1
                elif staffs[i].identity == 2:
                    rank12_num += 1
                else:
                    pass
                remove_lst.append(i)
    for i in remove_lst:
        arrange_priority.remove(i)
    return arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num
            

def to_min_shift(
    arrange_priority,
    staffs,
    day, 
    shifts, 
    person_num, 
    opt_num, 
    rank1_num, 
    rank12_num,
    opt_min,
    min_shift,
    ):

    rank1_min = 1
    rank12_min = 3
    remove_lst = []

    if person_num < min_shift:
        for i in arrange_priority:
            if person_num == min_shift:
                break

            if opt_num >= opt_min and staffs[i].is_opt == 1:
                remove_lst.append(i)
        
            if rank1_num >= 1:
                if staffs[i].identity == 1:
                    continue
            if rank1_num >= 1 or rank12_num >= 3:
                if staffs[i].identity == 1 or staffs[i].identity == 2:
                    continue
            if opt_num >= opt_min:
                if staffs[i].is_opt == 1:
                    continue

            if rank1_num >= rank1_min or rank12_num >= rank12_min:
                if opt_num <= opt_min:
                    if staffs[i].is_opt == 1:
                        pass
                    elif staffs[i].identity in [1, 2]:
                        continue
                    else:
                        pass
                elif opt_num >= opt_min:
                    if staffs[i].is_opt == 1:
                        continue
                    elif staffs[i].identity in [1, 2]:
                        continue
                    else:
                        pass
                else:
                    pass
            else:
                pass
            shifts[i] = 1
            staffs[i].serial_day += 1
            staffs[i].duty_days += 1
            staffs[i].yesterday_off = 0
            person_num += 1
            # track staff identity
            if staffs[i].identity == 1:
                rank1_num += 1
                rank12_num += 1
            elif staffs[i].identity == 2:
                rank12_num += 1
            else:
                pass
            # track the is_opt staff
            if staffs[i].is_opt == 1:
                opt_num += 1
            remove_lst.append(i)
    for i in remove_lst:
        arrange_priority.remove(i)
    
    return arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num

def to_max_shift(
    arrange_priority,
    staffs,
    day, 
    shifts, 
    person_num, 
    opt_num, 
    rank1_num, 
    rank12_num,
    opt_min,
    max_shift,
    ):
    remove_lst = []
    for i in arrange_priority:
        if person_num >= max_shift:
            break

        if rank1_num >= 1:
            if staffs[i].identity == 1:
                continue
        if rank1_num >= 1 or rank12_num >= 3:
            if staffs[i].identity == 1 or staffs[i].identity == 2:
                continue
        if opt_num >= opt_min:
            if staffs[i].is_opt == 1:
                continue

        shifts[i] = 1
        staffs[i].serial_day += 1
        staffs[i].duty_days += 1
        staffs[i].yesterday_off = 0
        person_num += 1
        # track staff identity
        if staffs[i].identity == 1:
            rank1_num += 1
            rank12_num += 1
        elif staffs[i].identity == 2:
            rank12_num += 1
        else:
            pass
        # track the is_opt staff
        if staffs[i].is_opt == 1:
            opt_num += 1
        remove_lst.append(i)
    
    for i in remove_lst:
        arrange_priority.remove(i)
    
    return arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num

def fill_rest_shift(
    arrange_priority,
    staffs,
    day, 
    shifts, 
    person_num, 
    opt_num, 
    rank1_num, 
    rank12_num,
    opt_min,
    max_shift,
):
    remove_lst = []

    for i in arrange_priority:
        if person_num >= max_shift:
            break
        if staffs[i].serial_day < 4:
            if staffs[i].identity == 1 or staffs[i].identity == 2:
                continue
            shifts[i] = 1
            staffs[i].serial_day += 1
            staffs[i].duty_days += 1
            staffs[i].yesterday_off = 0
            person_num += 1
            # track staff identity
            if staffs[i].identity == 1:
                rank1_num += 1
                rank12_num += 1
            elif staffs[i].identity == 2:
                rank12_num += 1
            else:
                pass
            # track the is_opt staff
            if staffs[i].is_opt == 1:
                opt_num += 1
            remove_lst.append(i)
    for i in remove_lst:
        arrange_priority.remove(i)
        
    remove_lst = []
    if person_num < max_shift:
        for i in arrange_priority:
            if person_num >= max_shift:
                break
            shifts[i] = 1
            staffs[i].serial_day += 1
            staffs[i].duty_days += 1
            staffs[i].yesterday_off = 0
            person_num += 1
            # track staff identity
            if staffs[i].identity == 1:
                rank1_num += 1
                rank12_num += 1
            elif staffs[i].identity == 2:
                rank12_num += 1
            else:
                pass
            # track the is_opt staff
            if staffs[i].is_opt == 1:
                opt_num += 1
            remove_lst.append(i)

    for i in remove_lst:
        arrange_priority.remove(i)
    
    return arrange_priority, shifts, person_num, opt_num, rank1_num, rank12_num
        
    