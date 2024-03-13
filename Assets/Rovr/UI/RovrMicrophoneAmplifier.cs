using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RovrMicrophoneAmplifier : MonoBehaviour
{
    private Slider slider;
    private RovrMicrophoneManager rovr;

    private void Awake()
    {
        rovr = FindObjectOfType<RovrMicrophoneManager>();
    }

    // Start is called before the first frame update
    void Start()
    {
        slider = GetComponent<Slider>();
        slider.SetValueWithoutNotify(rovr.audioMultiplier);
        slider.onValueChanged.AddListener(OnValueChanged);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnValueChanged(float value)
    {
        rovr.audioMultiplier = value;
    }
}
