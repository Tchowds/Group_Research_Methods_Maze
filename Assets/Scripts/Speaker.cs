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

    public AudioClip audioClip1;
    public AudioClip audioClip2;

    private bool facing_towards = true;
    // Start is called before the first frame update
    void Start()
    {
        // avatarManager = transform.parent.GetComponent<AvatarManager>();
        audioSource.clip = audioClip1;
        audioSource.Play();

    }

    // Update is called once per frame
    void Update()
    {
        if (avatarManager != null) {
            foreach (Avatar avatar in avatarManager.Avatars) {
                if (avatar != avatarManager.LocalAvatar) {
                    Transform remoteHead = avatar.transform.Find("Body/Floating_Head");
                    Debug.Log("Remote Head position: " + remoteHead);
                    gameObject.transform.position = remoteHead.position;
                    //Calculate number of objects in between both players
                    //Access position of local avatar
                    Transform localHead = avatarManager.LocalAvatar.transform.Find("Body/Floating_Head");
                    Debug.Log("Local Head position: " + localHead);
                    // Find vector in which the remote player is in
                    Vector3 direction = remoteHead.position - localHead.position;
                    float angle = Vector3.Angle(localHead.forward, direction);
                    if (angle < 90 && !facing_towards) {
                        // Debug.Log("facing towards");
                        audioSource.clip = audioClip1;
                        facing_towards = true;
                        audioSource.Play();
                    } else if (angle >= 90 && facing_towards) {
                        // Debug.Log("facing away");
                        audioSource.clip = audioClip2;
                        facing_towards = false;
                        audioSource.Play();
                    }
                    Debug.Log("Angle: " + angle);
                    //Distance between each player
                    float distance = direction.magnitude;
                    Debug.Log("Distance to other player: " + distance);
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
