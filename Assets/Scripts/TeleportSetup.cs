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
    public Transform player;

    void Start()
    {
        //Init random positions to be placed;
        playerPositions = new Vector3[]{
            new Vector3(-48f, 0f, 50f), //left side of map (x) PLAYER 1 ("REMOTE" IN FILENAME)
            new Vector3(-48f, 0f, 0f),
            new Vector3(-48f, 0f, -45f), 
            new Vector3(46f, 0f, 49.5f), //right side of map PLAYER 2 ("PLAYER" IN FILENAME)
            new Vector3(46f, 0f, 0f),
            new Vector3(46f, 0f, -47.5f),
        };
        
        int spawnPos = Random.Range(0,3);
        if(playerNum > 2 || playerNum < 1){
            playerNum = 1;
            Debug.Log("Incorrect player number entered, set to 1");
        }

        // Index into the randomized position, first three for player 1 second three for player 2
        // if override > 0, manually set position, for testing
        // player is locomotion (camera) object
        if(overrideSpawn != 0){
            player.position = playerPositions[overrideSpawn - 1];
        } else{
            player.position = playerPositions[((playerNum - 1) * 3) + spawnPos];
        }
        Debug.Log(player.position);


        if(playerNum == 1){
            player.rotation = Quaternion.Euler(0f, 90f, 0f);
        } else{
            player.rotation = Quaternion.Euler(0f, -90f, 0f);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
