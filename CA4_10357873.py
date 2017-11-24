#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 11:41:12 2017

@author: ciaran
"""

import pandas as pd
import numpy as np
import linecache
import datetime

#function to count the number of lines in the file
def count_lines_in_datafile(changes_file):
    #count the number of lines in the data file
    infile = open(changes_file)
    z = 0
    for line in infile:
        z = z + 1
    linecount = z
    return linecount
    
#function to create a dataframe with all the data required for ananlysis  
def create_data_frame(changes_file,linecount):
    #initialise variables. i will keep a record of current line number
    i = 0
    
    #define the column names in the dataframe
    columns = ("commit block", "user", "timestamp", "added", "deleted", "modified", "comment")
    
    #create the dataframe
    df = pd.DataFrame(columns=columns)
    infile = open(changes_file)
    #outer loop that searches through the file for matching pattern 20*'-' and starts inner loop each time it finds one
    for line in infile:
        
        i = i + 1
        linetest = line
        #loop that will run each time the pattern is matched
        if linetest[0:20] == "--------------------":
            test = "TRUE" 
            #j will count the number of lines in each commit section
            j = 1
            #loop to set j to the number of lines between one set of ---- and the next set of -----
            while test == "TRUE" and (i + j) < linecount:
                
                linetest_i = linecache.getline(changes_file, i + j)  
                if linetest_i[0:20] == "--------------------":
                    test = "FALSE"

                else:
                    test = "TRUE"
                    j = j + 1  
                    
            #loop that runs for each of the lines in each commit section, until the end of the file
            if i < (linecount - 1):
                #retrieve the line after the ------, which will have the 'commit block', 'user' &'timestamp' info
                data_line = linecache.getline(changes_file, i + 1)
                #split the line based on the '|'
                data = data_line.split("|")
                data0 =  data[0]
                data1 = data[1]
                data2 = data[2]
                #strip the unnecessary info from the time string
                date = data2[1:20]
                #convert the date string date to a time
                date_converted = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                
                #initialise variables
                f = i
                g = 3
                A = 0
                D = 0
                M = 0
                #loop that runs on the commit lines to count the number of added, modified and delete elements
                for f in range((i + 3),(i+j)):

                    data_line_2 = linecache.getline(changes_file, i + g)
                    #runs until it reaches a blank line
                    if len(data_line_2) > 1:
                        if data_line_2[3] == "A":
                            A = A + 1
                        elif data_line_2[3] == "M":
                            M = M + 1
                        elif data_line_2[3] == "D":
                            D = D + 1
                        f = f + 1
                        g = g + 1   
                    else:
                        #once it hits a blank line, store the comment section in a variable and break from this loop
                        comment_line = linecache.getline(changes_file, f + 1).rstrip()
                        break
                #define the line that will be added to the dataframe
                data  = [data0.strip(), data1.strip(), date_converted, A, D, M, comment_line]
                #append the line to the dataframe
                df.loc[len(df)] = data
        else:         
            continue
    
    return df

def investigate_data(df):
    #print the dataframe to a file for further analysis
    df.to_csv('dataframe_for_analysis.csv')
     
    #create pivot based on count of 'adds', 'deletes' and 'modifications' per user       
    pivot1 = pd.pivot_table(df,index='user',values=['added','deleted','modified'],aggfunc=np.sum,margins=True)
    print pivot1
    
    #create pivot based on percentages of 'additions' by user
    pivot2 = pd.pivot_table(df,index='user',values=['added'],aggfunc=np.sum,margins=True).div(sum(df.added)).mul(100)
    print pivot2
    
    #create pivot based on percentages of 'modifications' by user
    pivot3 = pd.pivot_table(df,index='user',values=['modified'],aggfunc=np.sum,margins=True).div(sum(df.modified)).mul(100)
    print pivot3
    
    #create pivot based on percentages of 'deletions' by user
    pivot4 = pd.pivot_table(df,index='user',values=['deleted'],aggfunc=np.sum,margins=True).div(sum(df.deleted)).mul(100)
    print pivot4
    
    #create dataframe of just 'timestamp' and 'addition' counts
    d = {'timestamp' :df['timestamp'], 'added':df['added']}
    df2 = pd.DataFrame(d)
    #plot a graph of 'additions' over time
    df2.plot(x = 'timestamp', y = 'added', title = '"Added" count over time')
    

    #create dataframe of just 'timestamp' and 'deletions' counts
    d = {'timestamp' :df['timestamp'], 'deleted':df['deleted']}
    df2 = pd.DataFrame(d)
    #plot a graph of 'deletions' over time
    df2.plot(x = 'timestamp', y = 'deleted', title = '"Deleted" count over time')
    
    #create dataframe of just 'timestamp' and 'modifications' counts
    d = {'timestamp' :df['timestamp'], 'modified':df['modified']}
    df2 = pd.DataFrame(d)
    #plot a graph of 'modifications' over time
    df2.plot(x = 'timestamp', y = 'modified', title = '"Modified" count over time')

     #create pivot based on count of 'adds', 'deletes' and 'modifications' per month       
    df['timestamp']=pd.to_datetime(df['timestamp'], format ='%Y-%m-%d %H:%M:%S').dt.to_period('M')
    pivot1 = pd.pivot_table(df,index='timestamp',values=['added','deleted','modified'],aggfunc=np.sum,margins=True)
    print pivot1
    #create a pivot without totals to see a stacked bar chart of the results
    pivot2 = pd.pivot_table(df,index='timestamp',values=['added','deleted','modified'],aggfunc=np.sum)
    pivot2.plot.bar(stacked=True)

if __name__ == '__main__':
    
    #rdefine the file to be read in
    changes_file = 'changes_python.txt'
    #count the number of lines in the file
    linecount = count_lines_in_datafile(changes_file)
    #create the dataframe with all the required data
    df = create_data_frame(changes_file,linecount)
    #output some data analysis
    investigate_data(df)


