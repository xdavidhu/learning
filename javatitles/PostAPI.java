package tk.ckdeveloper.javatitles;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.Charset;

 /**
  * @author xdavidhu
  */

public class PostAPI {

    public static String encryption;
    public static String ip;
    public static String pathToPage;
    public static String pageName;
    public static String args;

    /**
     * @param encryptionIn "http" or "https" <-- Method to connect to the site
     * @param ipIn "192.168.0.1" <-- The ip of the site
     * @param pathToPageIn "/api/" <-- Path to the page
     * @param pageNameIn "postreciever" <-- Name of the page (Don't need '.php'!)
     * @param argsIn "username=" + username + "&password=" + password <-- This is the date for the post
     */

   public static void postToPage(String encryptionIn, String ipIn, String pathToPageIn, String pageNameIn, String argsIn){

       /*

        Made by @xdavidhu -> CKDev

        Documentation / Examples:

        encryptionIn = "http" or "https" <-- Method to connect to the site
        ipIn = "192.168.0.1" <-- The ip of the site
        pathToPageIn = "/api/" <-- Path to the page
        pageNameIn = "postreciever" <-- Name of the page (Don't need '.php'!)
        args = "username=" + username + "&password=" + password <-- This is the date for the post

        */

       PostAPI.encryption = encryptionIn;
       PostAPI.ip = ipIn;
       PostAPI.pathToPage = pathToPageIn;
       PostAPI.pageName = pageNameIn;
       PostAPI.args = argsIn;

       HttpURLConnection conn = connect();
       BufferedReader in = null;
       try {
           in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
       } catch (IOException e) {
           e.printStackTrace();
       }
       String data = null;
       try {
           data = in.readLine();
       } catch (IOException e) {
           e.printStackTrace();
       }
       System.out.println(data);

   }



    private static HttpURLConnection connect() {
        try {

            String encryptionHelper;

            if (encryption.equalsIgnoreCase("http")){
                encryptionHelper = "http://";
            }
            else {
                encryptionHelper = "https://";
            }

            byte[] data = args.getBytes(Charset.forName("UTF-8"));
            int dataLength = args.length();
            String request = encryptionHelper + ip + pathToPage + pageName + ".php";
            URL url = new URL(request);

            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoInput(true);
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setRequestProperty("charset", "UTF-8");
            connection.setRequestProperty("Content-Length", String.valueOf(dataLength));

            DataOutputStream out = new DataOutputStream(connection.getOutputStream());
            out.write(data);
            out.flush();
            out.close();

            return connection;
        }

        catch (Exception e) {
            e.printStackTrace();

            return null;
        }
    }

}
