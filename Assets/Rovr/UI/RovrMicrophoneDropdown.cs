using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class RovrMicrophoneDropdown : MonoBehaviour
{
    private Dropdown dropdown;
    private RovrMicrophoneManager rovr;

    private void Awake()
    {
        rovr = FindObjectOfType<RovrMicrophoneManager>();
        dropdown = GetComponent<Dropdown>();
    }

    // Start is called before the first frame update
    void Start()
    {
        dropdown.onValueChanged.AddListener(OnValueChanged);
        dropdown.ClearOptions();
        var devices = Microphone.devices.ToList();
        dropdown.AddOptions(devices);
        try
        {
            dropdown.SetValueWithoutNotify(devices.IndexOf(rovr.deviceName));
        }catch(IndexOutOfRangeException e)
        {
        }
    }

    // Update is called once per frame
    void Update()
    {
    }

    void OnValueChanged(int option)
    {
        rovr.deviceName = dropdown.options[option].text;
    }
}
