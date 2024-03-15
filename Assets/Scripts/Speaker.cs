using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;
using Ubiq.Messaging;

public class Speaker : MonoBehaviour
{
    public AvatarManager avatarManager;

    // Start is called before the first frame update
    void Start()
    {
        // avatarManager = transform.parent.GetComponent<AvatarManager>();
    }

    // Update is called once per frame
    void Update()
    {
        if (avatarManager != null) {
            Transform head;
            foreach (Avatar avatar in avatarManager.Avatars) {
                if (avatar != avatarManager.LocalAvatar) {
                    head = avatar.transform.Find("Body/Floating_Head");
                    Debug.Log("Head position: " + head);
                    gameObject.transform.position = head.position;
                }
            }
        } else {
            Debug.Log("avatar manager not found");
        }
        Debug.Log("Speaker position: " + gameObject.transform.position);
    }
}
