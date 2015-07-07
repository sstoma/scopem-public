macro "measure stack" {
  for (currentStep=1; currentStep<=nSlices();currentStep++){
    setSlice(currentStep);
    run("Measure");
  }
}