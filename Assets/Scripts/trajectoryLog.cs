using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;
using UnityEngine.SceneManagement;

public class trajectoryLog : MonoBehaviour
{
    public string folderPath = "Assets/Logs/";
    private string filePath;
    private string remotePath;
    private AvatarManager avatarManager;

    public float writeInterval = 1f;

    private float timeElapsed = 0f;

    // Start is called before the first frame update
    void Start()
    {
        TeleportSetup teleport = transform.parent.GetComponent<TeleportSetup>();
        avatarManager = transform.parent.GetComponentInChildren<AvatarManager>();

        if (avatarManager == null)
        {
            Debug.Log("ERROR: avatar manager not found");
        }

        if (teleport == null)
        {
            Debug.Log("ERROR: teleport script not found");
        }

        int localNum = teleport.playerNum;
        int remoteNum;
        if (localNum == 1)
        {
            remoteNum = 2;
        }
        else
        {
            remoteNum = 1;
        }

        string dateTime = DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss_");
        string mode = SceneManager.GetActiveScene().name;
        string fileName = dateTime + ("player-" + localNum) + mode + ".txt";
        string remoteName = dateTime + ("remote-" + remoteNum) + mode + ".txt";
        filePath = Path.Combine(folderPath, fileName);
        remotePath = Path.Combine(folderPath, remoteName);
        WriteToFile(filePath, fileName, false);
        WriteToFile(remotePath, remoteName, false);



    }

    // Update is called once per frame
    void Update()
    {
        List<Avatar> list = new List<Avatar>(avatarManager.Avatars);
        Transform localHead = avatarManager.LocalAvatar.transform.Find("Body/Floating_Head");
        if(list.Count == 2)
        {
            timeElapsed += Time.deltaTime;
            if(timeElapsed >= writeInterval){
                timeElapsed = 0f;

                Transform remoteHead = null;
                foreach(Avatar avatar in avatarManager.Avatars){
                    if(avatar != avatarManager.LocalAvatar){
                        remoteHead = avatar.transform.Find("Body/Floating_Head");
                        break;
                    }
                }

                Vector3 direction = remoteHead.position - localHead.position;
                float distance = direction.magnitude;
                RaycastHit[] hits = Physics.RaycastAll(localHead.position, direction, distance);

                string localWrite = DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss") + "," + localHead.position.x + "," + localHead.position.z + "," + localHead.rotation.eulerAngles.y + "," + hits.Length;
                string remoteWrite = DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss") + "," + remoteHead.position.x + "," + remoteHead.position.z + "," + remoteHead.rotation.eulerAngles.y + "," + hits.Length;

                WriteToFile(filePath, localWrite);
                WriteToFile(remotePath, remoteWrite);
            }
        } 
        // else if (list.Count == 1)
        // {
        //     timeElapsed += Time.deltaTime;

        //     if (timeElapsed >= writeInterval)
        //     {
        //         timeElapsed = 0f;
        //         string toWrite = DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss") + "," + localHead.position.x + "," + localHead.position.z + "," + localHead.rotation.eulerAngles.y;
        //         WriteToFile(filePath, toWrite);
        //     }
        // }

    }


    private void WriteToFile(string path, string content, bool append = true)
    {
        StreamWriter writer = new StreamWriter(path, append);
        try
        {
            writer.WriteLine(content);
        }
        catch (Exception e)
        {
            Debug.Log("Error writing to file: " + e.Message);
        }
        finally
        {
            writer.Close();
        }
    }
}
