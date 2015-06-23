macro "create_image_with_moving_objects"{
  // initial variables
  nbr_frames = 40; // number of frames in the image
  color1 = 150; // color of first obj.
  color2 = 250; // color of sec. obj.
  canvas_size = 200; // size of the image
  step = 4; // progress in x between frames
  delta = 15; // difference in position between two objects in x
  x = 5; // initial position x of object
  y = 5;  // initial position y of object
  width = 10; // baseline size of object in x
  height = 10; // baseline size of object in y

  // empty image with noise
  newImage("Image", "8-bit black", canvas_size, canvas_size, nbr_frames); // image will be named "Image"
  run("Salt and Pepper", "stack");

  for(i=1;i<=nbr_frames;i++){
    setSlice(i);
    // first dot
    setColor(color1,color1,color1);
    fillOval(x+i*step, y+i*step, width, height);
    // second dot
    setColor(color2,color2,color2);
    fillOval(delta+x+i*step, canvas_size-(y+i*step), width*2, height*2);
  }
  run("glasbey");
}