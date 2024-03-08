using System.Collections;
using System.Collections.Generic;
using UnityEngine;
// using Ubiq.Avatars;



public class Teleporter : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject avatarManager;
    public bool confirm;
    void Start()
    {
        transform.position = new Vector3(0, 0, 0);
        Transform panel = transform.Find("Social");
        panel.position = new Vector3(-2,0,0);
        this.confirm = true;
    }

    // Update is called once per frame
    void Update()
    {
        // if(this.confirm){
        //     this.avatarManager = GameObject.Find("Avatar Manager");
        //     foreach(Avatar avatar in avatarManager.Avatars){
        //         // avatar.Position = new Vector3(-2,0,0);
        //     }
        //     this.confirm = false;
        // }      
    }
}
