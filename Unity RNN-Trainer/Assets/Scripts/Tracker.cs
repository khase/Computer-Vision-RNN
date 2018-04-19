using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tracker : MonoBehaviour {

    public int totalSpawnedRedBalls;

    public List<GameObject> invisibleRedBalls;
    public List<Vector3> invisibleRedBallPositions;

    public List<GameObject> visibleRedBalls;
    public List<Vector3> visibleRedBallPositions;
    
    public Camera cam;

    void Awake()
    {
        cam = GetComponentInParent<Camera>();

        visibleRedBalls = new List<GameObject>();

        invisibleRedBalls = new List<GameObject>();

        visibleRedBallPositions = new List<Vector3>();
    }

    void LateUpdate()
    {
        visibleRedBallPositions.Clear();

        foreach (GameObject redBall in visibleRedBalls)
        {
            Vector3 screenPos = cam.WorldToScreenPoint(redBall.transform.position);

            //Debug.Log("target position: " + screenPos.x + "\t" + screenPos.y + "\t" + screenPos.z);

            visibleRedBallPositions.Add(screenPos);
        }
        //Debug.Log("Red Balls on Screen: " + visibleRedBalls.Count);

        invisibleRedBallPositions.Clear();
        
        foreach (GameObject redBall in invisibleRedBalls)
        {
            Vector3 screenPos = cam.WorldToScreenPoint(redBall.transform.position);

            invisibleRedBallPositions.Add(screenPos);
        }

        Debug.Log("Total spawned red balls: " + totalSpawnedRedBalls);
    }
}
