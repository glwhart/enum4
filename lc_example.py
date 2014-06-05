#!/usr/bin/python
labeling = [1,1,1,1,2,0,2,0]
shortlabeling = []
for i in labeling:
    if i == 2:
        shortlabeling.append(1)
    elif i==0:
        shortlabeling.append(0)
print labeling
print shortlabeling

