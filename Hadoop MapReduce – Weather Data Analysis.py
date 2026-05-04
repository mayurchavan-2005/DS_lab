"""
Hadoop MapReduce Practical: Weather Data Analysis

This file records the Java MapReduce program details, sample weather input,
Hadoop compile/run commands, expected output, and analysis.

Files created in this folder:
WeatherAverage.java
weather_input.csv
"""


PRACTICAL = r"""
Aim:
Write a Hadoop MapReduce program to analyze weather data and compute city-wise
average temperature, dew point, and wind speed.


a) Sample Weather Input File

Sample file name:

    weather_input.csv

Sample data:

    city,temp,dew,wind
    Pune,30,18,12
    Pune,32,19,14
    Pune,31,20,13
    Mumbai,33,24,18
    Mumbai,34,25,20
    Mumbai,32,23,16
    Delhi,38,15,10
    Delhi,40,16,12
    Delhi,39,14,11
    Chennai,35,26,19
    Chennai,36,27,21
    Chennai,34,25,18


b) Mapper Class

The mapper reads each CSV line and extracts:

    city, temp, dew, wind

It emits:

    (city, "temp,dew,wind")

Example:

    Pune,30,18,12 -> (Pune, "30,18,12")

Mapper class in WeatherAverage.java:

    public static class WeatherMapper
            extends Mapper<Object, Text, Text, Text>


c) Reducer Class

The reducer receives all readings for each city and computes:

    average temperature
    average dew point
    average wind speed

Example:

    Pune -> 30,18,12
            32,19,14
            31,20,13

    Output:
    Pune    AvgTemp=31.00, AvgDew=19.00, AvgWind=13.00

Reducer class in WeatherAverage.java:

    public static class WeatherReducer
            extends Reducer<Text, Text, Text, Text>


d) Driver Class and Hadoop Run Commands

The driver configures the mapper, reducer, key/value classes, input path, and
output path.

Driver class in WeatherAverage.java:

    public static void main(String[] args) throws Exception


Steps to Compile and Run:

1. Start Hadoop services if they are not already running:

    start-dfs.sh
    start-yarn.sh

2. Create an input directory in HDFS:

    hdfs dfs -mkdir -p /weather/input

3. Upload the weather input file:

    hdfs dfs -put -f weather_input.csv /weather/input/

4. Compile the Java program:

    hadoop com.sun.tools.javac.Main WeatherAverage.java

Alternative javac command:

    javac -classpath "%HADOOP_HOME%\share\hadoop\common\*;%HADOOP_HOME%\share\hadoop\common\lib\*;%HADOOP_HOME%\share\hadoop\mapreduce\*;%HADOOP_HOME%\share\hadoop\mapreduce\lib\*" WeatherAverage.java

5. Create a JAR file:

    jar cf weatheraverage.jar WeatherAverage*.class

6. Remove existing output directory if required:

    hdfs dfs -rm -r /weather/output

7. Run the MapReduce job:

    hadoop jar weatheraverage.jar WeatherAverage /weather/input /weather/output


e) Display City-Wise Average Weather Statistics

View output directory:

    hdfs dfs -ls /weather/output

Display output:

    hdfs dfs -cat /weather/output/part-r-00000

Expected output:

    Chennai    AvgTemp=35.00, AvgDew=26.00, AvgWind=19.33
    Delhi      AvgTemp=39.00, AvgDew=15.00, AvgWind=11.00
    Mumbai     AvgTemp=33.00, AvgDew=24.00, AvgWind=18.00
    Pune       AvgTemp=31.00, AvgDew=19.00, AvgWind=13.00


Analysis:

1. Delhi has the highest average temperature among the sample cities.
2. Chennai has the highest average dew point, indicating more humid conditions.
3. Chennai also has the highest average wind speed in the sample data.
4. Pune has the lowest average temperature and wind speed among the listed
   cities.
5. The MapReduce approach is useful because the mapper extracts readings city
   wise and the reducer aggregates large volumes of weather records efficiently.


Conclusion:
The Hadoop MapReduce weather analysis program successfully computes city-wise
average temperature, dew point, and wind speed from weather input data.
"""


print(PRACTICAL)
