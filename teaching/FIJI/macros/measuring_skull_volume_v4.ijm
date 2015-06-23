macro "measure stack" {
  for (currentStep=1; currentStep<=nSlices();currentStep++){
    setSlice(i);
    run("Measure");
  }
}