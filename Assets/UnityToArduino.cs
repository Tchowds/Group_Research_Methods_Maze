using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;
using System.IO;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;
using Ubiq.Messaging;
using System;



public class UnityToArduino : MonoBehaviour
{
    public static string serialPortName = "/dev/cu.usbmodem2101";
    SerialPort serialPort = new SerialPort(serialPortName, 9600); 
    // Window use port name COMx and macOS use /dev/cu.XXX

    // Initializing Avatars

    public AvatarManager avatarManager;
    public NetworkId id1 = new NetworkId();
    public NetworkId id2 = new NetworkId();

    // Time interval to log data
    private float timer = 0f;
    private float logInterval = .5f; 
    private string userid =  Guid.NewGuid().ToString();


    void Start()
    {
        serialPort.Open();
        if (!serialPort.IsOpen){
            Debug.LogError("Failed to open serial port.");
        }
        avatarManager = GetComponent<AvatarManager>();
        // InvokeRepeating("SendDataToArduino", 1f, 1f);
    }

    static float DotProduct(float[] vector1, float[] vector2)
    {
        float result = 0.0f;
        for (int i = 0; i < vector1.Length; i++)
        {
            result += vector1[i] * vector2[i];
        }
        return result;
    }
    

    // Update is called once per frame
    void Update()
    {
        float xpos1 = 0;
        float ypos1 = 0;
        float rd1 = 0;

        float xpos2 = 0;
        float ypos2 = 0;
        float rd2 = 0;

        if (!serialPort.IsOpen){
            serialPort.Open();
        }

        if (avatarManager != null){            
            foreach (Avatar avatar in avatarManager.Avatars){
                if (avatar.NetworkId != null && avatar.NetworkId != id2 && id1 == new NetworkId()){
                    id1 = avatar.NetworkId;
                }
                else if (avatar.NetworkId != null && avatar.NetworkId != id1 && id2 == new NetworkId()){
                    id2 = avatar.NetworkId;
                }

                Transform ava = avatar.transform.Find("Body/Floating_Head");
                if (avatar.NetworkId == id1) {
                    xpos1 = ava.position.x;
                    ypos1 = ava.position.z;
                    rd1 = ava.rotation.eulerAngles.y;
                    
                }
                else if (avatar.NetworkId == id2) {
                    xpos2 = ava.position.x;
                    ypos2 = ava.position.z;
                    rd2 = ava.rotation.eulerAngles.y;
                }

            }

            // // Concatenate the data into string
            // string data = xpos1.ToString("F2") + "," + ypos1.ToString("F2") + "," + 
            //                 xpos2.ToString("F2") + "," + ypos2.ToString("F2") + "," + 
            //                 dir1.ToString("F2") + "," + dir2.ToString("F2");

            
            float rdir1 = ((rd1 + 270.0f) % 360.0f) * (float)(Math.PI / 180.0);
            float rdir2 = ((rd2 + 270.0f) % 360.0f) * (float)(Math.PI / 180.0);

            float diff_x = -xpos1 + xpos2;
            float diff_y = -ypos1 + ypos2;

            float[] p1_facing_dir = {(float)Math.Cos(rdir1), (float)Math.Sin(rdir1 - Math.PI)};
            float[] p2_facing_dir = { (float)Math.Cos(rdir2), (float)Math.Sin(rdir2 - Math.PI) };
            
            float[] p1_p2_vect = {diff_x, diff_y};

            float dot = DotProduct(p1_facing_dir, p1_p2_vect);

            float magA = (float)Math.Sqrt(p1_facing_dir[0] * p1_facing_dir[0] + p1_facing_dir[1] * p1_facing_dir[1]);
            float magB = (float)Math.Sqrt(p1_p2_vect[0] * p1_p2_vect[0] + p1_p2_vect[1] * p1_p2_vect[1]);

            float dot_denom = magA * magB;

            float theta = (float)(Math.Acos(dot / dot_denom) * (180.0 / Math.PI));
            
            // if ((ypos1 < ypos2 && theta > rd1) || (ypos1 > ypos2 && theta < rd1) || 
            //     (xpos1 < xpos2 && theta < rd1) || (xpos1 > xpos2 && theta > rd1))
            // {
            //     theta = 360.0f - theta;
            // }

            // float dotperp = p1_p2_vect[0] * p1_facing_dir[0] - p1_p2_vect[1] * p1_facing_dir[1];
            float dotperp = p1_p2_vect[0] * p1_facing_dir[1] - p1_p2_vect[1] * p1_facing_dir[0];
            // float dotperp = p1_p2_vect[1] * p1_facing_dir[0] - p1_p2_vect[0] * p1_facing_dir[1];


            if((dot > 0 && dotperp < 0) || (dot < 0 && dotperp <0)){
                theta = 360.0f - theta;
            }
            
            string data = "";

            if (theta <= 10.0f || theta >= 350.0f){
                float diff_x2 = -xpos2 + xpos1;
                float diff_y2 = -ypos2 + ypos1;
                float[] p2_p1_vect = { diff_x2, diff_y2 };
                float dot2 = DotProduct(p2_facing_dir, p2_p1_vect);

                float magA2 = (float)Math.Sqrt(p2_facing_dir[0] * p2_facing_dir[0] + p2_facing_dir[1] * p2_facing_dir[1]);

                float dot_denom2 = magA2 * magB;
                float theta2 = (float)(Math.Acos(dot2 / dot_denom2) * (180.0 / Math.PI));

                // float dotperp2 = p1_p2_vect[1] * p2_facing_dir[0] - p1_p2_vect[0] * p2_facing_dir[1];
                float dotperp2 = p1_p2_vect[0] * p2_facing_dir[1] - p1_p2_vect[1] * p2_facing_dir[0];
                if((dot2 > 0 && dotperp2 < 0) || (dot2 < 0 && dotperp2 <0)){
                    theta2 = 360.0f - theta2;
                }

                if (theta2 >= 350.0f || theta2 <= 10.0f){
                    float ratio = (float)Math.Sqrt(20000) / magB;
                    int delayVal = ((int) (1800 * ratio)) + 200 ;
                    data = delayVal.ToString();
                    // data = "N";
                }
                else {
                    data = "N";
                }
            }

            else{
                if (theta <= 22.5 || theta > 337.5){
                    // Angle is within the range of the north direction
                    data = "N";
                }

                else if (22.5 < theta && theta <= 67.5){
                    // Angle is within *range* degrees to the northeast direction
                    data = "NE";
                }

                else if (67.5 < theta && theta <= 112.5){
                    // Angle is within *range* degrees to the east direction
                    data = "E";
                }

                else if (112.5 < theta && theta <= 157.5){
                    // Angle is within *range* degrees to the southeast direction
                    data = "SE";
                }

                else if (157.5 < theta && theta <= 202.5){
                    // Angle is within *range* degrees to the south direction
                    data = "S";
                }

                else if (202.5 < theta && theta <= 247.5){
                    // Angle is within *range* degrees to the southwest direction
                    data = "SW";
                }

                else if (247.5 < theta && theta <= 292.5){
                    // Angle is within *range* degrees to the west direction
                    data = "W";
                }

                else if (292.5 < theta && theta <= 337.5){
                    // Angle is within *range* degrees to the northwest direction
                    data = "NW";
                }
            

            }
            // Send the combined data to Arduino
            Debug.Log("Data sent to Arduino: " + data);
            serialPort.WriteLine(data);

            timer += Time.deltaTime;
            if (timer >= logInterval)
            {
                Debug.Log("Dir: "+ rd1 +"Data Logged: " + data);
                timer = 0f;
                string datalog = DateTime.Now + " " + rd1 + " " + data ;
                string filePath = "userid_" + userid + "_data.txt";
                using (StreamWriter writer = File.AppendText(filePath))
                {
                    writer.WriteLine(datalog);
                }
            }
        }
        else {
            Debug.LogError("AvatarManager component not found on the GameObject.");
        }
    }

    static bool FacingSameDirection(float[] dir1, float[] dir2, float[] dir3)
    {
        Normalize(dir1);
        Normalize(dir2);
        Normalize(dir3);

        float dotProd = DotProduct(dir1, dir2);

        // Check if dir3 is equal to dir1 with a tolerance
        bool equal = true;
        for (int i = 0; i < dir3.Length; ++i)
        {
            if (Math.Abs(dir3[i] - dir1[i]) > 0.001)
            {
                equal = false;
                break;
            }
        }

        if (Math.Abs(dotProd) == 1 && equal)
        {
            return true;
        }
        return false;
    }

    static void Normalize(float[] vector)
    {
        // Calculate magnitude
        float magnitude = 0;
        for (int i = 0; i < vector.Length; i++)
        {
            magnitude += vector[i] * vector[i];
        }
        magnitude = (float)Math.Sqrt(magnitude);

        // Normalize vector
        for (int i = 0; i < vector.Length; i++)
        {
            vector[i] /= magnitude;
        }
    }

    void OnDestroy()
    {
        // Release the serial port when the script or application is destroyed
        if (serialPort != null && serialPort.IsOpen)
        {
            serialPort.Close();
            Debug.Log("Serial port closed.");
        }
    }
}