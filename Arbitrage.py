from itertools import permutations

liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def augment_liquidity( liquidity ):
    import copy
    new_dict = copy.deepcopy(liquidity)
    for k, v in liquidity.items():
        # print(k, v)
        new_dict[tuple(reversed(k))] = tuple(reversed(v))
    return new_dict

def input_path_2_tuple_path( input_path, liq ):
    tuple_path = []
    if type( input_path ) is not (list or tuple):
        raise Exception('Not Implemented.')
    for i in range( 1, len(input_path) ):
        tuple_path.append( liq[(input_path[i], input_path[i - 1])] )
    return tuple_path

def calculate_swap_amounts(initial_amount, liquidity_paths):
    fee_multiplier = 997 / 1000
    # Account for the 0.3% fee in swaps.
    current_amount = initial_amount

    # Process each swap in the sequence
    for R_out, R_in in liquidity_paths:
        old_amount = current_amount
        current_amount = (fee_multiplier * current_amount * R_out) / (R_in + fee_multiplier * current_amount)
        print(f'old_amount: {old_amount}')
        print(f'current_amount: {current_amount}')

    return current_amount


# Define the liquidity for each step in the swap path
# Note: These values are taken directly from your liquidity pool data. Adjust them as needed.
# liquidity_paths = [
#     (17, 10),  # tokenB -> tokenA (R_out_tokenA, R_in_tokenB)
#     (9, 15),   # tokenA -> tokenD (R_out_tokenD, R_in_tokenA)
#     (13, 6)    # tokenD -> tokenB (R_out_tokenB, R_in_tokenD)
# ]


if __name__ == '__main__':
    new_liq = augment_liquidity(liquidity)

    # input_path_list = []
    # for i in range( 1, 4 + 1 ):
    #     input_path_list += permutations(['tokenA', 'tokenC', 'tokenD', 'tokenE'], i)
    # # input_path_list = permutations(['tokenA', 'tokenC', 'tokenD', 'tokenE'])
    

    # max_profit = -1
    # path = None

    # for _input_path in input_path_list:

    #     input_path = ['tokenB'] + list(_input_path) + ['tokenB']


    #     new_path = input_path_2_tuple_path(input_path, new_liq)
    #     print(new_path)

    #     # Initial amount start the swaps.
    #     initial_amount = 5

    #     # Calculate the final amount of tokenB after the swaps
    #     final_amount = calculate_swap_amounts(initial_amount, new_path)
    #     print(f'path: {"->".join(input_path)}')
    #     print(f"Final amount of tokenB received: {final_amount}")

    #     if final_amount > max_profit:
    #         path = input_path
    #         max_profit = final_amount

    print('*' * 50)

    path = ['tokenB', 'tokenA', 'tokenD', 'tokenB']

    print(path)
    # print(max_profit)
    profit = calculate_swap_amounts(5, input_path_2_tuple_path(path, new_liq))
    print(f'final_profit: {profit}')
