from pyspark import  SparkContext
from operator import add

def tokenize(text):
    return text.split()

sc = SparkContext( 'local', 'pyspark')

text = sc.textFile('alice_in_wonderland.txt')
print(text)

words = text.flatMap(tokenize)
print(words)

wc = words.map(lambda x: (x, 1))

counts = wc.reduceByKey(add)
counts.saveAsTextFile("wc")