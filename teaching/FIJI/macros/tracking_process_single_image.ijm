macro "tracking_process_single_image"{
  run("Median...", "radius=2 slice");
  setThreshold(0, 100);
  run("Convert to Mask", "method=Otsu background=Light only");
  run("glasbey");
  run("Find Maxima...", "noise=25 output=List light");
}