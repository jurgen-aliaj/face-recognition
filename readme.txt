The script 'faces.py' takes 3 arguments. 
The first is either 'face' or 'gender' which specifies that you are doing face or gender classification respectively.
The second is 'training' or 'validation' or 'testing' which shows results for the training, validation, and testing sets respectively.
The third is a positive integer between 1 and 600, which specifies the k-value for k nearest neighbours.
The script outputs the accuracy for the given k, and if in testing mode it will output 5 failure cases.
In addition, the script outputs results for testing, training, and validation for various different k values.
The produced graph gets data from a file ('results.p'), which I prepared before hand since running the script for every value of k takes too long.
To run faces.py, you must make sure you have folders training, validation, and testing (in root directory) with the cropped 32x32 grayscale images.
I followed a slightly different naming convention for images compared to the script given in the assignment.
The image names have the format 'name_gender_i.format' (e.g. radcliffe_male_38.jpg). 
Please make sure to account for this before running the script.
If there are no training, validation, or testing sets then to create them there is a script named make_split.sh in the tools folder.
In order to run make_split.sh, you simply need a folder named 'cropped' with at least 120 images of each actor with the above naming conventions.
You can either generate the cropped folder yourself or use the get_data.py script under tools which I modified from the course website.
The make_split.sh file does not implement randomization in making the split.
It simply puts the first 100 images of each actor into the training folder, the next 10 into validation, and the next 10 into testing.
To see the results for part 6 of the assignment, simply run faces.py as before with the appropriate validation and testing sets for other actors.
To generate these validation and testing sets, there is a bash script make_other_spit.sh in the tools folder which requires a folder others_cropped.
The others_cropped folder should contain 32x32 grayscale images of the other actors with naming conventions as above.
If there is no such folder, the script get_others.py will generate one (requires 'others_cropped' folder exists before running).
