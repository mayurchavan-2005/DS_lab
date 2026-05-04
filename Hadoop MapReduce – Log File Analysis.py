"""
Hadoop MapReduce Practical: Server Log File Analysis

This file records the Java MapReduce program details, Hadoop compile/run
commands, sample output, and analysis.

Java source file created in this folder:
LogLevelCount.java
"""


PRACTICAL = r"""
Aim:
Write a Hadoop MapReduce program to analyze a server log file and count the
occurrences of log levels INFO, ERROR, and WARNING.


a) Mapper Class

The mapper reads each log line, extracts the log level, and emits:

    (INFO, 1)
    (ERROR, 1)
    (WARNING, 1)

Mapper class in LogLevelCount.java:

    public static class LogLevelMapper
            extends Mapper<LongWritable, Text, Text, IntWritable>

The mapper uses this regular expression:

    \b(INFO|ERROR|WARNING)\b

This detects the first matching log level from each line.


b) Reducer Class

The reducer receives each log level with a list of counts and sums them:

    (ERROR, [1, 1, 1]) -> (ERROR, 3)

Reducer class in LogLevelCount.java:

    public static class LogLevelReducer
            extends Reducer<Text, IntWritable, Text, IntWritable>


c) Driver Class and Hadoop Run Commands

The driver configures the mapper, reducer, key/value classes, input path, and
output path.

Driver class in LogLevelCount.java:

    public static void main(String[] args) throws Exception


Steps to Compile and Run:

1. Create a sample server log file:

    notepad server.log

Example server.log:

    2026-05-04 10:00:01 INFO Server started successfully
    2026-05-04 10:01:11 WARNING Disk usage reached 80 percent
    2026-05-04 10:02:22 ERROR Database connection failed
    2026-05-04 10:03:14 INFO User login successful
    2026-05-04 10:04:07 ERROR Request timeout
    2026-05-04 10:05:30 WARNING High memory usage detected
    2026-05-04 10:06:45 INFO Backup completed

2. Start Hadoop services if they are not already running:

    start-dfs.sh
    start-yarn.sh

3. Create an input directory in HDFS:

    hdfs dfs -mkdir -p /loganalysis/input

4. Upload the log file to HDFS:

    hdfs dfs -put -f server.log /loganalysis/input/

5. Compile the Java program:

    hadoop com.sun.tools.javac.Main LogLevelCount.java

Alternative javac command:

    javac -classpath "%HADOOP_HOME%\share\hadoop\common\*;%HADOOP_HOME%\share\hadoop\common\lib\*;%HADOOP_HOME%\share\hadoop\mapreduce\*;%HADOOP_HOME%\share\hadoop\mapreduce\lib\*" LogLevelCount.java

6. Create a JAR file:

    jar cf loglevelcount.jar LogLevelCount*.class

7. Remove existing output directory if required:

    hdfs dfs -rm -r /loganalysis/output

8. Run the MapReduce job:

    hadoop jar loglevelcount.jar LogLevelCount /loganalysis/input /loganalysis/output


d) Display Count of Each Log Level

View output directory:

    hdfs dfs -ls /loganalysis/output

Display output:

    hdfs dfs -cat /loganalysis/output/part-r-00000

Sample output:

    ERROR      2
    INFO       3
    WARNING    2


Analysis:

1. INFO appears 3 times, showing normal successful operations such as server
   startup, user login, and backup completion.
2. WARNING appears 2 times, showing conditions that need attention but may not
   have stopped the application.
3. ERROR appears 2 times, showing failed operations such as database connection
   failure and request timeout.
4. If ERROR count is high, administrators should inspect those log entries first
   because they indicate failures.
5. WARNING entries should also be monitored because repeated warnings can later
   become errors.


Conclusion:
The Hadoop MapReduce log analysis program successfully extracts log levels from
server log lines and counts the occurrences of INFO, ERROR, and WARNING using
Mapper, Reducer, and Driver classes.
"""


print(PRACTICAL)
