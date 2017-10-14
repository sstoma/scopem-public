// initilization
fileName = getInfo("image.filename");
outPath = "/Users/sstoma/Desktop/materials/images/hela/out/"; 
// exchange previous line with your path

// Process all images finishing with .tif 
dir = getDirectory("Choose a Directory where the HeLa tif files are");
dirresults = getDirectory("Choose a Directory where to save results (segmentations)");
list = getFileList(dir);

for (imagenumber=0;imagenumber<list.length;imagenumber++)
{
  if (endsWith(list[imagenumber],".tif")){
    open(dir+list[imagenumber]); 
    run("Clear Results");
    // processing
    run("Gaussian Blur...", "sigma=2 stack");
    setAutoThreshold("Triangle dark");
    run("Convert to Mask");
    run("Set Measurements...", "area mean display redirect=None decimal=9");
    run("Analyze Particles...", "show=[Overlay Masks] display exclude");

    // saving
    saveAs("Results", outPath + "Results-" + fileName + ".txt");
  }
}