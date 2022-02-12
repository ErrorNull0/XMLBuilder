# XMLBuilder
A Python program that automatically generates XML for complex entitygroups for 7 Days to Die. These are the spawn groups defined in entitygroups.xml.

Example: We want to generate the XML for the Bloodmoon horde group - which is called "feralHordeStageGS".

--------
 Step 1
--------

Create a csv file and use the entity group name as the filename. For example, the Bloodmoon horde group uses the names, feralHordeStageGS1, feralHordeStageGS2, feralHordeStageGS4, feralHordeStageGS7, etc. So you would ingore the numbers and just use "feralHordeStageGS" as the filename --> feralHordeStageGS.csv.

Each row in this file will represent spawn information for one zombie - refer to existing feralHordeStageGS.csv as an example. Each additional zombie is entered on a new row. Add all the zombies that will be spawning in this bloodmoon horde group. The information in each column of this file represents the following:

zombie name, starting probability, ending probability, starting gamestage, max gamestage, ending gamestage

zombie name - the name of the zombie, spelled exactly as shown in its entityclass definition
starting probability - the initial probability value this zombie will have as it starts the progression up the gamestages
ending probability - the highest probability value this zombie will attain
starting gamestage - the first gamestage number that this zombie will have any chance of spawning in
max gamestage -the gamestage number at which this zombie will reach its "ending probability"
ending gamestage - the final gamestage number that this zombie will spawn in. the zombie will not spawn in any later gamestages.

Example:
zombieArlene	        1	    1	  1	    195	  715
zombieArleneFeral	    0.1	  1	  31	  715	  1308
zombieArleneRadiated	0.1	  1	  103	  715	  715

zombieArlene starts spawning at gamestage 1 with spawn probability of 1. 
From gamestage 1 to gamestage 195, the spawn probabililty will remain constant at 1.
From gamestage 195 to 715, the spawn probability will gradually decreases from 1 to 0.
This zombie has zero probability to spawn after gamestage 715

zombieArleneFeral starts spawning at gamestage 31 with spawn probability of 0.1. 
From gamestage 31 to gamestage 715, the spawn probabililty gradually increases from 0.1 to 1.
From gamestage 715 to 1308, the spawn probability will gradually decreases from 1 to 0.
This zombie has zero probability to spawn after gamestage 1308.

zombieArleneRadiated starts spawning at gamestage 103 with spawn probability of 0.1. 
From gamestage 103 to gamestage 715, the spawn probabililty gradually increases from 0.1 to 1.
From gamestage 715 through all remaining gamestages, the spawn probability stays at 1.

--------
 Step 2
--------

When all rows have been entered for each zombie, skip one row.

Now list all possibile gamestage numbers for the Bloodmoon horde group (feralHordeStageGS) in ascending order, with each gamestage number on each row. All gamestage must match exactly the number of gamestages show in the vanilla entitygroups.xml file for this group, feralHordeStageGS.

--------
 Step 3
--------

Go to the Pythong program code, and near the top, look for where the variable "entitygroup_name" is defined. Ensure it is assigned the name of the entity group, which in this case is feralHordeStageGS.

entitygroup_name = "feralHordeStageGS"

Save a run the Python code. It will generate all the XML for the bloodmoon horde group, and output it to a txt file with the entity group name "feralHordeStageGS" as the filename. Copy and paste the contents of the text file in the game's entitygroups.xml file, in the appropriate location as an xpath <append> statement.
  
All done.

-----
Feel free to use and share.

ErrorNull
