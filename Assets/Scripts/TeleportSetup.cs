using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TeleportSetup : MonoBehaviour
{
    
    // Start is called before the first frame update
    //player 1 rotation = 90, player 2 rotation = -90
    public int playerNum;
    private Vector3[] playerPositions;
    //Can be used to specify the index of the spawn to override random generation, overrides player num as well
    public int overrideSpawn;

    void Start()
    {
        Transform social = transform.Find("Social");
        Transform interaction = transform.Find("XR Interaction Setup");

        //Init random positions to be placed;
        playerPositions = new Vector3[]{
            new Vector3(-45f, 0f, 47.5f), //left side of map (x)
            new Vector3(-45f, 0f, -2.5f),
            new Vector3(-45f, 0f, -47.5f), 
            new Vector3(45f, 0f, 47.5f), //right side of map 
            new Vector3(45f, 0f, -2.5f),
            new Vector3(45f, 0f, -47.5f),
        };
        
        int spawnPos = Random.Range(0,3);
        if(playerNum > 2 || playerNum < 1){
            playerNum = 1;
            Debug.Log("Incorrect player number entered, set to 1");
        }

        // Index into the randomized position, first three for player 1 second three for player 2
        // if override > 0, manually set position, for testing
        if(overrideSpawn != 0){
            social.position = playerPositions[overrideSpawn - 1];
            interaction.position = playerPositions[overrideSpawn - 1];
        } else{
            social.position = playerPositions[((playerNum - 1) * 3) + spawnPos];
            interaction.position = playerPositions[((playerNum - 1) * 3) + spawnPos];
        }


        if(playerNum == 1){
            social.rotation = Quaternion.Euler(0f, 90f, 0f);
            interaction.rotation = Quaternion.Euler(0f, 90f, 0f);
        } else{
            social.rotation = Quaternion.Euler(0f, -90f, 0f);
            interaction.rotation = Quaternion.Euler(0f, -90f, 0f);
        }
        Debug.Log(interaction.position);

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
