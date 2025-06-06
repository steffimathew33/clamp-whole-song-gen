# clamp-whole-song-gen
## preparing your environment:
1. clone the current repo:
   ```bash
   git clone https://github.com/steffimathew33/clamp-whole-song-gen.git
   ```
2. clone the [whole-song-gen](https://github.com/ZZWaang/whole-song-gen) git repo (for the diffusion model that generates pop songs). (training data: POP-909)

   ```bash
   git clone https://github.com/ZZWaang/whole-song-gen
   ```

## prepping the midi files:
pipeline: midi of whole song --> abc of whole song --> abc of melody --> melody embedding

**note: you will most likely need to alter the file paths found within these scripts (to access the files within whole-song-gen/data/matched_pop909_acc)**

1. extract all of the POP-909 midi files and put into a folder (midi files are found under the folders 001-909 inside matched_pop909_acc)

   ```bash
   python extract_midis.py
   ```
   
2. locally run [MuseScore 3’s Batch Convert Plugin](https://musescore.org/en/project/batch-convert) to convert the midi files to mxl files.

3. create an empty folder called pop909_abcs to store the pop909 abc files. then using [MuseScore’s ABC Import Plugin](https://musescore.org/en/project/abc-importexport) (xml2abc.py), locally convert the mxls to abc notation. (remember to change the file path of the xml2abc.py script!)

   ```bash
   python pop909_xml2abc.py
   ```
   
4. place each aligned_demo.abc file from pop909_abcs folder into its respective folder (matched_pop909_acc/001, /002, etc.) within the whole-song-gen repo

   ```bash
   python place_abcs.py
   ```
   
5. extract the melody from each aligned_demo.abc file. this creates aligned_demo_melody.abc for each song

   ```bash
   python extract_melodies.py
   ```
   
6. filter out unnecessary info from each aligned_demo_melody.abc file, and generate an embedding called melody_embedding.pt for the melody, based on the aligned_demo_melody.abc for each song

   ```bash
   python embed_abcs.py
   ```
