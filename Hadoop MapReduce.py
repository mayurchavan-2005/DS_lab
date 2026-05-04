"""
Hadoop MapReduce Practical: WordCount

This file records the program, compilation commands, HDFS run commands, and
sample output for a Hadoop MapReduce WordCount practical.

Java source file created in this folder:
WordCount.java
"""


PRACTICAL = r"""
Aim:
Write a Hadoop MapReduce program in Java to perform WordCount on a text file.


a) Mapper Class

The mapper reads each input line, tokenizes it into words, and emits:

    (word, 1)

Mapper code is available in WordCount.java as:

    public static class WordCountMapper
            extends Mapper<Object, Text, Text, IntWritable>


b) Reducer Class

The reducer receives each word with a list of counts and sums them:

    (word, [1, 1, 1]) -> (word, total_count)

Reducer code is available in WordCount.java as:

    public static class WordCountReducer
            extends Reducer<Text, IntWritable, Text, IntWritable>


c) Driver Class

The driver configures and submits the MapReduce job:

    Job job = Job.getInstance(configuration, "Word Count");
    job.setJarByClass(WordCount.class);
    job.setMapperClass(WordCountMapper.class);
    job.setReducerClass(WordCountReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);


d) Compile, Create JAR, and Run on Hadoop HDFS

1. Create a sample input file:

    notepad input.txt

Example input:

    Hadoop is fast
    Hadoop is scalable
    MapReduce counts words

2. Start Hadoop services if they are not already running:

    start-dfs.sh
    start-yarn.sh

3. Create input directory in HDFS:

    hdfs dfs -mkdir -p /wordcount/input

4. Upload input file to HDFS:

    hdfs dfs -put -f input.txt /wordcount/input/

5. Compile the Java program:

    hadoop com.sun.tools.javac.Main WordCount.java

Alternative if the above command is unavailable:

    javac -classpath "%HADOOP_HOME%\share\hadoop\common\*;%HADOOP_HOME%\share\hadoop\common\lib\*;%HADOOP_HOME%\share\hadoop\mapreduce\*;%HADOOP_HOME%\share\hadoop\mapreduce\lib\*" WordCount.java

6. Create the JAR file:

    jar cf wordcount.jar WordCount*.class

7. Remove old output directory if it already exists:

    hdfs dfs -rm -r /wordcount/output

8. Run the MapReduce job:

    hadoop jar wordcount.jar WordCount /wordcount/input /wordcount/output


e) View and Record the Output

View the output files:

    hdfs dfs -ls /wordcount/output

Display the final WordCount result:

    hdfs dfs -cat /wordcount/output/part-r-00000

Sample output:

    counts      1
    fast        1
    hadoop      2
    is          2
    mapreduce   1
    scalable    1
    words       1


Conclusion:
The Hadoop MapReduce WordCount program successfully tokenizes text input,
emits word-count pairs from the mapper, sums counts in the reducer, and stores
the final output in HDFS.
"""


print(PRACTICAL)
