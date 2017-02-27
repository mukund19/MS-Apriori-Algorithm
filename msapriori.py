import re
import numbers
import collections
from collections import defaultdict
import math
import itertools
import sys


def readInputFile(inputFile):
    with open(inputFile) as f:
        count_dictionary={}
        no_of_transactions =0
        transaction_list=[]
        for line in f:
            no_of_transactions=no_of_transactions+1;
            line = line.split()
            s=set()
            for l in line:
                number = re.findall('\d+', l)
                number1=int(''.join(number))
                s.add(number1)
                if number1 in count_dictionary:
                    count_dictionary[number1] +=1
                else:
                    count_dictionary[number1]=1
            transaction_list.append(s)
        return count_dictionary,no_of_transactions,transaction_list



def readParameterFile(parameterFile):
    with open(parameterFile) as f:
        mis_dictionary={}
        mis_dictionary_ordered=collections.OrderedDict()
        count =0
        sdc=0;
        must_have=[]
        cannot_be_together=defaultdict(list)
        list_of_lists=[]
        start="{"
        stop="}"

        for line in f:
                if "MIS" in line:
                    name, val = line.partition("=")[::2]
                    mis_dictionary[int(''.join(name[name.index("(")+1:name.index(")")]))] = float(val.strip())
                elif "SDC" in line:
                    name, val = line.partition("=")[::2]
                    sdc=float(val.strip())
                elif "must-have" in line:
                    name, val = line.partition(":")[::2]
                    for i in val.split("or"):
                        must_have.append(int(i.strip()))
                elif "cannot_be_together" in line:
                    val = line.split(":")[-1].strip()
                    val=''.join(val.split())
                    value=re.findall(r"\{([^}]+)\}", val)
                    for i in value:
                        list1=[]
                        for j in i.split(","):
                            list1.append(int(j))
                        list_of_lists.append(list1)
                    for i in range(len(list_of_lists)):
                        for j in range(len(list_of_lists[i])):
                            ele=list_of_lists[i][j]
                            k=0
                            list1=[]
                            while(k<len(list_of_lists[i])):
                                if(ele!=list_of_lists[i][k]):
                                    list1.append(list_of_lists[i][k])
                                k=k+1
                            cannot_be_together[ele].extend(list1)

        for w in (sorted(mis_dictionary.items(), key=lambda x: (x[1],x[0]), reverse=False)):
            mis_dictionary_ordered[w[0]] = w[1]
        return mis_dictionary_ordered,sdc,list_of_lists,must_have


"""This function generated level 1 candidates"""
def form_L(count_dictionary,no_of_transactions,mis_dictionary_ordered):
    list_L=[]
    flag=False
    for key in mis_dictionary_ordered:
        if key in count_dictionary:
            if (flag==False):
                meet_mis = mis_dictionary_ordered[key]
            if(count_dictionary[key]/no_of_transactions >= meet_mis):
                if(flag==False):
                    meet_mis=mis_dictionary_ordered[key]
                    flag=True
                    list_L.append(key)
                else:
                    list_L.append(key)
    return list_L
	
"""This function forms frequent itemset of size 1"""
def form_F1(count_dictionary,no_of_transactions,mis_dictionary_ordered,list_L):
    list_F1=[]
    for key in list_L:
        if(count_dictionary[key]/no_of_transactions >= mis_dictionary_ordered[key]):
            list_F1.append(key)
    return list_F1


""" This function filters frequent items based on must-have and cannot-be-together data"""
def check_F(F,cannot_be_together,must_have):
    F_after_check=[]
    must_have_set=set(must_have)
    for i in range(0,len(F)):
#         print(F[i])
        s=set(F[i])
        if(len(s.intersection(must_have_set)) > 0):
            F_after_check.append(F[i])

    F_after_check_length=len(F_after_check)
    F_after_check_new=F_after_check[:]
    for i in range(F_after_check_length):
#         print(range(len(F_after_check)))
        s1=set(F_after_check[i])
        for j in range(0,len(cannot_be_together)):
            s2=set(cannot_be_together[j])
            if(len(s1.intersection(s2)) > 1):
                F_after_check_new.remove(F_after_check[i])


                
    return F_after_check_new
	

def check_F1(list_F1,cannot_be_together,must_have):
    list_F1_after_reduction=[]
    for i in list_F1:
        if i in must_have:
            list_F1_after_reduction.append(i)
    return list_F1_after_reduction



""" Implementation of Level 2 candidate gen function"""	
def  L2_gen(list_L,sdc,no_of_transactions,count_dictionary,mis_dictionary_ordered):
#     print("L2_gen")
    candidate_list_final=[]
    for l in range(0,len(list_L)):
        if(count_dictionary[list_L[l]]/no_of_transactions >= mis_dictionary_ordered[list_L[l]]):
            for h in range(l+1,len(list_L)):
                if(count_dictionary[list_L[h]]/no_of_transactions >= mis_dictionary_ordered[list_L[l]]):
#                     supp_h = count_dictionary[list_L[h]]/no_of_transactions
#                     supp_l = count_dictionary[list_L[l]]/no_of_transactions
                    supp_h = count_dictionary[list_L[h]]
                    supp_l = count_dictionary[list_L[l]]
                    diff=supp_h-supp_l
                    if(abs(diff) <= (sdc*no_of_transactions)):
                        candidate_list=[]
                        candidate_list.append(list_L[l])
                        candidate_list.append(list_L[h])
                        candidate_list_final.append(candidate_list)
    return candidate_list_final



""" Implementation of MS candidate gen function"""
def MS_gen(F,sdc,no_of_transactions,count_dictionary,mis_dictionary_ordered):
    candidate_list_final=[]
#     print("inside msgen.................")
    for i in range(0,len(F)):
        l1=F[i][0:-1]
        for j in range(i+1,len(F)):
            l2=F[j][0:-1]
            if(l1==l2):
                first=F[i][-1]
                second=F[j][-1]
                if(mis_dictionary_ordered[first] < mis_dictionary_ordered[second] ):
#                     supp_first = count_dictionary[first]/no_of_transactions
#                     supp_second = count_dictionary[second]/no_of_transactions
                    supp_first = count_dictionary[first]
                    supp_second = count_dictionary[second]
                    diff=supp_first-supp_second
                    if(abs(diff) <= (sdc*no_of_transactions)):
                        candidate_list=[]
                        
#                         candidate_list.append(F[i][0:-1])
                        candidate_list=F[i][0:-1]
                        candidate_list.append(first)
                        candidate_list.append(second)
                        sub_list=list(list(itertools.combinations(candidate_list,len(candidate_list)-1)))
                        do_not_add=0
                        for k in range(0,len(sub_list)):
                            sub_list1=list(sub_list[k])
                            if((candidate_list[0] in sub_list1) or (mis_dictionary_ordered[candidate_list[0]] == mis_dictionary_ordered[candidate_list[1]]  )):
                                if(not(sub_list1 in F)):
                                    do_not_add=1
                                    break
                        if(do_not_add==0):
                            candidate_list_final.append(candidate_list)
    return candidate_list_final
	

""" MS-Apriori Algorithm"""
def msaprioriAlgorithm(): 
       
    F=[]
    inputFile='input-data.txt'
    parameterFile='parameter-file.txt'
    
    output=sys.stdout
    outputFile=open('output.txt','w')
    sys.stdout=outputFile
    
    
    count_dictionary,no_of_transactions,transaction_list = readInputFile(inputFile)
#     print("no_of_transactions",no_of_transactions)
#     print("length",len(transaction_list))
	
    mis_dictionary_ordered,sdc,cannot_be_together,must_have = readParameterFile(parameterFile)
#     print("SDC : ",sdc)
#     print("cannot_be_together",cannot_be_together)
#     print("must_have",must_have)

    list_L = form_L(count_dictionary,no_of_transactions,mis_dictionary_ordered)
    list_F1 = form_F1(count_dictionary,no_of_transactions,mis_dictionary_ordered,list_L)
    list_F1_after_reduction = check_F1(list_F1,cannot_be_together,must_have)
#     F.append(list_F1_after_reduction)
    F.append(list_F1)

    candidate_list_count_dict={}
    candidate_list_tail_count_dict={}

    k=1

    while(len(F[k-1]) > 0):
        if(k==1):
            candidate_list_final = L2_gen(list_L,sdc,no_of_transactions,count_dictionary,mis_dictionary_ordered)
#             print("......................",len(candidate_list_final))
            k=k+1
        else:
            candidate_list_final = MS_gen(F[k-1],sdc,no_of_transactions,count_dictionary,mis_dictionary_ordered)
            k=k+1

        for c in range(0,len(candidate_list_final)):
            l1=candidate_list_final[c]
            list_to_string = ','.join(map(str, l1))
            candidate_list_count_dict[list_to_string]=0
            candidate_list_tail_count_dict[list_to_string]=0

        for t in range(0,len(transaction_list)):
            for c in range(0,len(candidate_list_final)):
                l1=candidate_list_final[c]
                l2=l1[1:]

                s1=set(l1)
                s2=set(l2)

                if(s1.intersection(transaction_list[t])==s1):
                    list_to_string = ','.join(map(str, l1))
                    candidate_list_count_dict[list_to_string]+=1
                if(s2.intersection(transaction_list[t])==s2):
                    list_to_string = ','.join(map(str, l1))
                    candidate_list_tail_count_dict[list_to_string]+=1

        F_calculate=[]
        for c in range(0,len(candidate_list_final)):
            l1=candidate_list_final[c]
            list_to_string = ','.join(map(str, l1))
            if (candidate_list_count_dict[list_to_string]/no_of_transactions >= mis_dictionary_ordered[candidate_list_final[c][0]]):
                F_calculate.append(candidate_list_final[c])

#         print("Candidate List",candidate_list_final)
#         print("F_calculate.......................,k=",k,F_calculate)
#         F_after_check=F_calculate

#         for i in range(0,len(F_after_check)):
#             list_to_string=','.join(str(x) for x in F_after_check[i])
        F.append(F_calculate)

    
#     for i in range(0,len(F)):
#         print("k=",i+1,"list ",F[i])
        
    print("Frequent 1-itemsets")
    print()
    for i in range(0,len(list_F1_after_reduction)):
        s=set()
        s.add(list_F1_after_reduction[i])
        print(count_dictionary[list_F1_after_reduction[i]] ,":", s)
    print()
    print("Total number of frequent 1 - itemsets = ",len(list_F1_after_reduction))
    
    for i in range(1,len(F)):
        F_after_check=check_F(F[i], cannot_be_together, must_have)
        if(len(F_after_check)>0):
            print()
            print()
            print("Frequent ",i+1,"-itemsets")
            print()
            for j in range(0,len(F_after_check)):
                list_to_string=','.join(str(x) for x in F_after_check[j])
                print("\t",candidate_list_count_dict[list_to_string]," : ",set(F_after_check[j]))
                print("Tailcount = ",candidate_list_tail_count_dict[list_to_string])
            print()
            print("\tTotal number of frequent ",i+1,"- itemsets = ",len(F_after_check)  )
            
#     for i in range(1,len(F)):
#         F_after_check = check_F(F[i],cannot_be_together,must_have)
#         for j in range(0,len(F_after_check)):
#             list_to_string=','.join(str(x) for x in F_after_check[j])
#             print(F_after_check[i],candidate_list_count_dict[list_to_string],candidate_list_tail_count_dict[list_to_string])
        
    sys.stdout=output
    outputFile.close()
    outputFile=open('output.txt')
    print(outputFile.read())
    
    
if __name__ == '__main__':
    msaprioriAlgorithm()

