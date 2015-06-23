// initialization
outPath = "/Users/sstoma/Desktop/materials/images/hela/out/"; 
// exchange previous line with your path

// processing
run("Gaussian Blur...", "sigma=2 stack");
setAutoThreshold("Triangle dark");
run("Convert to Mask");
run("Set Measurements...", "area mean display redirect=None decimal=9");
run("Analyze Particles...", "show=[Overlay Masks] display exclude");

// saving
saveAs("Results", outPath+"Results.txt");