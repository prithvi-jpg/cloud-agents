---
name: write-like-prithvi
description: Draft, transform, minimally copyedit, and audit writing in Prithvi's voice across tweets, short messages, emails, personal prose, poems, context notes, public posts, and agent briefs. Use when Prithvi asks to write, rewrite, fix only spelling or grammar, clean up dictation, make text sound human or personal, remove AI slop, preserve his voice, produce a 240-character tweet, or turn a brain dump into the right communication format.
---

# Write Like Prithvi

Preserve the person in the thought. Clarify Prithvi's meaning without replacing his voice with generic polish or a shared anti-AI house style.

## Load the right references

1. Read [references/voice-profile.md](references/voice-profile.md) for every task.
2. Read [references/format-modes.md](references/format-modes.md) and select one output mode.
3. Read [references/slop-audit.md](references/slop-audit.md) for public, consequential, long-form, or explicitly anti-slop work. Use its quick gate for routine messages.

## Choose the operation

- **Transform:** Recover a usable piece from dictation, fragments, repetition, and self-correction.
- **Draft:** Write from supplied context in Prithvi's voice.
- **Copyedit:** Correct English mistakes with the smallest possible changes. Do not rewrite.
- **Edit:** Make the minimum effective change. Leave strong human lines alone.
- **Audit:** Name off-voice or slop patterns with quoted evidence. Do not guess whether AI wrote the text.

Use Copyedit when the user says fix only, spelling only, grammar only, minimal changes, do not rewrite, or do not change much. This overrides Transform. Otherwise, use Transform unless the user clearly requests another operation.

## Workflow

### Fix-only branch

When Copyedit is selected:

1. Correct only clear spelling, transcription, grammar, agreement, tense, article, preposition, capitalization, punctuation, and spacing errors.
2. Improve cohesion only when a sentence is genuinely hard to follow, using the smallest local change that makes it readable.
3. Compare the source and result sentence by sentence. Every change must repair a named correctness error or a real readability break.
4. Revert synonym swaps, stylistic upgrades, added transitions, compression, reordering, and changes in tone or formality.
5. If wording is unusual but valid, leave it. If a passage is ambiguous, do not guess what it means.
6. Return only the corrected text. Do not run candidate generation or the contextual slop scan.

Then stop. The remaining workflow applies to Transform, Draft, Edit, and Audit.

### 1. Pin the job

Identify the format, reader, relationship, purpose, desired effect, and hard length limit. Infer these when the destination is obvious. Ask one short question only when a missing answer would materially change the writing.

### 2. Recover the real thought

Extract:

- the core point;
- concrete particulars such as a moment, name, date, number, mechanism, link, or thing that broke;
- emotional cues and honest uncertainty;
- constraints, commitments, requests, and boundaries;
- phrases with real personal energy worth protecting.

Never mistake a spoken draft for the desired sentence structure. Reconstruct the thought instead of paraphrasing the transcript line by line.

### 3. Bind the voice before drafting

Use the voice profile and the source text's own cadence. Preserve vocabulary, bluntness, humor, warmth, uncertainty, digressions, fragments, or run-ons when they are clear and characteristic.

Treat explicit corrections as stronger evidence than inferred habits. Never add deliberate mistakes, slang, profanity, or vulnerability merely to simulate humanness.

### 4. Draft at the right depth

For routine transforms, produce one minimum-effective rewrite.

For public, creative, or consequential writing, internally consider three genuinely different moves, such as a concrete moment, a direct claim, or a mechanism. Reject the most generic move. Do not produce three synonym-swapped versions unless the user asks for options.

Write to the natural length, then remove padding. Do not compress away meaning, personality, or necessary context.

### 5. Run the gate

Check the draft against four questions:

1. **Specific:** Does it contain the detail that makes this Prithvi's piece rather than anyone's?
2. **Additive:** Does every sentence add information, feeling, stance, or useful rhythm?
3. **Shaped by content:** Does the structure follow the thought rather than an AI template?
4. **Voiced:** Does it use Prithvi's actual register for this format?

Then apply the hard rules and contextual scan in [references/slop-audit.md](references/slop-audit.md). Fix only failed spans. Stop after two editing passes. A third pass usually sands away the voice.

### 6. Return the right artifact

For transforms and drafts, return only the finished text unless the user asks for analysis or alternatives.

For audits, return:

1. the quoted line;
2. the named failure;
3. a brief reason;
4. an in-voice replacement.

Protect clean lines explicitly. Do not rewrite unflagged text merely for consistency.

## Non-negotiables

- Do not use em dashes in Prithvi's writing.
- Do not invent facts, numbers, memories, feelings, relationships, quotes, familiarity, promises, deadlines, or outcomes.
- Do not remove genuine uncertainty merely to sound confident.
- Do not use generic warmth, fake enthusiasm, corporate pep, marketing puffery, or motivational conclusions.
- Do not explain a joke, emotion, implication, or concrete fact that already lands.
- Do not turn exploratory notes into a plan unless asked.
- Do not turn a short message into an email or a tweet into a LinkedIn post.
- Do not compress a ramble into tasks while dropping the idea, mental model, or intended user understanding behind those tasks.
- Do not claim a text is human-written or AI-written. Report observable patterns only.
- In Copyedit mode, do not treat "world-class writing" as permission to rewrite. It means invisible correction and editorial restraint.

## Efficiency rule

Use the smallest process that protects the voice. A two-sentence message needs the quick gate, not a scored forensic audit. A public essay or personal application email deserves the full pass.
