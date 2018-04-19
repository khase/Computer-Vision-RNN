using UnityEngine;

[System.Serializable]
public struct FloatRange
{
    public float min, max;

    public float RandomInRange
    {
        get
        {
            return Random.Range(min, max);
        }
    }
}

[RequireComponent(typeof(Tracker))]
public class StuffSpawner : MonoBehaviour
{
    public FloatRange timeBetweenSpawns, scale, randomVelocity, angularVelocity;

    public Stuff[] stuffPrefabs;

    public float velocity;

    public Material stuffMaterial;

    float timeSinceLastSpawn;

    float currentSpawnDelay;

    static int noRedBalls;
    
    private void Start()
    {
        
    }

    void FixedUpdate()
    {
        timeSinceLastSpawn += Time.deltaTime;
        if (timeSinceLastSpawn >= currentSpawnDelay)
        {
            timeSinceLastSpawn -= currentSpawnDelay;
            currentSpawnDelay = timeBetweenSpawns.RandomInRange;
            SpawnStuff();
        }
    }

    void SpawnStuff()
    {
        Stuff prefab = stuffPrefabs[Random.Range(0, stuffPrefabs.Length)];
        Stuff spawn = Instantiate<Stuff>(prefab);

        spawn.transform.localPosition = transform.position;
        spawn.transform.localScale = Vector3.one * scale.RandomInRange;
        spawn.transform.localRotation = Random.rotation;

        spawn.body.velocity = transform.up * velocity +
            Random.onUnitSphere * randomVelocity.RandomInRange;
        spawn.body.angularVelocity = 
            Random.onUnitSphere * angularVelocity.RandomInRange;

        spawn.GetComponent<MeshRenderer>().material = stuffMaterial;

        if (prefab.name.Equals("Sphere") && stuffMaterial.name.Equals("Red"))
        {
            noRedBalls++;
            spawn.name = "RED BALL " + noRedBalls;
            spawn.isRedBall = true;
            //spawn.camera
        }
    }

    private void LateUpdate()
    {
        Debug.Log("no red balls: " + noRedBalls);
    }
}

