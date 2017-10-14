// Process all images finishing with .tif 
dir = getDirectory("Choose a Directory where the HeLa tif files are");
outPath = getDirectory("Choose a Directory where to save results (segmentations)");
list = getFileList(dir);

// in list elements are numbered from 0
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
vfileName = getInfo("image.filename");
    saveAs("Results", outPath + "Results-" + fileName + ".txt");
  }
}