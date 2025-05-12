# orf_finder.py
def find_orfs(sequence, min_length=100):
    start_codon = "ATG"
    stop_codons = {"TAA", "TAG", "TGA"}
    sequence = sequence.upper().replace("\n", "")
    orfs = []

    for strand, nuc in [('+', sequence), ('-', reverse_complement(sequence))]:
        for frame in range(3):
            i = frame
            while i < len(nuc) - 2:
                codon = nuc[i:i+3]
                if codon == start_codon:
                    for j in range(i+3, len(nuc)-2, 3):
                        next_codon = nuc[j:j+3]
                        if next_codon in stop_codons:
                            orf_len = j + 3 - i
                            if orf_len >= min_length:
                                orfs.append({
                                    "strand": strand,
                                    "frame": frame + 1,
                                    "start": i,
                                    "end": j + 3,
                                    "length": orf_len,
                                    "sequence": nuc[i:j+3]
                                })
                            break
                    i = j + 3
                else:
                    i += 3
    return orfs

def reverse_complement(seq):
    complement = str.maketrans("ATCG", "TAGC")
    return seq.translate(complement)[::-1]
