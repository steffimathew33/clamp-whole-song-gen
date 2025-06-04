import mido
import os

# Input and output root directories
INPUT_ROOT = "matched_pop909_acc"
OUTPUT_ROOT = "pop909_w_structure_label"

def extract_melody_from_midi(midi_path, output_path):
    try:
        midi = mido.MidiFile(midi_path)
        if len(midi.tracks) < 2:
            print(f"Skipping {midi_path} (less than 2 tracks)")
            return

        melody_track = midi.tracks[1]  # Track 1 (melody)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            f.write(f"Track 1: {melody_track.name if melody_track.name else 'melody'}\n")
            for msg in melody_track:
                if msg.type in ('note_on', 'note_off'):
                    f.write(f"{msg}\n")
    except Exception as e:
        print(f"Failed to process {midi_path}: {e}")

def batch_process():
    for i in range(1, 910):
        folder = f"{i:03d}"
        input_midi = os.path.join(INPUT_ROOT, folder, "aligned_demo.mid")
        output_txt = os.path.join(OUTPUT_ROOT, folder, "midi_melody.txt")

        if not os.path.exists(input_midi):
            print(f"⚠️  MIDI file not found in {input_midi}, skipping...")
            continue

        extract_melody_from_midi(input_midi, output_txt)

    print("✅ Finished extracting melody for all songs.")

if __name__ == "__main__":
    batch_process()

