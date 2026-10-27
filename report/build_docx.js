// Builds DL_IA3_Report.docx in the Karunya "skill based evaluation" report format (same helpers as the NLP report).
// Run from this folder: NODE_PATH=~/node_modules node build_docx.js
// Format: A4, 1-inch margins, Times New Roman 12 pt body (justified, 1.3 line spacing), chapter headings 13 pt bold centred,
// sub-headings 12 pt bold, table text 11 pt, captions 11 pt italic, code Courier New 9.5 pt, title page title 18 pt at 1.5 spacing,
// team names 16 pt, Tamil script in Latha. Edit the constants below before submitting.
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  BorderStyle, LevelFormat, Footer, PageNumber, SectionType } = require("docx");
const FONT = "Times New Roman", TAMIL = "Latha", W = 9026;
const TITLE = "Robustness of Character-Level Transliteration of Informal Romanized Tamil (Tanglish) to Tamil Script";
const COURSE_CODE = "23DC____ (fill in)", COURSE_NAME = "DEEP LEARNING", DATE = "Oct 2026";
const TEAM = ["LEBI RAJA C (URK24AI1005)", "KP SHOHIL (URK24AI1001)", "KRM LOHITH (URK24AI____)", "ALLEN JOHN ISAC (URK24AI____)"];
const ME = TEAM[0];

const runs = (t, o = {}) => String(t).split(/([஀-௿]+)/).filter(Boolean).map((p) =>
  new TextRun({ text: p, font: /[஀-௿]/.test(p) ? TAMIL : FONT, size: 24, ...o }));
const body = (t, o = {}) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 200, line: 312 }, ...o, children: runs(t) });
const centre = (t, o = {}, r = {}) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, ...o, children: runs(t, { bold: true, size: 28, ...r }) });
const chapter = (num, title) => [
  new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: runs(num, { bold: true, size: 26 }) }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 }, children: runs(title, { bold: true, size: 26 }) })];
const unnumbered = (title) => [new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: { after: 360 }, children: runs(title, { bold: true, size: 26 }) })];
const h = (t) => new Paragraph({ spacing: { before: 200, after: 120 }, keepNext: true, children: runs(t, { bold: true }) });
const bullet = (t) => new Paragraph({ numbering: { reference: "bul", level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 100, line: 300 }, children: runs(t) });
const caption = (t) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: runs(t, { italics: true, size: 22 }) });
const gap = (n = 200) => new Paragraph({ spacing: { after: n }, children: [] });
const line = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: line, bottom: line, left: line, right: line };
function table(rows, widths) {
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({ tableHeader: i === 0, cantSplit: true, children: r.map((c, j) => new TableCell({ borders,
      width: { size: widths[j], type: WidthType.DXA }, margins: { top: 60, bottom: 60, left: 100, right: 100 },
      shading: i === 0 ? { fill: "E7E6E6", type: ShadingType.CLEAR, color: "auto" } : undefined,
      children: [new Paragraph({ spacing: { after: 0 }, children: runs(c, { size: 22, bold: i === 0 }) })] })) })) });
}
function code(text) {
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [W], rows: [new TableRow({ cantSplit: false, children: [new TableCell({
    borders, width: { size: W, type: WidthType.DXA }, shading: { fill: "F2F2F2", type: ShadingType.CLEAR, color: "auto" },
    margins: { top: 100, bottom: 100, left: 140, right: 140 },
    children: text.split("\n").map((l) => new Paragraph({ spacing: { after: 0, line: 240 }, children: [new TextRun({ text: l === "" ? " " : l, font: "Courier New", size: 19 })] })) })] })] });
}
function img(path, widthPx) {
  const b = fs.readFileSync(path), w = b.readUInt32BE(16), hh = b.readUInt32BE(20);
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 }, keepNext: true,
    children: [new ImageRun({ type: "png", data: b, transformation: { width: widthPx, height: Math.round(widthPx * hh / w) }, altText: { title: path, description: path, name: path } })] });
}
const fig = (f, px, cap) => [img(`assets/${f}`, px), caption(cap)];

// ---------- front matter ----------
const cover = [gap(300), img("assets/karunya_logo.png", 440), gap(500),
  centre("DIVISION OF DATA SCIENCE AND CYBER SECURITY"), centre("SCHOOL OF COMPUTER SCIENCE AND TECHNOLOGY"), gap(300),
  centre("A SKILL BASED EVALUATION REPORT", {}, { size: 32 }), centre(TITLE, {}, { size: 24 }), gap(500), centre("SUBMITTED BY"), centre(ME), gap(400),
  centre("COURSE CODE"), centre(COURSE_CODE), gap(300), centre("COURSE NAME"), centre(COURSE_NAME), gap(400), centre(DATE)];
const certificate = [...unnumbered("ONLINE CERTIFICATE"), gap(600),
  body("The certificate and the mark sheet are to be attached here (delete this page if the course has no online certificate).", { alignment: AlignmentType.CENTER })];
const titlePage = [new Paragraph({ pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: { before: 600, after: 480, line: 360 }, children: runs(TITLE, { bold: true, size: 36 }) }),
  centre("A REAL TIME APPLICATION REPORT", {}, { italics: true }), centre("Submitted by", {}, { italics: true }),
  ...TEAM.map((t) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: runs(t, { bold: true, size: 32 }) })), gap(300),
  img("assets/karunya_emblem.png", 110), gap(300),
  centre("DIVISION OF DATA SCIENCE AND CYBER SECURITY"), centre("KARUNYA INSTITUTE OF TECHNOLOGY AND SCIENCES"),
  centre("(Declared as Deemed-to-be-under Sec-3 of the UGC Act, 1956) Karunya Nagar, Coimbatore - 641 114. INDIA"), gap(300), centre("Oct 2026.")];

const abstract = [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 }, children: runs("ABSTRACT", { bold: true, size: 28 }) }),
  body("Millions of Tamil speakers type Tamil with English letters (“Tanglish”), and tools built for Tamil script must convert that text back. This is transliteration, and it is hard because Latin letters cannot mark vowel length, doubled consonants or the several n, l and r sounds of Tamil, and because people drop vowels, collapse doubles and slip on keys. Published models are scored on clean romanisation, so their behaviour on informal typing is not known."),
  body("This project builds a paired, seeded robustness benchmark for Latin-to-Tamil transliteration on the Google Dakshina Tamil lexicon (25,000 training, 2,500 development and 2,500 test words): six Tamil-specific noise operators and their mixture at four strengths, giving 28 noisy copies of the test set, plus independent Aksharantar sets. Two deep-learning architectures, a BiLSTM with Luong attention and a pre-LN character Transformer, are trained at about 1M, 3M and 8M parameters with five seeds each and equal tuning (20 random-search trials), and six training conditions (clean, random noise, Tamil-phonological noise, sampled back-transliteration, their combination and a more-data control) are compared. In total 110 models were trained; every number traces to a logged run."),
  body("The architectures tie on clean text at 3M parameters (test CER 9.00 and 9.01), and the Transformer is slightly better under heavy noise. Dropped vowels raise CER from about 9 to 24 and keyboard slips to about 22 at 30% strength, while vowel-length, doubling and stretching cost only 1 to 2 points. Combining Tamil noise with back-transliterated data gives the lowest mixed-noise CER (21.8 against 25.5 for the clean-trained BiLSTM); the benefit does not transfer to an operator left out of training. A fine-tuned 3.15M-parameter deployment model reaches 8.93% clean CER, 65.3% top-1 and 84.8% top-5 accuracy, and runs in a typing demo. Real chat typing is only checked preliminarily, so whether synthetic noise predicts real typing remains open.")];

// ---------- chapters ----------
const ch1 = [...chapter("CHAPTER 1", "INTRODUCTION"),
  h("1.1 Background"),
  body("Tamil is written in its own script, but on phones and keyboards most people type it in the Latin alphabet because it is faster and needs no special keyboard. The result, Tanglish, is the everyday written form of Tamil in messages, social media and search queries. A message such as “vanakkam, eppadi irukkinga?” must be converted to வணக்கம், எப்படி இருக்கிறீர்கள்? before a search index, autocomplete engine or chatbot built for Tamil script can use it [1]."),
  h("1.2 Real-World Problem Description"),
  body("The Latin alphabet cannot express several Tamil distinctions: vowel length (a and aa), doubled consonants (k and kk) and the several n, l and r sounds. Writers therefore spell the same word in many ways; the Dakshina annotators produced 2.7 romanisations per word on average [1]. Fast typing adds dropped vowels (kankl for kanakkil), collapsed doubles (iruku for irukku), stretched letters (semmaaa) and key slips [4, 5]. Neural models reach about 8 to 9% character error rate (CER) on the clean Dakshina Tamil lexicon [1, 3], but the Tamil text in these corpora is formal and was romanised word by word with care, so how they behave on informal typing is not measured [6, 7]."),
  h("1.3 Problem Statement and Motivation"),
  body("Given a typed Latin word, return a ranked list of Tamil-script candidates, and measure how much realistic typing noise hurts, which training remedy helps, and whether the answer depends on the architecture. Transliteration is a pre-processing step for every Tamil NLP system, so an error here passes to every later stage. What is missing is a controlled measurement for Tamil: paired clean and noisy versions of the same test words, a breakdown per noise type, severity levels, and a comparison of remedies and architectures under the same noise."),
  h("1.4 Objectives and Scope"),
  bullet("Build a paired, seeded noise benchmark for Tamil (six operators, four strengths, 28 noisy test sets)."),
  bullet("Compare a BiLSTM with attention and a Transformer at matched size, equal tuning and five seeds."),
  bullet("Compare six training conditions, including a more-data control and held-out operators."),
  bullet("Deliver one deployment model and a typing demo, and report the limits honestly."),
  body("The scope is word-level transliteration. Sentences are handled by converting each word separately, with no sentence context. We speak of informal romanised Tamil and make no claim about chat text."),
  h("1.5 Overview of the Technologies Used"),
  body("Python 3 with PyTorch 2.11 (CUDA 12.8) implements the models and experiments on a single RTX 5070. The Dakshina [1] and Aksharantar [2] datasets provide the pairs. FastAPI serves the model with a single-page HTML and JavaScript front end. Matplotlib draws the figures, LaTeX with IEEEtran typesets the research paper, and Docker provides the runtime.")];

const ch2 = [...chapter("CHAPTER 2", "LITERATURE REVIEW"),
  body("Neural sequence-to-sequence models [10] with attention [11, 12] are the standard approach to transliteration. Wu et al. [8] show that a carefully tuned Transformer [9] is a strong character-level transducer. Roark et al. [1] released the Dakshina dataset of native-speaker romanisations for twelve South Asian languages, and Madhani et al. [2] released the larger Aksharantar collection. On Dakshina Tamil an LSTM was better than a Transformer in one study [1] and worse in another [3]; Transformers depend on batch size [8] and often win only with more parameters [13]. No comparison has tested noisy input."),
  body("Robustness to noise has mostly been studied in machine translation. Belinkov and Bisk [6] show that synthetic and natural noise both break translation models and that a model trained on one kind of noise does not transfer to another, and Karpukhin et al. [14] show that training on synthetic noise helps. For Indian languages, Baiju et al. [7] report that Malayalam CER rises from 7.4 to 22.7 when vowels are dropped, and Azam et al. [15] find that all systems, including large language models, fall to about 20% top-1 on 100 hand-noised Tamil words. Herath et al. [5] address shorthand romanised Tamil with a hybrid rule-based system, and Wolf-Sonkin et al. [4] study Latin keyboards for South Asian languages. Sennrich et al. [16] use back-translation to add data, which we adapt as sampled back-transliteration."),
  h("Comparison with Existing Work"),
  table([["Feature", "Clean-text neural models [1, 3]", "Noise studies in MT [6, 14]", "This project"],
    ["Tamil transliteration", "Yes", "No", "Yes"], ["Paired noisy test sets", "No", "Some (not Tamil)", "Yes, 28 sets"],
    ["Per-noise breakdown", "No", "Some", "Yes, 6 operators"], ["Architectures compared under noise", "No", "No", "BiLSTM and Transformer"],
    ["Training remedies with control", "No", "Some", "6 conditions plus control"]], [2400, 2300, 2100, 2226]), gap(),
  body("The contribution is not a new architecture. It is a controlled measurement for Tamil: a paired benchmark, a remedy study that separates more words from more spelling variety, an architecture comparison under noise, and a reproducible package with a deployed model.")];

const ch3 = [...chapter("CHAPTER 3", "METHODOLOGY"),
  h("3.1 Explanation of the Project"),
  body("A typed word is converted to characters, noise is optionally applied during training, and a character-level encoder-decoder produces Tamil characters one at a time. Beam search keeps the best ten partial outputs and returns the five best complete words. Figure 3.1 shows the data, the model, the decoding and the evaluation."),
  ...fig("fig_arch.png", 470, "Figure 3.1 System architecture: data and noise, pre-LN Transformer encoder-decoder, beam search and evaluation."),
  h("3.2 Dataset and Analysis"),
  body("The Dakshina Tamil romanisation lexicon [1] is split by Tamil word, so no word appears in more than one split. Inputs are lowercase Latin and outputs are Unicode NFC Tamil. A romanisation attested for several native forms is scored against all of them."),
  table([["Split", "Words", "Romanisation pairs", "Distinct typed inputs"], ["Train", "25,000", "68,218", "—"], ["Dev", "2,500", "6,827", "—"], ["Test", "2,500", "6,864", "6,833"]], [1500, 2000, 2800, 2726]), gap(),
  bullet("Independent test sets: Aksharantar Tamil test rows whose Tamil word is in no Dakshina split, in three source subsets (AK-Freq, AK-NEI, AK-NEF) and their union AK-all [2]."),
  bullet("Aksharantar training data shares stems with Dakshina test words, so it is not used in the controlled experiments."),
  bullet("The text is formal and romanised on request, so it is cleaner than real chat. This is why noise is modelled."),
  h("3.3 Data Preprocessing"),
  body("Typed words are lowercased and stripped of whitespace, and Tamil text is normalised to NFC so equal strings have one encoding. Vocabularies are built from training data only (30 source and 52 target symbols including specials). For the augmentation study a pool of 60,000 further Tamil words from the IndicXlit unigram list is built after removing every Dakshina word, every independent-test word and any word sharing a five-code-point prefix with a held-out word; a Tamil-to-Latin BiLSTM romanises each pool word three times by sampling, and a closeness filter leaves 123,488 pairs."),
  h("3.4 Noise Model"),
  body("Six rules written for Tamil perturb the Latin input, plus a mix of all of them. Each is applied at strengths p of 0.1, 0.2, 0.3 and 0.5, with a seed derived from the word, operator and strength, so the 28 noisy sets are exactly reproducible and each noisy item stays paired with its clean form and references."),
  table([["Operator", "Effect", "Example", "Words changed at p=0.3"], ["V-DROP", "delete non-initial vowels", "kanakkil → kankl", "73%"], ["V-LEN", "collapse long vowels", "vanakkaam → vanakkam", "13%"],
    ["GEM", "collapse doubled consonants", "irukku → iruku", "9%"], ["DIGRAPH", "swap th/t, dh/d, sh/s, zh/l", "tamizh → tamil", "32%"],
    ["KEY", "neighbouring key replaces a letter", "nanba → nanva", "52%"], ["REPEAT", "repeat a letter", "semma → semmaaa", "29%"], ["MIX", "all six together", "—", "69%"]], [1500, 3000, 2526, 2000]), gap(),
  h("3.5 Feature Engineering and Text Representation"),
  body("The models work on characters, not words or sub-words. Tanglish spelling is unbounded (names, slang, loan words, typos), so a word vocabulary would constantly meet unseen words, while characters give a closed vocabulary of 30 input and 52 output symbols. No pretrained vectors exist for Tanglish spellings, so character embeddings are learned together with the task, scaled by the square root of the model width, and a learned position embedding is added for the Transformer."),
  h("3.6 Model Selection"),
  table([["Model", "Description"],
    ["BiLSTM + attention", "Two-layer bidirectional LSTM encoder, two-layer LSTM decoder, Luong “general” attention [11, 12]; 0.98M, 2.99M and 8.04M parameters."],
    ["Transformer", "Pre-LN encoder-decoder [9], three layers per side, four heads, learned positions; 0.80M, 3.15M and 8.70M parameters."]], [2400, 6626]), gap(),
  body("Both are small enough to train in 7 to 32 minutes each. Width is chosen by search to hit about 1M, 3M and 8M trainable parameters, so “matched” means approximately matched. The two are compared rather than one chosen in advance because earlier work disagrees on which is better [1, 3]."),
  h("3.7 Training and Testing"),
  body("Training uses Adam with gradient clipping at 1.0 and early stopping on development CER. For each architecture and size, 20 random-search trials over learning rate (10^-3.5 to 10^-2.5), batch size (64 to 512), dropout, label smoothing (0 to 0.1) and, for the Transformer, warmup are run, selected on development CER with beam 10 only; the test set is never used for selection. Each final configuration is trained with five seeds. Six training conditions are compared at about 3M parameters, each with five seeds: A0 Dakshina only; A1 plus random character noise [14]; A2 plus the four Tamil-phonological operators; A3 plus the 123,488 back-transliterations [16]; A4 = A2 plus A3; and CTRL, the same pool words romanised once, greedily, which separates more words from more spelling variety. Online noise is redrawn each epoch and leaves 40% of items clean. Two variants, A2-noGEM and A2-noVDROP, leave one operator out and are tested on it. KEY and REPEAT are never trained, so they test transfer."),
  h("3.8 Evaluation Metrics"),
  bullet("Character error rate (CER): corpus-level Levenshtein distance between the top hypothesis and the closest attested reference, divided by reference length [1, 3]. Lower is better."),
  bullet("Top-k accuracy and mean reciprocal rank (MRR): an input is correct if any of the best k hypotheses equals any reference."),
  bullet("Statistics: mean and sample standard deviation over five seeds; paired bootstrap over 6,833 test items (10,000 resamples); Kruskal-Wallis and Dunn’s test with Holm correction over the six conditions."),
  h("3.9 Novelty of the Project"),
  body("The work adds a paired, seeded noise benchmark for Tamil with per-operator results, a remedy study with a more-data control and held-out operators, an architecture comparison under matched size and equal tuning, and a reproducibility package in which every run writes its configuration, seed, code commit and data checksums.")];

const ch4 = [...chapter("CHAPTER 4", "IMPLEMENTATION"),
  h("4.1 Dataset Used"),
  body("Dakshina Tamil lexicon [1] for training and clean evaluation, Aksharantar [2] for independent test sets and for the fine-tuned deployment model, and public code-mixed Tamil corpora [17] used only to calibrate how often each noise type occurs in real text."),
  h("4.2 Implementation Process"),
  body("The code is a small Python package (src/translit): data.py loads the lexicons, noise.py holds the noise operators, augment.py builds the training conditions, models.py the BiLSTM and the Transformer, decode.py the beam search, metrics.py the CER and ranking metrics, stats.py the bootstrap and rank tests, and train.py and finetune.py the training loops. Scripts run the tuning, the 110-run study, the aggregation of results and the generation of every table and figure. A job supervisor runs several trainings at once on one GPU."),
  h("4.3 Code Snippets"),
  body("The model interface shared by both architectures (teacher-forced training and beam search use the same two calls):"),
  code("class TransformerS2S(nn.Module):\n    def forward(self, src, tgt_in):          # [B, S], [B, T] -> logits [B, T, V]\n        mem, pad = self._memory(src)\n        return self._decode(tgt_in, mem, pad)\n\n    def init_state(self, src):               # encoder run once per batch\n        mem, pad = self._memory(src)\n        return {\"mem\": mem, \"pad\": pad, \"prefix\": ...}\n\n    def step(self, state, tok):              # one decoding step for beam search\n        prefix = torch.cat([state[\"prefix\"], tok.unsqueeze(1)], 1)\n        logits = self._decode(prefix, state[\"mem\"], state[\"pad\"])[:, -1]\n        return F.log_softmax(logits, -1), dict(state, prefix=prefix)"), gap(),
  body("The Transformer is the stock PyTorch module with pre-LN blocks, scaled character embeddings and learned positions:"),
  code("self.tr = nn.Transformer(d_model, heads, enc_layers, dec_layers, ff, dropout,\n                          batch_first=True, norm_first=True)\n\ndef _embed(self, emb, x):\n    p = torch.arange(x.size(1), device=x.device)\n    return self.drop(emb(x) * math.sqrt(self.d) + self.pos(p))"), gap(),
  body("The vowel-drop noise operator (seeded, never returns an empty word):"),
  code("def v_drop(word: str, p: float, rng: random.Random) -> str:\n    \"\"\"Delete non-initial vowels (kanakkil -> kankl).\"\"\"\n    out = [c for i, c in enumerate(word)\n           if not (i > 0 and c in VOWELS and rng.random() < p)]\n    return _nonempty(\"\".join(out), word)"), gap(),
  h("4.4 Web Interface"),
  body("A FastAPI service with a single-page interface loads the deployment model and converts typed Tanglish as the user types. Each Latin word is converted separately, the top candidate is shown in the sentence, and clicking a word reveals the other four candidates. A button copies the Tamil text. A word takes a few milliseconds on a CPU. To run: python app/server.py, then open http://localhost:8000."),
  ...fig("fig6_demo.png", 400, "Figure 4.1 The typing demo converting a Tanglish sentence, with the candidate list of one word open.")];

const ch5 = [...chapter("CHAPTER 5", "TESTING AND VALIDATION"),
  h("5.1 Testing Approach"),
  body("The code is checked by 31 automated pytest tests covering the data loaders, the noise operators, the metrics, the statistics and the job-retry logic, and all 31 pass. Experiments are checked against published numbers before any new run (a reproduction gate), and every stored checkpoint was re-scored per item to confirm that it reproduces its logged result."),
  h("5.2 Test Cases and Results"),
  table([["Test case", "Expected", "Observed"],
    ["Split disjointness and row counts", "25,000 / 2,500 / 2,500 words; no word in two splits", "Loader tests pass"],
    ["Noise operators", "Deterministic for a seed; output never empty", "Tests pass"],
    ["Metrics", "CER and top-k equal hand-computed cases, including multiple references", "Tests pass"],
    ["Reproduction gate", "Match published Dakshina baselines", "Dev CER 8.39 to 8.43 (BiLSTM) against 8.4; 8.49 (Transformer) between 9.4 and 8.2"],
    ["Re-scoring of 110 checkpoints", "Each reproduces its logged score", "109 reproduced; one (8.43 vs 8.49 CER) was retrained"],
    ["Job supervisor incident", "No duplicate workers", "33 of 72 early runs were affected; reruns matched within seed variation"],
    ["Demo API /api/transliterate", "Top-5 per word with timing", "Returns candidates in milliseconds on CPU"]], [2500, 3300, 3226]), gap(),
  h("5.3 Validation Against Requirements"),
  body("The requirements were a real problem with a dataset analysis, justified preprocessing and representation, justified models with a fair comparison, appropriate metrics with analysed results, and a working application. Each is met in Chapters 3 to 6. The one requirement not fully met is real-world accuracy: the benchmark uses formal text romanised on request, and the only check on real chat words is preliminary with labels not yet verified by a person.")];

const ch6 = [...chapter("CHAPTER 6", "RESULTS AND DISCUSSION"),
  body("All CER values are percentages on the Dakshina test lexicon unless stated, with mean and standard deviation over five seeds."),
  h("6.1 Clean Accuracy and Model Size"),
  table([["Model", "Size", "Params", "Dev CER", "Test CER", "Top-1 %", "Top-5 %"],
    ["BiLSTM", "1M", "0.98M", "8.39 ± 0.11", "8.90 ± 0.24", "63.6 ± 0.5", "82.5 ± 0.4"], ["BiLSTM", "3M", "2.99M", "8.41 ± 0.12", "9.00 ± 0.20", "63.3 ± 0.2", "82.3 ± 0.4"],
    ["BiLSTM", "8M", "8.04M", "8.43 ± 0.06", "8.77 ± 0.07", "63.4 ± 0.2", "83.0 ± 0.4"], ["Transformer", "1M", "0.80M", "9.06 ± 0.13", "9.71 ± 0.12", "60.2 ± 0.9", "82.8 ± 0.2"],
    ["Transformer", "3M", "3.15M", "8.49 ± 0.03", "9.01 ± 0.17", "63.1 ± 0.7", "83.4 ± 0.4"], ["Transformer", "8M", "8.70M", "8.76 ± 0.32", "9.40 ± 0.40", "61.4 ± 2.0", "83.3 ± 0.4"]], [1500, 700, 1000, 1400, 1400, 1500, 1526]),
  caption("Table 6.1 Clean results (CER in %, beam 10, mean ± sd over five seeds)."),
  body("At 3M parameters the two architectures tie (test CER 9.00 and 9.01; paired bootstrap difference −0.01, 95% CI [−0.15, +0.12]). At 1M and 8M the BiLSTM is better by 0.81 and 0.63 CER, partly because the Transformer is less stable: its 8M model is worse than its 3M model and has the largest seed spread. The BiLSTM barely changes between 1M and 8M parameters (8.77 to 9.00), so on this word-level task capacity is not the limit."),
  ...fig("fig_tuning.png", 360, "Figure 6.1 Random-search tuning: development CER of 20 trials per architecture and size."),
  h("6.2 How Much Does Typing Noise Hurt?"),
  body("Two operators cause most of the damage. Vowel dropping raises CER from about 9 to 24 at p=0.3 and keyboard slips to about 22; mixed noise is worst (24 to 25). Vowel-length collapse, doubled-consonant collapse and letter stretching cost only 1 to 2 points, and digraph swaps about 3.3. Damage grows steadily with severity: for MIX the 3M BiLSTM gives 14.8, 20.4, 25.5 and 34.4 at p = 0.1, 0.2, 0.3 and 0.5. Per edited character, keyboard slips hurt more than vowel dropping."),
  ...fig("fig_noise_curves.png", 520, "Figure 6.2 Test CER of the 3M models against noise severity for each operator."),
  h("6.3 Which Architecture Degrades Less?"),
  body("Under mixed noise at p=0.3 the Transformer is better at every size (BiLSTM minus Transformer CER: +0.42 at 1M, +1.30 at 3M, +0.28 at 8M), and it degrades less in relative terms (+168% against +183% at 3M), most clearly under vowel dropping (21.7 against 24.0). On clean text the BiLSTM is equal or better. The gaps are 0.3 to 1.3 CER, of the order of tuning and seed effects, so we do not claim the Transformer is generally more robust."),
  ...fig("fig_architectures.png", 520, "Figure 6.3 Clean, mixed-noise and vowel-drop CER against model size."),
  h("6.4 Which Training Augmentation Helps?"),
  table([["Condition", "BiLSTM clean", "BiLSTM MIX", "BiLSTM V-DROP", "BiLSTM KEY", "Transf. clean", "Transf. MIX"],
    ["A0", "9.00", "25.49", "24.03", "22.14", "9.16", "24.27"], ["A1", "9.90", "23.17", "21.69", "18.58", "9.94", "22.49"], ["A2", "9.83", "22.47", "17.70", "23.43", "9.96", "22.46"],
    ["A3", "8.67", "25.10", "22.91", "21.83", "8.65", "23.83"], ["A4", "9.35", "21.82", "16.65", "22.85", "9.13", "21.79"], ["CTRL", "8.64", "25.68", "23.58", "22.09", "8.67", "24.63"]], [1100, 1300, 1300, 1400, 1250, 1350, 1326]),
  caption("Table 6.2 Test CER (%) of the six conditions at 3M parameters; noise at p=0.3, mean over five seeds."),
  bullet("Noise training buys robustness and costs clean accuracy: A1 and A2 lower mixed-noise CER by 2.3 and 3.0 for the BiLSTM but add 0.8 to 0.9 clean CER."),
  bullet("Tamil-aware noise helps only for what it models: A2 beats A1 on vowel dropping (17.7 against 21.7) but is worse on keyboard slips (23.4 against 18.6), which A2 does not model."),
  bullet("Extra words, not spelling variety, explain the clean gain of back-transliteration: A3 (8.67) and the one-romanisation control (8.64) are indistinguishable on clean text; the variants add a small robustness gain on mixed noise."),
  bullet("The combination is best: A4 has the lowest mixed-noise CER for both architectures (21.8) and removes most of A2’s clean cost."),
  ...fig("fig_augmentation.png", 520, "Figure 6.4 Test CER of the six conditions on clean text, three noise suites and the independent AK-all set."),
  body("Robustness does not transfer to a held-out operator. Leaving vowel dropping out of A2 removes almost all of its benefit: BiLSTM CER on V-DROP is 24.97 against 17.70 for full A2, no better than the clean baseline A0 (24.03). Leaving out GEM costs only 0.15 to 0.23 CER on GEM, but GEM is mild to begin with. This agrees with earlier findings that training on one noise type does not protect against another [6]."),
  ...fig("fig_heldout.png", 340, "Figure 6.5 Held-out operators: removing V-DROP from A2’s training removes its benefit on V-DROP."),
  h("6.5 Deployment Model"),
  body("The best seed of the A4 Transformer (3.15M parameters) was fine-tuned with all weights on Dakshina (three times), the back-transliterations and 2.08M filtered Aksharantar pairs (all Dakshina and independent-test words removed), with all six noise operators applied to half of the items, for five epochs (20 minutes on one GPU). The result is one 12.6 MB file."),
  table([["Test suite", "v1 (A4)", "v2 (fine-tuned)", "Change"], ["Test CER", "9.02", "8.93", "−0.09"], ["Test top-1 (%)", "63.88", "65.27", "+1.39"], ["Test top-5 (%)", "85.03", "84.81", "−0.22"],
    ["AK-all CER", "10.95", "10.76", "−0.20"], ["MIX p=0.3 CER", "21.80", "17.77", "−4.03"], ["V-DROP p=0.3 CER", "16.20", "16.00", "−0.20"], ["KEY p=0.3 CER", "23.04", "15.40", "−7.63"]], [3000, 1800, 2226, 2000]),
  caption("Table 6.3 Deployment model against the A4 model it was fine-tuned from (single run each)."),
  body("Clean accuracy is unchanged within noise and the independent Aksharantar sets improve slightly, while robustness improves strongly. These noise gains are not held-out evidence, because the fine-tuning mixture contains all six operators, including KEY and REPEAT that A2 lacked. A preliminary check on 370 words from private chat exports gives CER 24.9 and top-5 71.1%, but its labels are model-made and not yet verified by a person."),
  ...fig("fig_v2.png", 520, "Figure 6.6 Deployment model against its A4 parent on each noise type (left) and on mixed noise at all strengths (right)."),
  h("6.6 Discussion"),
  bullet("Dropped vowels make the input genuinely ambiguous (kankl fits several Tamil words), so part of the remaining error is irreducible without context or a lexicon; top-5 accuracy and language-model reranking are natural next steps rather than larger models."),
  bullet("Data, not capacity, is the limit: growing the BiLSTM from 1M to 8M parameters changes clean CER by at most 0.25, while adding 60,000 pool words lowers it by 0.3 to 0.5 [2]."),
  bullet("The BiLSTM and Transformer disagreement in earlier work is largely a matter of tuning and seeds; Transformers were the more sensitive to hyperparameters here [8, 13]."),
  h("6.7 Limitations and Threats to Validity"),
  bullet("No verified real typing yet: all noise is synthetic and applied to formal Dakshina romanisations, so whether synthetic noise predicts real typing is open."),
  bullet("Hyperparameters were tuned once per size on clean development CER with one seed, early stopping uses clean CER (which disadvantages noise-trained models), and five seeds give low power for small differences."),
  bullet("Back-transliterated pairs are machine-made and inherit the errors of the model that made them."),
  bullet("A supervisor bug started duplicate workers overnight; the damage was checked by reruns and a per-item re-scoring of all 110 checkpoints, one run was retrained, and the logs are in the repository."),
  bullet("The real-chat words come from private conversations; only aggregate scores are reported and the data cannot be released.")];

const conclusion = [...unnumbered("CONCLUSION"),
  body("We built a paired, seeded robustness benchmark for Latin-to-Tamil transliteration and used 110 trained models to answer three questions. Typing noise hurts mainly through dropped vowels and key slips. Tamil-aware noise training removes most of the vowel-drop damage but not damage from operators it does not model, extra romanised words matter at least as much as spelling variety, and Tamil noise combined with back-transliterated data is the best overall. The BiLSTM and the Transformer are close, with the Transformer slightly better under heavy noise. A 3.15M-parameter deployment model reaches 8.93% clean CER and 84.8% top-5 accuracy and runs in a typing demo."),
  body("The main limitation is that no verified real typing exists yet, so the link between synthetic and real noise is open. Future work is to collect and verify a human-typed test set, to add lexicon or language-model reranking for noisy input, to sample spelling variants from real typing instead of a Dakshina-trained model, and to try byte-level pretrained models and sentence context. Code, configurations, per-run logs and the scripts that generate every table and figure are in the project repository (github.com/lebiraja/tamil-translit-robustness, Apache-2.0).")];

const refs = [...unnumbered("REFERENCES"), ...[
  "[1] B. Roark, L. Wolf-Sonkin, C. Kirov, et al., “Processing South Asian Languages Written in the Latin Script: the Dakshina Dataset,” in Proc. LREC, 2020.",
  "[2] Y. Madhani, S. Parthan, P. Bedekar, et al., “Aksharantar: Open Indic-language Transliteration Datasets and Models for the Next Billion Users,” in Findings of EMNLP, 2023.",
  "[3] C. Kirov, C. Johny, A. Katanova, A. Gutkin, B. Roark, “Context-aware Transliteration of Romanized South Asian Languages,” Computational Linguistics, 2024.",
  "[4] L. Wolf-Sonkin, V. Schogol, B. Roark, M. Riley, “Latin script keyboards for South Asian languages with finite-state normalization,” in Proc. FSMNLP, 2019.",
  "[5] H. M. A. D. Herath and T. G. D. K. Sumanathilaka, “TAMZHI: Shorthand Romanized Tamil to Tamil Reverse Transliteration Using Novel Hybrid Approach,” ICTer, 2024.",
  "[6] Y. Belinkov and Y. Bisk, “Synthetic and Natural Noise Both Break Neural Machine Translation,” in Proc. ICLR, 2018.",
  "[7] B. Baiju, K. Manohar, L. G. Pillai, E. Sherly, “Romanized to Native Malayalam Script Transliteration Using an Encoder-Decoder Framework,” 2024.",
  "[8] S. Wu, R. Cotterell, M. Hulden, “Applying the Transformer to Character-level Transduction,” 2021.",
  "[9] A. Vaswani, N. Shazeer, N. Parmar, et al., “Attention Is All You Need,” in Advances in NeurIPS, 2017.",
  "[10] I. Sutskever, O. Vinyals, Q. V. Le, “Sequence to Sequence Learning with Neural Networks,” in Advances in NeurIPS, 2014.",
  "[11] D. Bahdanau, K. Cho, Y. Bengio, “Neural Machine Translation by Jointly Learning to Align and Translate,” in Proc. ICLR, 2015.",
  "[12] M.-T. Luong, H. Pham, C. D. Manning, “Effective Approaches to Attention-based Neural Machine Translation,” in Proc. EMNLP, 2015.",
  "[13] M. Moran and C. Lignos, “Effective Architectures for Low Resource Multilingual Named Entity Transliteration,” in Proc. LoResMT Workshop, 2020.",
  "[14] V. Karpukhin, O. Levy, J. Eisenstein, M. Ghazvininejad, “Training on Synthetic Noise Improves Robustness to Natural Noise in Machine Translation,” 2019.",
  "[15] G. Azam, M. Sadique, S. Ali, M. Nadeem, E. Cambria, et al., “Beyond Specialization: Benchmarking LLMs for Transliteration of Indian Languages,” 2025.",
  "[16] R. Sennrich, B. Haddow, A. Birch, “Improving Neural Machine Translation Models with Monolingual Data,” 2016.",
  "[17] B. R. Chakravarthi, V. Muralidaran, R. Priyadharshini, J. P. McCrae, “Corpus Creation for Sentiment Analysis in Code-Mixed Tamil-English Text,” 2020."]
  .map((t) => new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 140, line: 280 }, indent: { left: 540, hanging: 540 }, children: runs(t) }))];

const appendices = [...unnumbered("APPENDICES"),
  h("Appendix A: Technologies Used"), bullet("Python and PyTorch 2.11 (CUDA 12.8): models, training, metrics."), bullet("FastAPI and Pydantic: the API. HTML and JavaScript: the typing interface."),
  bullet("Matplotlib: figures. LaTeX (IEEEtran): the research paper. Docker: runtime."),
  h("Appendix B: How to Run"),
  code("pytest                                   # 31 tests\npython app/server.py                     # demo at http://localhost:8000\n# every table and figure in the paper is generated from results/*.json\n# by scripts/make_tables.py and scripts/make_figures.py"), gap(),
  h("Appendix C: Model Configuration"),
  body("Deployment model: character Transformer encoder-decoder, 3 encoder and 3 decoder layers, 4 heads, model width 192, feed-forward width 768, learned positions, 3,153,844 parameters, beam width 10, five returned candidates, 12.6 MB single file. Compared sizes: BiLSTM 0.98M, 2.99M, 8.04M; Transformer 0.80M, 3.15M, 8.70M.")];

const evalSheet = [...unnumbered("EVALUATION SHEET"),
  body("Reg.No: URK24AI1005", { spacing: { after: 60 } }), body("Name: LEBI RAJA C", { spacing: { after: 60 } }), body("Course code: " + COURSE_CODE, { spacing: { after: 60 } }), body("Course Name: Deep Learning"),
  table([["S.No", "Rubrics", "Maximum Marks", "Marks Obtained"], ["1", "Viva", "", ""], ["2", "Report", "", ""], ["3", "Presentation", "", ""], ["", "Total", "", ""]], [900, 4526, 1800, 1800]),
  gap(900), new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 600 }, children: runs("Signature of the Faculty-in-charge") })];

const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 })] })] });
const page = { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } };

const doc = new Document({ creator: "Lebi Raja C", title: TITLE, styles: { default: { document: { run: { font: FONT, size: 24 } } } },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [{ properties: { page }, children: [...cover, ...certificate, ...titlePage] },
    { properties: { type: SectionType.NEXT_PAGE, page: { ...page, pageNumbers: { start: 1 } } }, footers: { default: footer },
      children: [...abstract, ...ch1, ...ch2, ...ch3, ...ch4, ...ch5, ...ch6, ...conclusion, ...refs, ...appendices, ...evalSheet] }] });
Packer.toBuffer(doc).then((b) => { fs.writeFileSync("DL_IA3_Report.docx", b); console.log("written", b.length); });
