// initialization
x = 20;
y = 20;

// iterations
for (nbr_x=0;nbr_x<5;nbr_x++){
  for (nbr_y=0;nbr_y<5;nbr_y++){
    makePoint(x+x*nbr_x, y+y*nbr_y);
    run("Enlarge...", "enlarge=5 pixel");
    roiManager("Add");
  }
}