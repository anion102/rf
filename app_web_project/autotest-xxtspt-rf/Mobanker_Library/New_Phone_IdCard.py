#encoding:utf-8

import time, random

ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
pro = {0:11,1:12,2:13,3:14,4:15,5:21,6:22,7:23,8:31,9:32,10:33,11:34,12:35,13:36,14:37,15:41,16:42,17:43,18:44,19:45,20:46,21:50,22:51,23:52,24:53,25:54,26:61,27:62,28:63,29:64,30:65}

def createIdcard():
    u''' 随机生成新的18为身份证号码 '''
    t = time.localtime()[0]
    #print t
    x = '%02d%02d%02d%04d%02d%02d%03d' %(pro[random.randint(0,30)],
                                        random.randint(01,99),
                                        random.randint(01,99),
                                        random.randint(t - 80, t - 20),
                                        random.randint(1,12),
                                        random.randint(1,28),
                                        random.randint(1,999))
    #print x[8],x[9]
    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]

    return '%s%s' %(x, LAST[y % 11])

def createPhone():
        u'''随机生成手机号'''

	prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
	return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))

#print createIdcard()
#print type(createPhone())