using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;

public class set_headset : MonoBehaviour
{
    // Start is called before the first frame update

    void Start()
    {
        transform.rotation = InputTracking.GetLocalRotation(XRNode.Head);
    }

    // Update is called once per frame
    void Update()
    {
        transform.rotation = InputTracking.GetLocalRotation(XRNode.Head);
        Debug.Log(transform.rotation);
    }
}
