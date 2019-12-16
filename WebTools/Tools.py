def PrintTitle(function_name):
    
    border = '   [' + '#' * (len(function_name) + 10) + ']\n'
    middle = '   [##| [' + function_name + '] |##]\n'  
    
    print('\n' + border + middle + border)
    