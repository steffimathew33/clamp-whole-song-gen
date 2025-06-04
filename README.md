# clamp-whole-song-gen

1. clone this repo
   `git clone https://github.com/steffimathew33/clamp-whole-song-gen.git`
2. clone the whole-song-gen git repo (for the diffusion model that generates pop songs). (training data: POP-909)
   git clone https://github.com/ZZWaang/whole-song-gen
3. collect all midi files in a folder (found under matched_pop909_acc)
   python extract_midis.py
4. locally run [MuseScore 3’s Batch Convert Plugin](https://musescore.org/en/project/batch-convert) to convert the midi files to mxl files.
5. create an empty folder called pop909_abcs to store the pop909 abc files. then using [MuseScore’s ABC import plugin](https://musescore.org/en/project/abc-importexport) (xml2abc.py), locally convert the mxls to abc notation.
   python pop909_xml2abc.py
6. place each aligned_demo.abc file from pop909_abcs folder into its respective folder (matched_pop909_acc/001, /002, etc.) within the whole-song-gen repo
   python place_abcs.py
7. extract the melody from each aligned_demo.abc file. this creates aligned_demo_melody.abc for each song
   python extract_melodies.py
8. filter out unnecessary info from each aligned_demo_melody.abc file, and generate an embedding (melody_embedding.pt) for the melody, based on the aligned_demo_melody.abc for each song
   python embed_abcs.py
