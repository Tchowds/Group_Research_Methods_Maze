using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;

public class SpawnTeleporter : MonoBehaviour
{
    // Start is called before the first frame update
    private AvatarManager avatarManager;
    private Avatar local;
    private bool confirm;
    void Start()
    {
        avatarManager = GetComponent<AvatarManager>();
        local = avatarManager.LocalAvatar;
        confirm = true;

    }

    // Update is called once per frame
    void Update()
    {
        if(avatarManager != null){
            if(confirm){
                foreach(Avatar avatar in avatarManager.Avatars){
                    // avatar.transform.Find("Body/Floating_Head").transform.position = new Vector3(-2,0,0);
                    // Debug.Log("avatar pos" + avatar.transform.Find("Body/Floating_Head").transform.position);
                    // confirm = false;
                    GameObject avatarObject = avatar.gameObject;
                    // avatarObject.transform.position = new Vector3(-2f,1f,-2f);
                    
                    Transform head = avatarObject.transform.Find("Body/Floating_Head");
                    GameObject floating = head.gameObject;
                    // floating.transform.position = new Vector3(-2f,1f,-2f);
                    // head.position = new Vector3(-2f,1f,-2f);
                    Debug.Log("Avatar: " + avatar + "\n Position: " + floating.transform.position);
                    // Debug.Log("avatar = " + avatarObject);
                    // confirm = false;
                }
            }
        }



                    

    }
}
