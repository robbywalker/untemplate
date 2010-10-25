""" a script to test parsing on comcast documents """
from untemplate import getData

def testComcast():
	file1 = open("documents/comcast-statement1.txt").read()
	file2 = open("documents/comcast-statement2.txt").read()
	file3 = open("documents/comcast-statement3.txt").read()
	print getData(file1, file2, file3)


if __name__ == "__main__":
	testComcast()
