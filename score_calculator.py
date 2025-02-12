from data import combat_options_score, combat_options_extra_score

def calculate_score(selected_options, quantity, collection, recruit_4star, recruit_5star, recruit_6star, 
                    starting_balance, ending_balance, remaining_withdrawal, settlement_score, chaos_status, 
                    emergency_status):
    total_score = 0
    
    for option in selected_options:
        base_score = combat_options_score.get(option, 0)
        
        if option in chaos_status:
            if "混乱" in chaos_status[option]:
                base_score += 50
            
            if "滚动先祖" in chaos_status[option] or "终结的实相" in chaos_status[option]:
                base_score += 150

        if option in emergency_status:
            if emergency_status[option] == "紧急无漏":
                if option == "信号灯":
                    base_score += 20
                elif option == "劫虚济实":
                    base_score += 30
                elif option == "鸭速公路":
                    base_score += 50
                elif option == "玩具的报复":
                    base_score += 20
            elif emergency_status[option] == "普通无漏":
                if option == "鸭速公路":
                    base_score += 30


        total_score += base_score
    
    total_score += int(quantity) * 20
    
    total_score += len(collection) * 10 if collection else 0
    
    total_score += int(recruit_4star) * 10 if recruit_4star else 0
    total_score += int(recruit_5star) * 20 if recruit_5star else 0
    total_score += int(recruit_6star) * 50 if recruit_6star else 0
    
    if starting_balance and ending_balance and remaining_withdrawal:
        withdrawal_difference = abs(int(starting_balance) - int(ending_balance))
        remaining_withdrawal = int(remaining_withdrawal)
        
        if withdrawal_difference > remaining_withdrawal:
            excess = withdrawal_difference - remaining_withdrawal
            total_score -= (excess // 1) * 50

    total_score += int(settlement_score) if settlement_score else 0

    return total_score
