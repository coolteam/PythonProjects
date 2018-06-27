import glob
from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()
for filename in glob.glob('D:/English base2cleaned&expanded_Metko/*.txt'):

    detector.reset()
    for line in open(filename, 'rb'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    if detector.result['encoding'] != 'UTF-8-SIG':
        print(filename.ljust(60))
        print(detector.result)
