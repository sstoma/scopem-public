// processing
run("Gaussian Blur...", "sigma=2 stack");
setAutoThreshold("Triangle dark");
run("Convert to Mask");
run("Set Measurements...", "area mean display redirect=None decimal=9");
run("Analyze Particles...", "show=[Overlay Masks] display exclude");