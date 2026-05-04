import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WeatherAverage {
    public static class WeatherMapper
            extends Mapper<Object, Text, Text, Text> {

        private final Text cityName = new Text();
        private final Text weatherValues = new Text();

        @Override
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString().trim();

            if (line.isEmpty() || line.toLowerCase().startsWith("city,")) {
                return;
            }

            String[] columns = line.split(",");

            if (columns.length == 4) {
                String city = columns[0].trim();
                String temp = columns[1].trim();
                String dew = columns[2].trim();
                String wind = columns[3].trim();

                cityName.set(city);
                weatherValues.set(temp + "," + dew + "," + wind);
                context.write(cityName, weatherValues);
            }
        }
    }

    public static class WeatherReducer
            extends Reducer<Text, Text, Text, Text> {

        private final Text result = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {

            double tempSum = 0.0;
            double dewSum = 0.0;
            double windSum = 0.0;
            int count = 0;

            for (Text value : values) {
                String[] readings = value.toString().split(",");

                if (readings.length == 3) {
                    tempSum += Double.parseDouble(readings[0]);
                    dewSum += Double.parseDouble(readings[1]);
                    windSum += Double.parseDouble(readings[2]);
                    count++;
                }
            }

            if (count > 0) {
                double avgTemp = tempSum / count;
                double avgDew = dewSum / count;
                double avgWind = windSum / count;

                result.set(String.format(
                        "AvgTemp=%.2f, AvgDew=%.2f, AvgWind=%.2f",
                        avgTemp,
                        avgDew,
                        avgWind));
                context.write(key, result);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: WeatherAverage <input path> <output path>");
            System.exit(-1);
        }

        Configuration configuration = new Configuration();
        Job job = Job.getInstance(configuration, "City Wise Weather Average");

        job.setJarByClass(WeatherAverage.class);
        job.setMapperClass(WeatherMapper.class);
        job.setReducerClass(WeatherReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
