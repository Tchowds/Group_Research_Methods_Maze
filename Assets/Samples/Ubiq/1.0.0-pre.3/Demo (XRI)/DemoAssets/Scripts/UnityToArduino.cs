using System.Collections;
using System.Collections.Generic;
using UnityEngine;
// using System.IO.Ports;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;


public class UnityToArduino : MonoBehaviour
{

    private AvatarManager avatarManager;

    void Start()
    {
        avatarManager = GetComponent<AvatarManager>();
        Avatar local = avatarManager.LocalAvatar;
        // Debug.Log("local avater = " + local);

    }

    // Update is called once per frame
    void Update()
    {

        if (avatarManager != null){
            foreach (Avatar avatar in avatarManager.Avatars){
                // Debug.Log("Avatars: " + avatar);
                //avatar doesnt work, avatar position doesnt work, avatar transform position doesnt work
                // Debug.Log("Avater.position" + avatar.Position);
                
                // GameObject head = GameObject.Find("Floating_Head");
                Transform head = avatar.transform.Find("Body/Floating_Head");
                Debug.Log("Avatar: " + avatar + "\n Position: " + head.position );
                
            }
        }
        else {
            Debug.LogError("AvatarManager component not found on the GameObject.");
        }
    }
}
