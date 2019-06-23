// initialization
roiManager("reset");
x = 20;
y = 20;
nbr_sensors = 4;
delta = 12;

// GUI
Dialog.create("Please specify parameters:");
Dialog.addNumber("Size [px]: ", 5);
Dialog.show();
size = Dialog.getNumber();

// get the input for location from the image
waitForUser("Draw ROI, then hit OK"); 
getBoundingRect(x, y, width, height)

// iterations to create selection
for (nbr_x=0;nbr_x<nbr_sensors;nbr_x++){
  for (nbr_y=0;nbr_y<nbr_sensors;nbr_y++){
    makePoint(x+delta*nbr_x, y+delta*nbr_y);
    run("Enlarge...", "enlarge="+ size +" pixel");
    roiManager("Add");
  }
}

// measurement and save results
roiManager("Multi Measure");
fn = getInfo("image.filename");
saveAs("Results", "/Users/sstoma/Desktop/Results-"+ fn +".txt");
// exchange previous line with your path