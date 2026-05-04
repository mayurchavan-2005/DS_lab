import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class LogLevelCount {
    public static class LogLevelMapper
            extends Mapper<LongWritable, Text, Text, IntWritable> {

        private static final Pattern LOG_LEVEL_PATTERN =
                Pattern.compile("\\b(INFO|ERROR|WARNING)\\b");
        private static final IntWritable ONE = new IntWritable(1);
        private final Text logLevel = new Text();

        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString().toUpperCase();
            Matcher matcher = LOG_LEVEL_PATTERN.matcher(line);

            if (matcher.find()) {
                logLevel.set(matcher.group(1));
                context.write(logLevel, ONE);
            }
        }
    }

    public static class LogLevelReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private final IntWritable result = new IntWritable();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {

            int sum = 0;
            for (IntWritable value : values) {
                sum += value.get();
            }

            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: LogLevelCount <input path> <output path>");
            System.exit(-1);
        }

        Configuration configuration = new Configuration();
        Job job = Job.getInstance(configuration, "Server Log Level Count");

        job.setJarByClass(LogLevelCount.class);
        job.setMapperClass(LogLevelMapper.class);
        job.setReducerClass(LogLevelReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
