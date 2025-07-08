# backend/utils/text_utils.py
def split_into_chunks(segments, max_words=100):
    chunks = []
    current_chunk = []
    word_count = 0

    for seg in segments:
        seg_words = seg["text"].split()
        current_chunk.append(seg)
        word_count += len(seg_words)

        if word_count >= max_words:
            chunk_text = " ".join([s["text"] for s in current_chunk])
            chunks.append({
                "start": current_chunk[0]["start"],
                "end": current_chunk[-1]["end"],
                "text": chunk_text
            })
            current_chunk = []
            word_count = 0

    if current_chunk:
        chunk_text = " ".join([s["text"] for s in current_chunk])
        chunks.append({
            "start": current_chunk[0]["start"],
            "end": current_chunk[-1]["end"],
            "text": chunk_text
        })

    return chunks
