using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;

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
        
        if(avatarManager == null){
            Debug.Log("ERROR: avatar manager not found");
        }
            
        if(teleport == null){
            Debug.Log("ERROR: teleport script not found");
        }
            

        string dateTime = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
        string fileName = ("player-" + teleport.playerNum) + ".txt";
        string remoteName = ("remote-" + teleport.playerNum) + ".txt";
        filePath = Path.Combine(folderPath, fileName);
        remotePath = Path.Combine(folderPath, remoteName);
        WriteToFile(filePath, fileName, false);
        WriteToFile(remotePath, remoteName, false);

        

    }

    // Update is called once per frame
    void Update()
    {
        List<Avatar> list = new List<Avatar>(avatarManager.Avatars);
        if(list.Count > 1){
            timeElapsed += Time.deltaTime;

            if(timeElapsed >= writeInterval){
                timeElapsed = 0f;

                foreach(Avatar avatar in avatarManager.Avatars){
                    if(avatar == avatarManager.LocalAvatar){
                        //Transform posHead = avatarManager.LocalAvatar.transform.Find("Body/Floating_Head");
                        Transform posHead = avatarManager.LocalAvatar.transform;
                        string toWrite = posHead.position.x + "," + posHead.position.z + "," + posHead.rotation.eulerAngles.y;
                        WriteToFile(filePath, toWrite);

                    } else{
                        //Transform posHead = avatar.transform.Find("Body/Floating_Head");
                        Transform posHead = avatar.transform;
                        string toWrite = posHead.position.x + "," + posHead.position.z + "," + posHead.rotation.eulerAngles.y;
                        WriteToFile(remotePath, toWrite);
                    }
                }
            }
        }

    }


    private void WriteToFile(string path, string content, bool append = true){
        StreamWriter writer = new StreamWriter(path, append);
        try{
            writer.WriteLine(content);
        } catch (Exception e){
            Debug.Log("Error writing to file: " + e.Message);
        } finally{
            writer.Close();
        }
    }
}
