using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Ubiq.Avatars;
using Avatar = Ubiq.Avatars.Avatar;
using Ubiq.Messaging;

public class Speaker : MonoBehaviour
{
    public AvatarManager avatarManager;
    public AudioSource audioSource;

    // Start is called before the first frame update
    void Start()
    { 
        //avatarManager = transform.parent.GetComponent<AvatarManager>();
        avatarManager = gameObject.GetComponentInParent<AvatarManager>();
    }

    // Update is called once per frame
    void Update()
    {
        if (avatarManager != null) {
            // List<Avatar> list = new List<Avatar>(avatarManager.Avatars);
            // if(list.Count > 1){
            //     Transform localHead = avatarManager.LocalAvatar.transform.Find("Body/Floating_Head");
            //     Transform remoteHead;
            //     foreach(Avatar avatar in avatarManager.Avatars){
            //         if(avatar != avatarManager.LocalAvatar){
            //             remoteHead = avatar.transform.Find("Body/Floating_Head");
            //             break;
            //         }
            //     }
            //     gameObject.transform.position = localHead.position;
            //     audioSource.volume = 0.5f;
                

            // }


            foreach (Avatar avatar in avatarManager.Avatars) {
                if (avatar != avatarManager.LocalAvatar) {
                    //Transform head = avatar.transform.Find("Body/Floating_Head");
                    Transform head = avatar.transform;
                    Debug.Log("Head position: " + head);
                    gameObject.transform.position = head.position;


                    //Calculate number of objects in between both players
                    //Access position of local avatar
                    //Transform localHead = avatarManager.LocalAvatar.transform.Find("Body/Floating_Head");
                    Transform localHead = avatarManager.LocalAvatar.transform;
                    // Find vector in which the remote player is in
                    Vector3 direction = head.position - localHead.position;
                    //Distance between each player
                    float distance = direction.magnitude;
                    //Gets a list of all the objects between both players with .Length field to use
                    RaycastHit[] hits = Physics.RaycastAll(localHead.position, direction, distance);
                    Debug.Log(hits.Length);
                    audioSource.volume = 1f - (0.15f * hits.Length);

                }
            }
        } else {
            Debug.Log("avatar manager not found");
        }
        // Debug.Log("Speaker position: " + gameObject.transform.position);
    }
}
