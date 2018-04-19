using UnityEngine;
using System.Collections;

public class FrameDump : MonoBehaviour {

    public string folder = "frame dumps";
	
	public int frameCount;

	// Initialization
	void Start () {

		// delete folder if it exists
		if( System.IO.Directory.Exists(folder) )
        {
			System.IO.Directory.Delete(folder, true);	
		}
		
        // create the folder for dumps
		System.IO.Directory.CreateDirectory(folder);
		
		// initialize frame counter to 0
		frameCount = 0;
	}
	
	// Update is called once per frame, writes each frame to disk
	void Update () {
		string filename = string.Format("{0:000000}", frameCount);
		ScreenCapture.CaptureScreenshot(folder + "/" + filename + ".jpg");
		frameCount++;
	}
}