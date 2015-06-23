macro "tracking_process_stack_v2"{
  // clearing previous result and preparing image copy
  run("Clear Results"); 
  rename("Image");
  run("Duplicate...", "duplicate");
  rename("orig");
  selectWindow("Image");

  // iterating for each slice in the stack
  for (i=1;i<=nSlices();i++){
    setSlice(i);
    run("Median...", "radius=2 slice"); // removing noise
    setThreshold(0, 100); // hardcoded thr. for image
    run("Convert to Mask", "method=Otsu background=Light only");
    run("glasbey"); // changing LUT to get false collors to better distinguish objects
    run("Set Measurements...", "area mean standard center median skewness area_fraction stack redirect=orig decimal=2");
    run("Analyze Particles...", "display slice");
    run("Next Slice [>]");
  }
}