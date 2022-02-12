print("\n*******************************************************")
print("********** XML BUILDER for Entitygroups v1.0 **********")
print("*******************************************************\n")

# entitygroup_name MUST match an existing entitygroup from within entitygroups.xml. 
# This is the entity group for which the XML spawn data will be auto-generated.
# This also tells the program what filename to look for as the input CVS file,
# and also determine the filename of the output TXT file.
entitygroup_name = "feralHordeStageGS"

gamestages = []

# load all zombie data from file
file = open(entitygroup_name + ".csv", mode='r', encoding='utf-8')
filedata = file.read().splitlines()
file.close()
zombie_data = []

print("Loading zombies: ", end="")
for index in range(len(filedata)):
    popped_data = filedata.pop(0)
    #print("popped_data: " + popped_data)

    if popped_data != ",,,,,":
        zombie_raw_data = popped_data.split(",")
        #print("zombie_raw_data: ", end="")
        #print(zombie_raw_data)
        zombie_name = zombie_raw_data[0]
        prob_start = float(zombie_raw_data[1])
        prob_end = float(zombie_raw_data[2])
        gs_start = int(zombie_raw_data[3])
        gs_max = int(zombie_raw_data[4])
        gs_end = int(zombie_raw_data[5])
        zombie_data.append([zombie_name, prob_start, prob_end, gs_start, gs_max, gs_end, 1, 1])
        print(zombie_name + " ", end="")
    else:
        print(".. Done!\n")
        print("Loading Gamestage values... ", end="")
        
        for index in range(len(filedata)):
            popped_data = filedata.pop(0)
            #print("popped_data: " + popped_data)
            gamestages.append(int(popped_data.strip(",")))
        
        print("Done!")
        print("GS values loaded: ", end="")
        print(gamestages)
        break
        
    #print("zombie_data: ", end="")
    #print(zombie_data)
    #print("")

gamestage_count = len(gamestages)
print("")
print("Gnerating custom zombie spawn probabilities for... \n")

file = open(entitygroup_name + ".txt", 'w', encoding = 'utf-8')
for index in range(gamestage_count):
    
    # print the opening <append> tag for this gamestage and go to the next line
    current_gamestage_num = gamestages[index]
    #print("<append xpath=\"/entitygroups/entitygroup[@name=\'" + entitygroup_name  + str(current_gamestage_num) + "\']\">")
    print(entitygroup_name  + str(current_gamestage_num), end="")
    file.write("<append xpath=\"/entitygroups/entitygroup[@name=\'" + entitygroup_name  + str(current_gamestage_num) + "\']\">\n")
    
    for index2 in range(len(zombie_data)):
        zombie_name = zombie_data[index2][0]
        zombie_prob_start = zombie_data[index2][1]
        zombie_prob_end = zombie_data[index2][2]
        zombie_spawn_start_index = gamestages.index(zombie_data[index2][3])
        zombie_spawn_falloff_index = gamestages.index(zombie_data[index2][4])
        zombie_spawn_end_index = gamestages.index(zombie_data[index2][5])
        zombie_prob_climbing_counter = zombie_data[index2][6]
        zombie_prob_falling_counter = zombie_data[index2][7]
        zombie_spawn_prob = 0

        # too early for zombie to spawn at this gamestage, so prob set to zero
        if  index < zombie_spawn_start_index:
            zombie_spawn_prob = 0
        
        # the first gamestage for zombie to spawn. add entry with first/begining prob value
        elif index == zombie_spawn_start_index:
            zombie_spawn_prob = zombie_prob_start            
            
        # the last gamestage for zombie to spawn. add entry with final/last prob value
        elif index == zombie_spawn_falloff_index:
            zombie_spawn_prob = zombie_prob_end
            
        elif index > zombie_spawn_end_index:
        
            # zombie configured to stay at max 100% spawn prob when reaching falloff point 
            if zombie_spawn_end_index == zombie_spawn_falloff_index:
                zombie_spawn_prob = 1
                
            # reached the final gamestage for this zombie, so no more spawning.
            else: 
                zombie_spawn_prob = 0
                
        # zombie has gone past its max gamestage, and now each entries has decreasing prob value
        elif index > zombie_spawn_falloff_index:
            prob_decrement = zombie_prob_end / (zombie_spawn_end_index - zombie_spawn_falloff_index)
            zombie_spawn_prob = round(zombie_prob_end - (prob_decrement * zombie_prob_falling_counter), 2)
            zombie_data[index2][7] = zombie_prob_falling_counter + 1
            
            # if zombie prob drops off below 5%, do not add any more entries for spawning
            if zombie_spawn_prob < 0.05:
                 zombie_spawn_prob = 0
        
        # zombie hasn't reached its max/falloff gamestage, so each entry has increasing prob value
        else: 
            prob_increment = (zombie_prob_end - zombie_prob_start) / (zombie_spawn_falloff_index - zombie_spawn_start_index)
            zombie_spawn_prob = round(zombie_prob_start + (prob_increment * zombie_prob_climbing_counter), 2)
            zombie_data[index2][6] = zombie_prob_climbing_counter + 1
        
        
        ###### PRINT THE RESULTING XML ######
       
        # if spawn prob < 5%, zombie should not spawn so do not print any spawn code
        if zombie_spawn_prob < 0.05:
            doNothing = "nothingGoingOnHereYet.."
            
        # if spawn prob is 100%, print the shortened spawn code (without the "prob" attribute/value)
        elif zombie_spawn_prob == 1:            
            #print("<entity name=\"" + zombie_name + "\"/>", end="")
            print(".", end="")
            file.write("<entity name=\"" + zombie_name + "\"/>")
        
        # print the spawn code with "prob" attribute/value for this zombie
        else: 
            #print("<entity name=\"" + zombie_name + "\" prob=\"" + str(zombie_spawn_prob) + "\"/>", end="")
            print(".", end="")
            file.write("<entity name=\"" + zombie_name + "\" prob=\"" + str(zombie_spawn_prob) + "\"/>")
            
    # for loop complete: go to next line and add closing </append> tag since there's no more zombies of this type
    #print("\n</append>")
    print(" done!\n")
    file.write("\n</append>\n")

    
file.close()

print("XML for " + entitygroup_name + " created and saved to file \"" + entitygroup_name + ".txt\"!")
print("Copy and paste the contents into the appropriate location within ENTITYCLASSES.XML.")