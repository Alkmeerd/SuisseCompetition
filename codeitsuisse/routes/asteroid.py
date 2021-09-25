import logging
import json

from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

def Cal(s):
    def Score(increment):
        if increment >= 7 and increment < 10:
            return increment*1.5
        elif increment >= 10:
            return increment*2
        else:
            return increment


    list1, list2 = [],[]

    c = 1
    for i in range(len(s)):
        try:
            if s[i] != s[i+1]:
                list1.append(s[i])
                list2.append(c)
                c = 0
        except:
            list1.append(s[-1])
            list2.append(c)

        c += 1



    max_score = 0
    pos = 0

    for i in range(len(list1)):
        target = i
        left = target
        right = target
        score = Score(list2[target])
    
        while left > 0 and right < len(list1)-1:

            if list1[left] != list1[right]:
                break
            else:
                left -= 1
                right += 1

                if list1[left] != list1[right]:
                    break
                increment = list2[left]+list2[right]
                score += Score(increment)

            
        #print(length)  
        if score > max_score:
            max_score = score
            pos = i


    origin = 1
    for i in range(pos):
        origin += list2[i]

    return (max_score, origin)
    #print(origin)

def Output(i):
    a, b = Cal(i)
    #print(i)
    #print(a)
    #print(b)

    dict = {
        "input": i,
        "score": a,
        "origin": b,
    }

    return dict    

@app.route('/asteroid', methods=['POST'])
def asteroid():

    data = request.get_json()

    list = []
    for i in data["test_cases"]:
        dict = Output(i)
        list.append(dict)


    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(list))

    return json.dumps(list)



