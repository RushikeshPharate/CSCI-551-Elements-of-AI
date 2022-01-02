#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Rushikesh Pharate
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#


"""
- State Space: Groups of all the users where each group has all the users in the combination of 1/2/3
- Initial State: Users arranged in the groups of 1 each
- Succesor Function: For the current state, successor function is all the unique combinations of teams derived after arranging  
- Goal State: There is no particular goal state here, we are searching for arrangements of given users into groups of 1/2/3 such that the the staff has to do minimum work
- Cost Function: For a given combination of groups, the cost function is total amount of time the staff has to spend for this combination

Calculation of time spent on current combination was not that hard to implement as it was just about handling every case for time required mentioned in the assignment

The hardest part of the assignment was to come up with the successor function and initial state.

When I first started thinking about the problem, forming groups of 3 seemed like a good option for initial state because the time for grading each assignment is 5 mins and having less teams means less cost. But, after spending some time thinking about what will be the successor function I dropped that thought as I was not able to come up with a logic for successor function. 

After spending a day or two on thinking about the initial state and successor functions, I came up with an idea to start with groups of 1 user each and then increment the group size one at a time. The successor function in this case return all the valid combination of group arrangement with size increased by 1.

While coding the logic for calculating successor functions I made a lot of mistakes but after spending significant amount of time on dubugging finally I was able to implement it correctly.


Also, when I was working on defining successor function I had a high level discussion with Nikhil Kambale from EAI-b551 in person batch about how we can implement it

"""


import sys
from itertools import combinations
import heapq

# calculate the total time spent on current combination os teams
def calculate_assignment_cost(assigned_teams,stu_preferences,stu_dontwants,stu_preferred_team_size):
    teamsize_mismatch=0
    preference_mismatch=0
    dontwant_mismatch=0
    teams_count=0

    for current_team in assigned_teams:
        # print(current_team)
        
        #calculate preference mismatch in current team
        for stu in current_team:
            # print(stu)
            curr_stu_preferences=stu_preferences.get(stu)
            #print(curr_stu_preferences)
            if curr_stu_preferences is not None:
                for x in curr_stu_preferences:
                    if x not in ('xxx','zzz'):
                        if x not in current_team:
                            preference_mismatch+=1
                # print(preference_mismatch) 

        #calculate dontwant mismatchin current team
        for stu in current_team:
            # print(stu)
            curr_stu_dontwants=stu_dontwants.get(stu)
            # print(curr_stu_dontwants)
            if curr_stu_dontwants is not None:
                for x in curr_stu_dontwants:
                    if x in current_team:
                        dontwant_mismatch+=1
                # print(dontwant_mismatch)

        for stu in current_team:
            # print(stu)
            curr_stu_preferred_team_size=stu_preferred_team_size.get(stu)
            # print(curr_stu_preferred_team_size)
            if len(current_team)!=curr_stu_preferred_team_size:
                teamsize_mismatch+=1
            # print(teamsize_mismatch)
        teams_count+=1
    total_time_for_curr_team=preference_mismatch*(0.05*60) + dontwant_mismatch*10 + teamsize_mismatch*2 + 5*teams_count
    return total_time_for_curr_team

# Check if if any user from new_team is present in team
def is_user_in_new_team_present_in_team(new_team,team):
    for user in new_team[0]:
        if user in team:
            return True
    return False


# calculate sucessors of the current_state
def succ_of_current_assignment(curr_assignment):
    successors=[]
    new_team=[]
    a=combinations(curr_assignment, 2)
    for i in a:
        teams_from_currAss_not_having_any_member_in_newTeam=[]
        # print("i is: ",i)
        new_team=[i[0]+i[1]]
        # print("New team is: ",new_team)
        if len(new_team[0])>3:
            continue
        for team in curr_assignment:
            if not is_user_in_new_team_present_in_team(new_team,team):
                teams_from_currAss_not_having_any_member_in_newTeam.append(team)    
        new_assignment_state=new_team+teams_from_currAss_not_having_any_member_in_newTeam
        successors.append(new_assignment_state)
        # print("NEw Assignment state: ",new_assignment_state)    
    # print("Print Successors: ",successors)
    return successors
        
# convert current combination of teams into a proper format to yield the data
def get_returnable_data(curr_assignment):
    res=[]
    for team in curr_assignment:
        res.append('-'.join(team))
    return res

def solver(input_file):
    #Read the input_file and store all the data fron one row as a list
    text_file=open(input_file,'r')
    data=[]
    for row in text_file:
        itm=row.rstrip('\n').split(' ')
        data.append(itm)
    # print(data)

    #one list storing all the student usernames and two dictionaries for storing preferences and dontwants with student username as the key
    stu_username=[]
    stu_preferences={}
    stu_dontwants={}
    stu_preferred_team_size={}

    for ele in data:
        temp1=ele[1].split('-')
        preferred_team_size=len(temp1)
        # print("preferred team size: ",preferred_team_size)
        # print('/n')
        stu_preferred_team_size[ele[0]]=preferred_team_size
        stu_preferences[ele[0]]=temp1[1:]
        temp2=ele[2].split(',')
        stu_dontwants[ele[0]]=temp2
        temp3=[None]
        temp3[0]=ele[0]
        stu_username.append(temp3)
        
    # print(stu_username)
    # print(stu_preferences)
    # print(stu_preferred_team_size)
    # print(stu_dontwants)

    initial_team=stu_username    

    fringe=[]
    # Using priority queue for implementation of fringe
    heapq.heapify(fringe)
    heapq.heappush(fringe,(calculate_assignment_cost(initial_team,stu_preferences,stu_dontwants,stu_preferred_team_size),initial_team))  
    
    visited_assignment_states=[] # tracking the visited states to avoid algorithm going into infinite loop
    cost_limit_for_yield=1000

    while len(fringe)>0:
        # print("Fringe Start")
        (curr_assignment_cost,curr_assignment)=heapq.heappop(fringe)
        visited_assignment_states.append(curr_assignment)

        if curr_assignment_cost<cost_limit_for_yield:
            cost_limit_for_yield=curr_assignment_cost
            data={}            
            data["assigned-groups"]=get_returnable_data(curr_assignment)
            data["total-cost"]=curr_assignment_cost
            yield(data)

        for succ in succ_of_current_assignment(curr_assignment):
            # print("Inside Succ")
            # print("Current Successor: ",succ)
            curr_succ_cost=calculate_assignment_cost(succ,stu_preferences,stu_dontwants,stu_preferred_team_size)
            # print("curr_succ_cost: ",curr_succ_cost)
            # print("curr_assignment_cost: ",curr_assignment_cost)
            if succ in visited_assignment_states:
                continue
            else:
                if curr_succ_cost<curr_assignment_cost:
                    # print("BEFORE HEAPPUSH")
                    heapq.heappush(fringe,(curr_succ_cost,succ))
                    # print("After HEAPPUSH")
        
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    






