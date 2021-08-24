# imports extern
import pandas as pd
import numpy as np

# imports intern
import sequence_pre_calculation as pre_calc

# TODO statistical calculation here
#pre_calc.dict_best_one
#pre_calc.dict_best_two

ov95 = [0, 0]
ov90 = [0, 0]
ov80 = [0, 0]
#ov50 = [0, 0]
#lo50 = [0, 0]

#for val in pre_calc.dict_best_one:
    #if val < 50:
    #    lo50[0] += 1
    #elif val > 80:
    #    ov80[0] += 1
    #else:
    #    ov50[0] += 1
#for val in pre_calc.dict_best_two:
    #if val < 50:
    #    lo50[1] += 1
    #elif val > 80:
    #    ov80[1] += 1
    #else:
    #    ov50[1] += 1

for val in pre_calc.dict_over95_one:
    ov95[0] += int(val/95)
for val in pre_calc.dict_over90_one:
    ov90[0] += int(val/90)
for val in pre_calc.dict_over80_one:
    ov80[0] += int(val/80)

for val in pre_calc.dict_over95_two:
    ov95[1] += int(val/95)
for val in pre_calc.dict_over90_two:
    ov90[1] += int(val/90)
for val in pre_calc.dict_over80_two:
    ov80[1] += int(val/80)


print("best values for each row, column")
#print("total one :", len(pre_calc.seq_one))
#print("total two : ", len(pre_calc.seq_two))
#print("< 50     :", lo50)
#print("> 50 < 80:", ov50)

#print(">= 80 < 90:", ov80)
print(">= 80 < 90: %d , %d" % (ov80[0]/len(pre_calc.seq_one), ov80[1]/len(pre_calc.seq_two)))
#print(">= 90 < 95:", ov90)
print(">= 90 < 95: %d , %d" % (ov90[0]/len(pre_calc.seq_one), ov90[1]/len(pre_calc.seq_two)))
#print(">= 95     :", ov95)
print(">= 95     : %d , %d" % (ov95[0]/len(pre_calc.seq_one), ov95[1]/len(pre_calc.seq_two)))
