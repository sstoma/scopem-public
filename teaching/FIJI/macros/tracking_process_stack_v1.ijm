macro "tracking_process_stack_v1"{
  r = newArray();
  for (i=1;i<=nSlices();i++){
    setSlice(i);
    run("Median...", "radius=2 slice");
    setThreshold(0, 100);
    run("Convert to Mask", "method=Otsu background=Light only");
    run("glasbey");
    run("Find Maxima...", "noise=25 output=List light");
    run("Next Slice [>]");

  // workaround for Find maxima overwriting results at each step
    for (j=0;j<nResults();j++){
      x = getResult("X", j);
      y = getResult("Y", j);
      print(x, y, i);
      temp = newArray(x, y);
      r = Array.concat(r, temp);
    }
  }
  Array.show( r );
}