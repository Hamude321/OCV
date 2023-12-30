import os
import subprocess

def replace_backslash_with_slash():
    search_text = "\\"
    replace_text = "/"

    #read file
    with open(r'pos.txt', 'r') as file: 
        data = file.read() 
        data = data.replace(search_text, replace_text) 

    #write file
    with open(r'pos.txt', 'w') as file: 
        file.write(data) 

def generate_negatives():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

def generate_positives():
    subprocess.run('C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=positive/')
    replace_backslash_with_slash()

def generate_vector_from_positives(num=100, width =24, height=24):
    subprocess.run('C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w {} -h {} -num {} -vec pos.vec'.format(width,height, num))

def run_machine_learning(stages = 5, numPos = 7, numNeg = 30, width = 24, height = 24, maxFalseAlarmRate = 0.3, minHitRate = 0.8 ):
    subprocess.run('C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data  cascade/ -vec pos.vec -bg neg.txt -w {} -h {} -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos {} -numNeg {} -numStages {} -maxFalseAlarmRate {} -minHitRate {}'.format(width, height, numPos, numNeg, stages, maxFalseAlarmRate, minHitRate))

#generate_negatives()
#generate_positives()
#generate_vector_from_positives()
run_machine_learning()
    
#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=positive/
#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 100 -vec pos.vec
#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 7 -numNeg 30 -numStages 12 -maxFalseAlarmRate 0.3 -minHitRate.999

#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=positive/
#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 100 -vec pos.vec            