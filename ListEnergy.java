import java.io.*;
import java.net.Socket;
import java.util.*;

public class ListEnergy {

    static String DEVICE = "USB::QTL2843-03-023";
    static Socket socket;
    static InputStream in;
    static OutputStream out;

    public static void main(String[] args) throws Exception {

        // connect to QIS (QIS must already be running)
        socket = new Socket("127.0.0.1", 9722);
        in = socket.getInputStream();
        out = socket.getOutputStream();

        sendCommand("$scan");
        Thread.sleep(3000);

        new File("results_list_java_12s").mkdir();

        int[] sizes = {500, 5000, 50000, 500000};
        int repeats = 10;

        // ArrayList experiments
        for (int s = 0; s < sizes.length; s++) {
            for (int run = 1; run <= repeats; run++) {
                runExperiment(new ArrayList<Integer>(), "ArrayList", sizes[s], run);
            }
        }

        // LinkedList experiments
        for (int s = 0; s < sizes.length; s++) {
            for (int run = 1; run <= repeats; run++) {
                runExperiment(new LinkedList<Integer>(), "LinkedList", sizes[s], run);
            }
        }

        socket.close();
        System.out.println("Done");
    }

    // one run: record with quarch while adding elements at index 0
    static void runExperiment(List<Integer> list, String type, int size, int run) throws Exception {
        System.out.println("Running " + type + " size " + size + " run " + run);

        // start recording
        sendCommand(DEVICE + " rec stream");
        Thread.sleep(1000);

        // the experiment: for 12 seconds, keep building a new list
        // (add elements at index 0) and count how many lists we built
        long startTime = System.currentTimeMillis();
        int listsBuilt = 0;
        while (System.currentTimeMillis() - startTime < 12000) {
            list.clear();
            for (int i = 0; i < size; i++) {
                list.add(0, i);
            }
            listsBuilt++;
        }
        System.out.println("  lists built in 12 s: " + listsBuilt);

        // stop recording
        Thread.sleep(1000);
        sendCommand(DEVICE + " rec stop");
        Thread.sleep(1000);

        // save the raw quarch data to a file
        saveData("results_list_java_12s/" + type + "_" + size + "_run" + run + ".txt");

        // save how many lists were built
        PrintWriter countFile = new PrintWriter("results_list_java_12s/" + type + "_" + size + "_run" + run + "_count.txt");
        countFile.println(listsBuilt);
        countFile.close();
    }

    // send a command to QIS and return the reply (QIS replies end with '>')
    static String sendCommand(String command) throws Exception {
        out.write((command + "\r\n").getBytes());
        out.flush();

        StringBuilder reply = new StringBuilder();
        int c = in.read();
        while (c != '>') {
            reply.append((char) c);
            c = in.read();
        }
        return reply.toString();
    }

    // read all recorded data from QIS and write it to a file
    static void saveData(String fileName) throws Exception {
        PrintWriter file = new PrintWriter(fileName);
        file.println("time_us L1_mA L1_mV L2_mA L2_mV L3_mA L3_mV Neutral_mA");

        String data = sendCommand(DEVICE + " stream text all");
        while (!data.contains("eof")) {
            file.print(data);
            data = sendCommand(DEVICE + " stream text all");
        }
        file.println(data.replace("eof", "").trim());

        file.close();
    }
}
