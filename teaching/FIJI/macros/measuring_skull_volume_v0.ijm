// this macro is used to document conversion of FIJI sample "MRI Stack (528K)" into binary mask
run("Duplicate...", "duplicate");
run("Gaussian Blur...", "sigma=2 stack");
//setAutoThreshold("Otsu");
//run("Threshold...");
//setAutoThreshold("Otsu dark");
setThreshold(15, 255);
setOption("BlackBackground", false);
run("Convert to Mask", "method=Otsu background=Dark list");
run("Fill Holes", "stack");