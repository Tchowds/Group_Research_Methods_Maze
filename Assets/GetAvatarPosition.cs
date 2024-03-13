using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;

public class GetAvatarPosition : MonoBehaviour
{
    Avatar myAvatar;
    Avatar myAvatar2;
    AvatarManager myAvatarManager;


    void Start()
    {
         myAvatarManager = GetComponent<AvatarManager>();
    }

    void Update()
    {
        myAvatar = myAvatarManager.GetComponentInChildren<Avatar>();
        GameObject head = GameObject.Find("Floating_Head");
        Debug.Log("Position = " + head.transform.position);
        }
}
