/*
 * 1. Make sure that image with logo to be pasted is open.
 * 2. change the variable source to the title of the logo image
 * 3. Change the number of stamps per image (nbr_stamps)
 * 4. Make sure that output folders do exist
 */

//variables
setBatchMode(true);
output_path = '/Users/sstoma/tmp/stamped/';
output_path_imgs = output_path+'imgs/';
output_path_labels = output_path+'labels/';
source_fn = "/Users/sstoma/src/scopem-public/code/synthetize_images/img/logo-small.tif"; // please set it up before running macro; make sure image is open
target = getTitle(); // make use
nbr_stamps = 10; // how many stamps per image
close_windows = true; 

// create target-mask
selectWindow(target);
run("Duplicate...", " ");
rename("target-mask.png");
target_width = getWidth()
target_height = getHeight()
run("Set...", "value=0");

// create target-copy
selectWindow(target);
run("Duplicate...", " ");
rename("target-modified.png");

// open logo image
open( source_fn );
rename("source");

for (i=0; i<nbr_stamps; i++)
{
	// get pixels from source & change them to fit mask pixel value to rand(1
	selectWindow(source);
	run("Select All");
	run("Multiply...", "value=255");
	m = random()+ (1/255); // to avoid 0ing mask
	run("Multiply...", "value="+m); // use different grey level
	run("Copy");
	setPasteMode("Transparent-zero");
	source_width = getWidth();
	source_height = getHeight();
	
	// paste into mask
	selectWindow("target-mask.png");
	run("Paste");
	w = random();
	h = random();
	// TODO make sure that the box is in a good place
	makeRectangle(round(w*target_width), round(h*target_height), source_width, source_height);
	
	// paste into mask
	selectWindow("target-modified.png");
	run("Paste");
	// we reuse coordinates to make sure we paste in the same place
	makeRectangle(round(w*target_width), round(h*target_height), source_width, source_height);
}

selectWindow("target-mask.png");
run("Select None");
run("Multiply...", "value=255");
saveAs("Tiff", output_path_labels+target);
close()

selectWindow("target-modified.png");
saveAs("Tiff", output_path_imgs+target);
close()

selectWindow(source);
close();
