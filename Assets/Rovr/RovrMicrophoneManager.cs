using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class RovrMicrophoneManager : MonoBehaviour
{
    public string deviceName = null;
    public float audioMultiplier = 1f;
    public float Speed_Mulitplier = 2.0f;

    private AudioSource RovrAudioSource;
    private string openedDevice = null;

    [HideInInspector]
    [NonSerialized]
    public float fAudioForce;

    private const int FREQUENCY = 2000;
    private float[] samples;           // Samples
    private int iStartTimeout;
    private float fAverage = 0.0f;
    private float fMinInputThreshold = 0.1f;
    private float fAudioAmplitude = 0.0f;
    private float[] fAverageArray;
    private int iArrayCount;
    private int ARRAYSIZE;


    private void Awake()
    {
        RovrAudioSource = GetComponent<AudioSource>();
    }

    // Start is called before the first frame update
    void Start()
    {
        //added
        samples = new float[FREQUENCY];
        iStartTimeout = 100;                //when program starts wait until mic input transient noise subsides
        fAudioAmplitude = 0.0f;
        ARRAYSIZE = 3;

        fAverageArray = new float[ARRAYSIZE];
        for (iArrayCount = 0; iArrayCount < ARRAYSIZE; iArrayCount++)
            fAverageArray[iArrayCount] = 0;
        iArrayCount = 0;

        deviceName = PlayerPrefs.GetString("DeviceName",deviceName);
        audioMultiplier = PlayerPrefs.GetFloat("AudioMultiplier",audioMultiplier);

        StartMicListener();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void FixedUpdate()
    {
        // If the audio has stopped playing, this will restart the mic play the clip.
        if (!RovrAudioSource.isPlaying)
        {
            StartMicListener();
        }

        if(deviceName != openedDevice)
        {
            StartMicListener();
        }

        // Gets volume value
        AnalyzeSound();

        if (iStartTimeout > 0)
            iStartTimeout = iStartTimeout - 1;
    }

    /// <summary>
    /// Starts the Mic, and plays the audio back in (near) real-time.
    /// </summary>
    private void StartMicListener()
    {
        Debug.Log("STARTED");
        if(RovrAudioSource.isPlaying)
        {
            RovrAudioSource.Stop();
        }

        if (Microphone.devices.Length > 0) // check if we have any microphone devices available
        {
            Debug.Log("here >>>>>>>>>>>>>>>>>>>");
            //if(true) //if(deviceName == "")
            //{
               
                deviceName = Microphone.devices[0];
                Debug.Log("Hereeeeee " + deviceName + " thereeeeee");
            //}
            Debug.Log("there >>>>>>>>>>>>>>>>>>>");
            RovrAudioSource.clip = Microphone.Start(deviceName, true, 1, 2000);
            RovrAudioSource.loop = true;

            var sampleTime = Time.time;

            while (!(Microphone.GetPosition(deviceName) > 0))
            {
                if (Time.time - sampleTime > 2f)
                {
                    break;
                }
            }

            RovrAudioSource.Play();

            Debug.Log("Started Microphone " + deviceName);

            openedDevice = deviceName;
        }
    }

    /// Credits to aldonaletto for the function, http://goo.gl/VGwKt
    /// Analyzes the sound, to get volume and pitch values.
    private void AnalyzeSound()
    {
        // Get all of our samples from the mic.
        RovrAudioSource.GetOutputData(samples, 0);

        float sum = 0;

        for (int i = 0; i < 2000; i++)
        {
            sum += Mathf.Abs(samples[i]) * audioMultiplier;
        }

        fAverage = sum / 2000f;

        fAverageArray[iArrayCount] = fAverage;
        iArrayCount++;
        if (iArrayCount >= ARRAYSIZE)
        {
            iArrayCount = 0;
        }

        sum = 0;
        for (int i = 0; i < ARRAYSIZE; i++)
        {
            sum = sum + fAverageArray[i];
        }

        float fArrayAverage = sum / ARRAYSIZE;

        if (iStartTimeout > 1)
        {
            return;
        }

        fAudioAmplitude = fArrayAverage;

        if (fAudioAmplitude < fMinInputThreshold)
        {
            fAudioAmplitude = 0;
        }

        //clear whole buffer - avoids having to maintain pointers to where the latest sample starts because we throw it away after calculating the power anyway
        for (int i = 0; i < 2000; i++)
        {
            samples[i] = 0;
        }

        fAudioForce = fAudioAmplitude * Speed_Mulitplier;
    }

    private void OnDestroy()
    {
        PlayerPrefs.SetString("DeviceName", deviceName);
        PlayerPrefs.SetFloat("AudioMultiplier", audioMultiplier);   
    }
}
