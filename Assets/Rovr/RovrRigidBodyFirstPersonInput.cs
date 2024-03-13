using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityStandardAssets.Characters.FirstPerson;

public class RovrRigidBodyFirstPersonInput : MonoBehaviour
{
    public RigidbodyFirstPersonController controller;
    public RovrMicrophoneManager microphone;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        controller.fAudioForce = microphone.fAudioForce;
    }
}
