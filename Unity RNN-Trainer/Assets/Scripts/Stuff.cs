using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Stuff : MonoBehaviour
{
    public Rigidbody body { get; private set; }
    
    public bool isRedBall;

    public bool isVisible;              // debug

    public Tracker tracker;

    public Vector3 screenPosition;      // debug

    void Awake()
    {
        body = GetComponent<Rigidbody>();
        tracker = GameObject.Find("Red Ball Tracker").GetComponentInParent<Tracker>();
        isRedBall = false;
        isVisible = false;
        //To-Do: Datei anlegen
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Kill Zone"))
        {
            tracker.visibleRedBalls.Remove(this.gameObject);
            tracker.invisibleRedBalls.Remove(this.gameObject);
            Destroy(gameObject);
        }
    }

    private void Update()
    {
        if (isRedBall)
        {
            screenPosition = tracker.cam.WorldToScreenPoint(this.gameObject.transform.position);    // debug

            isVisible = GetComponent<Renderer>().IsVisibleFrom(Camera.main);

            // To-Do: Positionen in Datei schreiben

            if(!tracker.visibleRedBalls.Contains(this.gameObject) && !tracker.invisibleRedBalls.Contains(this.gameObject))
            {
                tracker.totalSpawnedRedBalls++;
            }

            if (isVisible)
            {
                tracker.invisibleRedBalls.Remove(this.gameObject);

                if (!tracker.visibleRedBalls.Contains(this.gameObject))
                {
                    tracker.visibleRedBalls.Add(this.gameObject);
                }
            }
            else
            {
                tracker.visibleRedBalls.Remove(this.gameObject);

                if (!tracker.invisibleRedBalls.Contains(this.gameObject))
                {
                    tracker.invisibleRedBalls.Add(this.gameObject);
                }
            }

        }
    }
}