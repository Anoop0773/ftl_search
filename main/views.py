from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import csv 
import json
import math


# word_list is list of all stirng lists
# search_dictionary is all key value pair of word and their usage
word_list = []
rows = []
search_dictionary = {}

#load_search_file will load the file and store valus in word_list and search_dictionary
def load_search_file():
    filename = 'word_search.tsv'
    search_file = settings.STATIC_ROOT + 'searchFile/' + filename
    with open(search_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            word_list.append(row[0])
            rows.append(row)
            search_dictionary[row[0]] = row[1]


#index fucntion to load page 
def index(request):
    context = {}
    if len(word_list) == 0:
        load_search_file()
    return render(request,'index.html',context) 
    
    



#search funtion to use for giving search result to template and json
# def search(request):
#     search = {}
#     all_suggest_tags = []
#     suggest_tags = []
#     word = request.GET.get('word')
#     if len(word_list) == 0:
#         load_search_file()


#     #following code will filter out all your words and store in all_suggest_tags.
#     #following code will satisfiled constraint (1)
#     for row in word_list:
#         if word in row:
#             all_suggest_tags.append(row)
            


#     #following code will give rank position if all your words if they starts with given word.
#     #following code will satisfiled constraint (2)(a)
#     for tag in all_suggest_tags:
#         if tag.startswith(word):
#             suggest_tags.append(tag)
   
  
#     #following code will will use to store all rest list of words
#     rest_tags = set(all_suggest_tags) - set(suggest_tags)
#     rest_tags = list(rest_tags)

#     #following code will  give rank position according to len of word.
#     #following code will satisfiled constraint (2)(c)
#     suggest_tags.sort(key=len)
#     rest_tags.sort(key=len)
    
#     if len(suggest_tags) < 25:
#         suggest_tags.extend(rest_tags[:(25 - len(suggest_tags))])
#     else:
#         suggest_tags = suggest_tags[:25]
    


#     #following code will  give rank position according to number of usage.
#     #following code will satisfiled constraint (2)(b)
#     # word_list_list = []
#     # for tag in suggest_tags:
#     #     single_row = [tag,search_dictionary[tag]]
#     #     word_list_list.append(single_row)
    
#     # word_list_list = sorted(word_list_list, key = lambda x: int(x[1]),reverse=True)
#     # final_tags = []
#     # for row in word_list_list:
#     #     final_tags.append(row[0])
#     search['suggest_tags']  = suggest_tags
#     print(len(suggest_tags))

#     return HttpResponse(json.dumps(search), content_type="application/json")







# search funtion to use for giving search result to template and json
def search(request):
    search = {}
    suggest_dic = {}
    all_suggest_tags = []
    suggest_tags = []
    word = request.GET.get('word')
    print('#########')
    print(word)
    if len(word_list) == 0:
        load_search_file()


    #following code will filter out all your words and store in all_suggest_tags.
    #following code will satisfiled constraint (1)
    max_len_string = 0
    for row in word_list:
        if word in row:
            all_suggest_tags.append(row)
            suggest_dic[row] = int(search_dictionary[row])/10000
            # print('key,value',row,search_dictionary[row])
            if len(row)>max_len_string:
                max_len_string = len(row)
    


    #following code will change position all your words.
    #following code will satisfiled constraint (2)

    #follwoing logic I made for this,start_index is where search string starts in a perticular string
    #match_len is how much string is left after matching the search string in that perticilar string
    # power is something  where we give weight to string according to appearance in sting of search string
      


    list_of_all_strings = []
    for key in suggest_dic:
        start_index =  key.find(word)
        match_len = max_len_string - (len(key) - len(word)) 
        power = math.pow((max_len_string - start_index),len(word)) 
         
        # print('key ->match_len',key,match_len)
        
        weight_calculation = suggest_dic[key] * match_len * power
        one_row = [key , weight_calculation]
        list_of_all_strings.append(one_row)
     
    
    sorted_list =   sorted(list_of_all_strings, key = lambda x: int(x[1]),reverse=True) 

    search_list = []
    for row in sorted_list:
        search_list.append(row[0])

    # print(search_list[:25])
    search['search_list'] = search_list[:25]
    search['length'] = len(sorted_list[:25])
    

    return HttpResponse(json.dumps(search), content_type="application/json")