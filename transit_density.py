# transit_density.avg_density() gives a measure of the population served by the stops of a real or imagined transit line anywhere in greater Toronto.
# Input argument is a list of [lat,long] points representing the stations on a line.
# Output is a measure of the average density of each station's surroundings, on a scale from 0 (not dense) to 1 (very dense).
# 'd.csv' contains RGB values for the following jpeg image, a map of StatsCan density data for Toronto:
#   https://mitchellwhale.com/wp-content/uploads/2017/11/toronto-traffic-density.jpg

import csv
import math
filepath='./d.csv'

def get_data():
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        result = []
        for row in csv_reader:
            result.append(row)
            line_count += 1
        split_result=[]
        for item in result[0]:
            j=item.split(' ')
            split_result.append(j)
    return split_result

def get_colours():
    inmat=get_data()
    r=[]
    g=[]
    b=[]
    i=0
    for row in inmat:
        if i%3==0: 
            r.append(row)
        if i%3==1:
            g.append(row)
        if i%3==2:
            b.append(row)
        i+=1
    result=[r,g,b]
    return result

def d():
    colour_list=get_colours()
    legend={'road':[0,0,0],'lake':[255,255,255],'k27':[140,197,253],'k37':[124,255,243],'k47':[164,254,135],'k60':[233,254,127],'k80':[254,204,134],'k95':[254,126,126],'ktop':[254,60,60]}
    cat_list=[]
    for i in range(len(colour_list[0])):
        cat_row=[]
        for j in range(len(colour_list[0][0])):
            cost_dict={}
            for key,value in legend.items():
                cost_minilist=[]
                for k in range(2):
                    colour_cost=abs(int(colour_list[k][i][j])-value[k])
                    cost_minilist.append(colour_cost)
                cost_dict[key]=sum(cost_minilist)
            v=list(cost_dict.values())
            k=list(cost_dict.keys())
            cat_row.append(k[v.index(min(v))])
        cat_list.append(cat_row)
    return cat_list


def density():
    i=0
    colour_list=get_colours()
    density_list=[]
    for item in colour_list[0]:
        j=0
        density_row=[]
        for jtem in item:
            rgb=int(jtem)-(int(colour_list[1][i][j])+int(colour_list[2][i][j]))
            
            density_row.append(density)
            j+=1
        density_list.append(density_row)
        i+=1
    return density_list
        
def ind2lat(ind):
    return 43.884989-0.000542496*ind
def ind2long(ind):
    return 0.000739551*ind-79.680089
def lat2ind(lat):
    return (lat-43.884989)/-0.000542496
def long2ind(long):
    return (long+79.680089)/0.000739551
def ll2ind(latlong):
    ind1=lat2ind(latlong[0])
    ind2=long2ind(latlong[1])
    return [ind1,ind2]
def ind2ll(ind1ind2):
    lat=ind2lat(ind1ind2[0])
    long=ind2long(ind1ind2[1])
    return [lat,long]

def station_density(station_ll):
    dens=d()
    ind=ll2ind(station_ll)
    g_list=[]
    for y in dens[int(ind[0]-10):int(ind[0]+10)]:
        for x in y[int(ind[1]-10):int(ind[1]+10)]:
            pixel_distance=abs(dens.index(y)-ind[0])+abs(y.index(x)-ind[1])
            val_dct={'road':0,'lake':-1,'k27':0,'k37':1,'k47':2,'k60':3,'k80':4,'k95':5,'ktop':6}
            x_val=val_dct[x]
            g_pixel = x_val/pixel_distance
            g_list.append(g_pixel)
    summed_goodness=sum(g_list)
    normalized_goodness=(summed_goodness+0.9793181777649153)/23.12726812796419
    return normalized_goodness

def avg_density(line):
    line_list=[]
    for item in line:
        line_list.append(station_density(item))
    return sum(line_list)/len(line_list)

def stations(start_ll,min_dist,max_dist,n,dens='none'):
    station_list=[start_ll]
    dist_list=[]
    if dens=='none':
        dens=d()
    dist=min_dist
    current_location=start_ll
    last_location=[]
    while dist<=max_dist:
        dist_list.append(dist)
        dist+=0.001
    print(dist_list)
    for i in range(n):
        print(current_location)
        candidates_n=[]
        for dist in dist_list:
            candidates_n.append([current_location[0]-dist/5,current_location[1]]) #5 is rough ratio of lat to long in distance. calculate precisely later.
            candidates_n.append([current_location[0]+dist/5,current_location[1]])
            candidates_n.append([current_location[0],current_location[1]-dist])
            candidates_n.append([current_location[0],current_location[1]+dist])
        if last_location in candidates_n:
            candidates_n.remove(last_location)
        g_list=[]
        print(candidates_n)
        for candidate in candidates_n:
            g_list.append(station_density(candidate))
        station_list.append(candidates_n[g_list.index(max(g_list))])
        g_dict={}
        for i in range(len(candidates_n)):
            g_dict[tuple(candidates_n[i])]=g_list[i]
        print(g_dict)
        last_location=current_location
        current_location=candidates_n[g_list.index(max(g_list))]
    return station_list

def get_rgb(ind1,ind2):
    colour_list=get_colours()
    r=colour_list[0][ind1][ind2]
    g=colour_list[1][ind1][ind2]
    b=colour_list[2][ind1][ind2]
    return [r,g,b]