using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;
using Ubiq.Messaging;



public class UnityToArduino : MonoBehaviour
{
    public static string serialPortName = "COM9";
    SerialPort serialPort = new SerialPort(serialPortName, 9600); 
    // // Window use port name COMx and macOS use /dev/cu.XXX

    // Initializing Avatars

    public AvatarManager avatarManager;
    public NetworkId id1 = new NetworkId();
    public NetworkId id2 = new NetworkId();
    private int index = 0;


    void Start()
    {
        serialPort.Open();
        if (!serialPort.IsOpen){
            Debug.LogError("Failed to open serial port.");
        }
        avatarManager = GetComponent<AvatarManager>();
        }

    // Update is called once per frame
    void Update()
    {
        float xpos1 = 0;
        float ypos1 = 0;
        float dir1 = 0;

        float xpos2 = 0;
        float ypos2 = 0;
        float dir2 = 0;

        if (!serialPort.IsOpen){
            serialPort.Open();
        }

        if (avatarManager != null){            
            foreach (Avatar avatar in avatarManager.Avatars){
                if (avatar.NetworkId != null && avatar.NetworkId != id2 && id1 == null){
                    id1 = avatar.NetworkId;
                }
                else if (avatar.NetworkId != null && avatar.NetworkId != id1 && id2 == null){
                    id2 = avatar.NetworkId;
                }

                Transform ava = avatar.transform.Find("Body/Floating_Head");
                if (avatar.NetworkId == id1) {
                    xpos1 = ava.position.x;
                    ypos1 = ava.position.z;
                    dir1 = ava.rotation.eulerAngles.y;
                    
                }
                else if (avatar.NetworkId == id2) {
                    xpos2 = ava.position.x;
                    ypos2 = ava.position.z;
                    dir2 = ava.rotation.eulerAngles.y;
                }
                // Access individual avatar  
                // index++;
            }
            // index = 0;

            // Concatenate the data into string
            string data = xpos1.ToString("F2") + "," + ypos1.ToString("F2") + "," + 
                            xpos2.ToString("F2") + "," + ypos2.ToString("F2") + "," + 
                            dir1.ToString("F2") + "," + dir2.ToString("F2");

            // Send the combined data to Arduino
            serialPort.WriteLine(data);
            Debug.Log("Data sent to Arduino: " + data);
            StartCoroutine(DelayedSend(1.0f));
        }
        else {
            Debug.LogError("AvatarManager component not found on the GameObject.");
        }
    }
    IEnumerator DelayedSend(float delayInSeconds)
    {
        yield return new WaitForSeconds(delayInSeconds);
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
