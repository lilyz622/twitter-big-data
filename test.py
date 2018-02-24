# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 15:34:18 2017

@author: blues

"""
#Group 4: Tian Lan & Xian Yang
#Project: Given a log file of Apple stock prices, calculate some simple statistics.


def main():        
    file_obj = get_input_descriptor()  
    if file_obj == -1:
        print('You enter too, try next time')
        return None
    column_number = int(input('Input colume number: ', ))
    v = get_data_list(file_obj, column_number)
    w = average_data(v)
    w.sort()
    print(' ')
    print('Lowest 6 for column', column_number)
    for i in range(6):
        date = list(w[i])[1]
        data = list(w[i])[0]
        print('Date:', date,', Value:{:6.2f}'.format(data))
    print(' ')
    print('Highest 6 for column', column_number)
    for j in range(-6, 0, 1):
        date = list(w[j])[1]
        data = list(w[j])[0]
        print('Date:', date,', Value:{:6.2f}'.format(data))
    file_obj.close()
    
    
def get_input_descriptor():
    file_input = ''
    count = 0
    while count < 5:
        file_input = input('Open what file: ', )
        if file_input != 'table.csv':
            count += 1
            print('Bad file name, try again (enter ',count, 'out of 5)')
            if count == 5:
                return -1
            continue
        else:
            infile = open('table.csv')
            return infile

  
def get_data_list(file_object, column_number):
    next(file_object)
    tuple_list = []
    for lines in file_object:
        line_date = lines.split(',')[0]
        line = lines.split(',')[column_number]
        Mytuple = line_date, line[:-1]
        tuple_list.append(Mytuple)
    return tuple_list

def average_data(list_of_tuples):
    sums = []
    months = []
    for m,t in list_of_tuples:
        temp = m.split('-')
        m = (temp[1]+'-'+temp[0])
        t = float(t)
        for i in range(len(months)):
            if months[i] == m:
                sums[i].append(t)
                break
        else:
            months.append(m)
            sums.append([t])
    i = 0
    month_list = []
    while i < len(months):
        average = sum(sums[i])/len(sums[i])
        month_tuple = average, months[i]
        month_list.append(month_tuple)
        i += 1
    return month_list 
    
    
main()



        
                
            
 
    



    

        







    


            

        

        
        
        

        
        
        
    