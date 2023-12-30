import os

def generate_negative_description_file():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

#generate_negative_description_file()


#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=positive/
#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 100 -vec pos.vec
#C:/Users/Anwender/Desktop/Cascading/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data  cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 7 -numNeg 30 -numStages 12 -maxFalseAlarmRate 0.3 -minHitRate.999
            