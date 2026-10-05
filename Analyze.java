import java.io.*;
import java.util.*;

public class Analyze {

    public static void main(String[] args) throws Exception {

        String[] listTypes = {"ArrayList", "LinkedList"};
        int[] sizes = {500, 5000, 50000, 500000};
        int repeats = 10;

        for (int t = 0; t < listTypes.length; t++) {
            for (int s = 0; s < sizes.length; s++) {

                String type = listTypes[t];
                int size = sizes[s];

                // energy per list of every run = total energy / lists built
                double[] energy = new double[repeats];
                for (int run = 1; run <= repeats; run++) {
                    String fileName = "results_list_java_12s/" + type + "_" + size + "_run" + run + ".txt";
                    String countName = "results_list_java_12s/" + type + "_" + size + "_run" + run + "_count.txt";
                    BufferedReader countReader = new BufferedReader(new FileReader(countName));
                    int listsBuilt = Integer.parseInt(countReader.readLine().trim());
                    countReader.close();
                    energy[run - 1] = getEnergy(fileName) / listsBuilt;
                }

                // sort, then remove 2 lowest and 2 highest (4 outliers)
                Arrays.sort(energy);
                double sum = 0;
                for (int i = 2; i < repeats - 2; i++) {
                    sum = sum + energy[i];
                }
                double average = sum / (repeats - 4);

                System.out.println(type + " " + size + " average energy per list = " + average + " J");
            }
        }
    }

    // energy (joules) of one run = sum of power * time for every sample
    static double getEnergy(String fileName) throws Exception {
        BufferedReader reader = new BufferedReader(new FileReader(fileName));
        reader.readLine(); // skip header line

        double energy = 0;
        double sampleTime = 0.000125; // 125 microseconds per sample

        String line = reader.readLine();
        while (line != null) {
            String[] parts = line.trim().split(" ");
            double l1mA = Double.parseDouble(parts[1]);
            double l1mV = Double.parseDouble(parts[2]);
            double l2mA = Double.parseDouble(parts[3]);
            double l2mV = Double.parseDouble(parts[4]);
            double l3mA = Double.parseDouble(parts[5]);
            double l3mV = Double.parseDouble(parts[6]);

            // mA * mV = microwatts, divide by 1,000,000 to get watts
            double power = (l1mA * l1mV + l2mA * l2mV + l3mA * l3mV) / 1000000;
            energy = energy + power * sampleTime;

            line = reader.readLine();
        }

        reader.close();
        return energy;
    }
}
