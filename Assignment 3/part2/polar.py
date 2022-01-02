#!/usr/local/bin/python3
#
# Authors: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import pandas as pd
import math

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = image.copy()
    new_image = draw_boundary(new_image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

def calc_emission_probablity(edge_strength,image_array):
    add_mat = edge_strength+0.000045*image_array
    return add_mat

def calc_transition_probablity(trans_prob):
    
    denominator=[]
    for i in range(len(trans_prob)):
        den1=0
        den2=0
        for j in range(len(trans_prob)):
            trans_prob[j][i] = len(trans_prob)-abs(i-j)
            if abs(i-j) in range(0,30):
                den1+=trans_prob[j][i]
            else:
                den2+=trans_prob[j][i]
        den1=den1/0.99
        den2=den2/0.01

    for i in range(len(trans_prob)):
        for j in range(len(trans_prob)):
            if abs(i-j) in range(0,30):
                trans_prob[j][i] = math.log(trans_prob[j][i])-math.log(den1)
            else:
                trans_prob[j][i] = math.log(trans_prob[j][i])-math.log(den2)

    return trans_prob

def viterbi(emission_prob,trans_prob,initial_prob):
    initial = initial_prob
    V_table = zeros((len(emission_prob),len(emission_prob[0])))
    which_table = zeros((len(emission_prob),len(emission_prob[0])))

    for i in range(len(emission_prob)):
        V_table[i][0] = emission_prob[i][0]

    for i  in range(1,len(emission_prob[0])):
        for j in range(len(emission_prob)):
            curr_v = [V_table[s0][i-1]+trans_prob[s0][j] for s0 in range(len(emission_prob))]
            which_table[j][i], V_table[j][i] =  argmax(curr_v),max(curr_v)
            V_table[j][i] += emission_prob[j][i]
    
    viterbi_seq = [0] * len(emission_prob[0])
    viterbi_seq[len(emission_prob[0])-1] =int(argmax(V_table[:,len(emission_prob[0])-1]))
    
    for i in range(len(emission_prob[0])-2, -1, -1):
        
        viterbi_seq[i] = int(which_table[viterbi_seq[i+1]][i+1])
    viterbi_seq = asarray(viterbi_seq)
    
    return viterbi_seq

def human_viterbi(emission_prob,trans_prob,initial_prob,point):
    point_x,point_y = point[0],point[1]
    initial = initial_prob
    V_table = zeros((len(emission_prob),len(emission_prob[0])))
    which_table = zeros((len(emission_prob),len(emission_prob[0])))

    for i in range(len(emission_prob)):
        V_table[i][0] = emission_prob[i][0]

    for i  in range(1,len(emission_prob[0])):
        for j in range(len(emission_prob)):
            curr_v = [V_table[s0][i-1]+trans_prob[s0][j] for s0 in range(len(emission_prob))]
            which_table[j][i], V_table[j][i] =  argmax(curr_v),max(curr_v)
            if j==point_y and i==point_x:
                V_table[j][i]=1
            V_table[j][i] += emission_prob[j][i]
    
    viterbi_seq = [0] * len(emission_prob[0])
    viterbi_seq[len(emission_prob[0])-1] =int(argmax(V_table[:,len(emission_prob[0])-1]))
    
    for i in range(len(emission_prob[0])-2, -1, -1):
        viterbi_seq[i] = int(which_table[viterbi_seq[i+1]][i+1])
    viterbi_seq = asarray(viterbi_seq)
    
    return viterbi_seq



# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.
    #airice_simple = [ image_array.shape[0]*0.25 ] * image_array.shape[1]
    
    
    prior_prob1 =zeros((len(edge_strength),len(edge_strength[0])))
    d=(len(edge_strength)*(len(edge_strength)+1))/2
    for i in range(len(prior_prob1[0])):
        for j in range(len(prior_prob1)-1,-1,-1):
            prior_prob1[j][i]=(len(prior_prob1)-j)/d

    emission_prob = calc_emission_probablity(edge_strength,image_array)
    num=prior_prob1*emission_prob
    
    

    ridge=list(argmax(num,axis=0))
   
    airice_simple =ridge
    num2=zeros((len(edge_strength),len(edge_strength[0])))
    prior_prob2 =zeros((len(edge_strength),len(edge_strength[0])))
    count_a=0
    count_b=0
    
    for i in range(len(edge_strength[0])):
        count_a=0
        count_b=0
        for j in range(len(edge_strength)):
            if j<ridge[i]+10:
                count_a+=1
        count_b=len(edge_strength)-count_a
        for j in range(count_a):
            prior_prob2[j][i] = 0.01/count_a
        for j in range(count_a,len(edge_strength)):
            prior_prob2[j][i] = 0.99/count_b
        
    num2 = prior_prob2*emission_prob
    denom1=sum(num,axis=0)
    denom2 = sum(num2,axis=0)
    for i in range(len(num[0])):
        for j in range(len(num)):
            num[j][i]=math.log(num[j][i]/denom1[i])

    for i in range(len(num2[0])):
        for j in range(len(num2)):
            num2[j][i]=math.log(num2[j][i]/denom1[i])

    for i in range(len(prior_prob1[0])):
        for j in range(len(prior_prob1)):
            prior_prob1[j][i] = math.log(prior_prob1[j][i])
            prior_prob2[j][i] = math.log(prior_prob2[j][i])

    
    
    

    ridge2=list(argmax(num2,axis=0))
    icerock_simple = ridge2

    trans_prob = zeros((len(image_array),len(image_array)))
    trans_prob=calc_transition_probablity(trans_prob)
    ridge3=viterbi(num,trans_prob,prior_prob1[:,0])
    airice_hmm = ridge3

    ridge4 = viterbi(num2,trans_prob,prior_prob2[:,0])
    icerock_hmm = ridge4

    ridge5 = human_viterbi(num,trans_prob,prior_prob1[:,0],gt_airice)
    airice_feedback =ridge5

    ridge6 = human_viterbi(num2,trans_prob,prior_prob1[:,0],gt_icerock)
    icerock_feedback =ridge6
    

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
