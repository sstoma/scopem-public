// initialization
roiManager("reset");
x = 220;
y = 110;
nbr_sensors = 4;
delta = 12;

// iterations to create selection
for (nbr_x=0;nbr_x<nbr_sensors;nbr_x++){
  for (nbr_y=0;nbr_y<nbr_sensors;nbr_y++){
    makePoint(x+delta*nbr_x, y+delta*nbr_y);
    run("Enlarge...", "enlarge=5 pixel");
    roiManager("Add");
  }
}

// measurement and save results
roiManager("Multi Measure");
fn = getInfo("image.filename");
saveAs("Results", "/Users/sstoma/Desktop/Results-"+ fn +".txt");
// exchange previous line with your path