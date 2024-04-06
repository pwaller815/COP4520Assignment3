# COP4520Assignment3

To run this program first download the files minotaurBirthday.py and minotaurShowroom.py; save the files anywhere you desire. Next using a command prompt navigate to the directory you saved the file in. Once there, use the command following command to run the script:

For part 1:
python minotaurGift.py
For part 2:
python ATRM.py

# Part 1:
# Evaluation/Summary of approach

When approaching this problem I decided on using a strategy that involves "hand over hand" order. Servant threads are able to enter the list for any operation of the three operations: insert, remove, contains. This is due to the fact that each node in the linked list has a lock. Each lock is managed as a thread traverses each node, this allowed for the runtime to be exponentially better for the assignment as threads were not waiting long periods for other threads to complete any task. 

# Proof of correctness, efficiency and experimental evaluation

This solution meets the criteria of the problem because it does not allow any threads to make mistakes due to the locking method. Once a thread encounters a locked node it returns to the method call it made and tries again. This means that threads are not able to edit or change any nodes that are locked and will simply try its method call once more after the changes were complete from another thread and those nodes become unlocked. The use of this method greatly increased my runtime from minutes to seconds. 

# Part 2:
# Evaluation/Summary of approach

When approaching this problem I decided to use a strategy that involved keeping track of the # of temperature readings that each sensor has inserted into the shared memory. Since each tempertature reading is said to represent a minute, I would run the sensor threads for 60 readings for every hour the user decideds to acquire reports for. My report thread would be constantly checking once the sensor threads all acquire 60 additional readings. Once this was true the report thread would acquire the data specific to the most recent hour and compile the report. 

# Proof of correctness, efficiency and experimental evaluation

This solution meets the criteria of the problem because the only critical section is when the sensor threads add temperature readings to the shared memory, so I included a lock for this portion. The rest of the project involves some shared data but is not utilized in ways that are critical. The report thread for example waits until the readings for an entire hour are fully compiled before reading them. The sensor thread functions are extremely simple with only some thought out list manipulation occuring in the report thread function. The Program is relatively fast and prints results in ordered fashion.
