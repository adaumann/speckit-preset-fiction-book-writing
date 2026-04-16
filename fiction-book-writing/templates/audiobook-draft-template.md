---
chapter_id: [CHAPTER_ID]
chapter_name: [CHAPTER_NAME]
audiobook_format: ssml-cloud | elevenlabs | both
speaker_mode: single | multi
source_draft: draft/[CHAPTER_ID]_[CHAPTER_NAME].md
status: audiodraft
generated: [YYYY-MM-DD]
---

<!-- ═══════════════════════════════════════════════════════════════════
     AUDIOBOOK DRAFT — SSML-CLOUD VARIANT
     Compatible with: Azure TTS, Google Cloud TTS, Amazon Polly
     Speaker mode: single → all text in narrator voice block
                   multi  → narrator and per-character <voice> blocks
     Pronunciation: <phoneme alphabet="ipa" ph="..."> from Lexicon table
     Delivery hints: <!-- DELIVERY: ... --> comments before passages
     ═══════════════════════════════════════════════════════════════════ -->

<!-- DELIVERY: [Narrator style hint from Audiobook Style Hints table] -->
<speak version="1.0"
       xmlns="http://www.w3.org/2001/10/synthesis"
       xml:lang="en-US">

  <voice name="[NARRATOR_VOICE_SSML]">

    <!-- Chapter heading spoken aloud -->
    <p>[CHAPTER_NAME]</p>
    <break time="1000ms"/>

    <!-- ── Narration ─────────────────────────────────────────────── -->
    <!-- DELIVERY: [context-specific hint if applicable] -->
    <p>[Narration text. Apply phonemes for any lexicon word:
    e.g. <phoneme alphabet="ipa" ph="ˈkiːvə">Caoimhe</phoneme>]</p>
    <break time="600ms"/>

    <!-- ── Dialogue (multi-speaker mode: close narrator, open character voice) -->
    <!-- SINGLE SPEAKER: keep inside narrator <voice>; add prosody if needed -->
    <!-- MULTI SPEAKER:  uncomment the </voice> and <voice> tags below -->

    <!-- </voice>
    <voice name="[CHARACTER_VOICE_SSML]"> -->
    <!-- DELIVERY: [character delivery hint] -->
    <p>"[Dialogue text.]"<break time="250ms"/></p>
    <!-- </voice>
    <voice name="[NARRATOR_VOICE_SSML]"> -->

    <!-- ── Scene break ────────────────────────────────────────────── -->
    <break time="1500ms"/>

    <!-- ── Continue narration ─────────────────────────────────────── -->
    <p>[Next narration passage.]</p>
    <break time="600ms"/>

  </voice>

</speak>

---

<!-- ═══════════════════════════════════════════════════════════════════
     AUDIOBOOK DRAFT — ELEVENLABS VARIANT
     ElevenLabs v2 API supported tags: <break>, <phoneme alphabet="ipa">, <emphasis>
     Speaker mode: single → one <speak> block with narrator voice header
                   multi  → one <speak> block per voice segment
     Lexicon:      See audiodraft/lexicon.pls (upload to EL project first)
     Substitutes:  Pronunciation Lexicon EL Substitute values replace source words inline
     API hint:     POST /v1/text-to-speech/{voice_id}
                   model_id: eleven_multilingual_v2 or eleven_turbo_v2_5
     ═══════════════════════════════════════════════════════════════════ -->

<!-- ELEVENLABS AUDIOBOOK DRAFT
     Chapter:      [CHAPTER_ID] [CHAPTER_NAME]
     Speaker mode: single | multi
     Segments:     [N]
     Lexicon:      audiodraft/lexicon.pls
     Generated:    [YYYY-MM-DD]
     API hint:     Pass each segment's <speak> content as the `text` field.
                   Synthesize segments in order; stitch resulting MP3s per chapter. -->

<!-- ── Segment 1 ─────────────────────────────────────────────────── -->
<!-- VOICE: [NARRATOR_EL_VOICE_ID] | role: narrator -->
<speak>
[Chapter heading spoken aloud]
<break time="1000ms"/>
<!-- DELIVERY: [Narrator style hint] -->
[Narration text. Use EL Substitute for lexicon words, e.g. "Keeva" instead of "Caoimhe".]
<break time="600ms"/>
</speak>

<!-- ── Segment 2 (multi-speaker only: one segment per voice change) ─ -->
<!-- VOICE: [CHARACTER_EL_VOICE_ID] | role: [CHARACTER_NAME] -->
<!-- DELIVERY: [Character delivery hint] -->
<speak>
"[Dialogue text.]"
<break time="250ms"/>
</speak>

<!-- ── Segment 3 ─────────────────────────────────────────────────── -->
<!-- VOICE: [NARRATOR_EL_VOICE_ID] | role: narrator -->
<speak>
<break time="1500ms"/>
[Next narration passage.]
<break time="600ms"/>
</speak>
