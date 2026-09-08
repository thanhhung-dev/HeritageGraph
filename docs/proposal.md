**International School**

**CAPSTONE PROJECT 1**

CMU-SE 450

**PROJECT PROPOSAL**

**Date: September 5, 2026**

**A Personalized Hybrid RAG + GraphRAG Platform for Exploring, Understanding and Planning Local Cultural Experiences**

**Submitted by: C1SE.50**

Duong Thanh Hung – 29219043370

**Approved by:**

**Msc. Nguyen Thi Thanh Tam**

**Proposal Review Panel Representative:**

Name: Signature: Date:

**Capstone Project 1 – Mentor:**

Name: **Msc. Nguyen Thi Thanh Tam** Signature: Date:

**Da Nang, September 2026**

---

**PROJECT INFORMATION**

| Field | Value |
| --- | --- |
| Project title | A Personalized Hybrid RAG + GraphRAG Platform for Exploring, Understanding and Planning Local Cultural Experiences |
| Project acronym | CulturalMemoryGraph / CMG |
| Product name | **HeritageGraph** |
| Project duration | 27/08/2026 – 06/12/2026 (15 weeks) |
| Institution | International School, CMU-SE 450 |
| Pilot locality / theme | Huế and Đà Nẵng — heritage sites, cuisine, performing arts, craft villages, festivals, museum artifacts |
| Project status | Capstone project proposal |

---

## 1. Project Title

**A Personalized Hybrid RAG + GraphRAG Platform for Exploring, Understanding and Planning Local Cultural Experiences**

Short name: **CulturalMemoryGraph (CMG)**. Product name: **HeritageGraph**.

Every element of the title names a concrete capability of the system:

| Title element | Capability |
| --- | --- |
| **Personalized** | A per-user interest profile drives ranking, expansion and recommendation. Two users entering the same query receive different, individually justified result sets |
| **Hybrid RAG** | Retrieval fuses three complementary channels — lexical sparse retrieval, dense semantic retrieval, and diacritic-insensitive n-gram retrieval — so that formal queries, paraphrases and accent-free typing all succeed |
| **GraphRAG** | A knowledge graph of people, places, events, time, crafts, artifacts and documents anchors retrieval, re-ranks candidates, and serves as the reasoning substrate for cross-domain recommendation |
| **Exploring, Understanding** | Vietnamese question answering with sentence-level citation, an interactive card interface, entity detail views, timelines and a graph explorer |
| **Planning** | When the system detects that the user is preparing to attend a cultural activity, it supplies the practical context needed to actually go: schedule, venue, weather, what to bring, where to stand, where to park |

## 2. Team Members

| Full name | Student ID | Role | Email |
| --- | --- | --- | --- |
| Duong Thanh Hung | 29219043370 | Project Leader — requirements analysis, AI and retrieval development, data and knowledge engineering, frontend, QA, documentation | *[to be completed before submission]* |

This is a one-member project, so the roles defined separately in the standard template are merged into a single responsibility set. The supervisor provides direction, feedback and progress review.

Two evaluation activities require an external second rater, and Section 11.4 defines that step: review of entity gold labels, and relevance judgement for recommendations. A relevance score produced by the same person who wrote the recommender would not be evidence, and the project does not treat it as such.

## 3. Supervisor(s)

| Full name | Title / Department | Role | Email |
| --- | --- | --- | --- |
| Msc. Nguyen Thi Thanh Tam | International School | Project Supervisor / Mentor | *[to be completed before submission]* |
| *[to be appointed]* | Museum or cultural centre | Domain Advisor — heritage content review | *[to be completed]* |

The supervisor helps define scope, review the architecture, assess data quality, monitor progress and critique results. A domain contact with local knowledge reviews the factual accuracy and attribution of cultural records: a staff member of the Museum of Cham Sculpture or the Museum of Royal Antiquities, a representative of the Hue Monuments Conservation Centre, or a history teacher.

## 4. Problem Statement

### 4.1. Background

Cultural material about Huế and Đà Nẵng is abundant but structurally flat. Encyclopaedia articles, festival yearbooks, museum labels, gazetteers and tourism pages each describe one object at a time. A person who arrives interested in one thing — a form of theatre, a dish, a statue, a festival, a craft — receives a single article and is left to discover related culture unaided.

Two distinct failures follow, and the project addresses both.

### 4.2. Failure One — Discovery Is Not Personalized

Search engines and heritage portals return the same ranked list to everybody. Interest in Huế royal court music and interest in Cham stone sculpture produce the same generic "related links" block, because relatedness is computed from text similarity or fixed editorial curation, never from the user.

Culture is the domain where this fails hardest, because cultural interest is idiosyncratic and cuts across categories. A person drawn to one traditional performing art is usually also open to its costume, its instruments, the venue where it is staged, the craft village that produces its props, and the festival at which it is performed. Those objects live in different categories and different documents, so no existing tool connects them *for that particular person*.

### 4.3. Failure Two — Understanding Is Not Actionable

Existing cultural information systems answer "what is this?" and stop. The user's real need is usually one step further and is almost never stated out loud.

Somebody researching a museum artifact implicitly wants to know which museum holds it, what else from the same period is there, and whether a comparable object or replica can be seen or bought. Somebody reading about a festival implicitly wants to know when it happens this year, where to stand, whether it will rain, and where to leave a motorbike. Every one of those questions is answerable from data. None is answered by a cultural corpus alone.

### 4.4. Core Problem

The project addresses **the absence of a cultural information platform that adapts to the individual user and anticipates the practical need behind a cultural query, while remaining verifiable.**

The final clause is what makes this a research-grade problem rather than merely unbuilt software. The two obvious ways to add personalization and proactivity both fail:

- **Collaborative filtering**, the standard commercial recommender, requires a large user base and produces unexplainable output. It can indicate *that* two things are related but never *why*. In a heritage and education context that is a defect, not a cosmetic gap.
- **Letting a general-purpose language model improvise** the additional context reintroduces hallucination in exactly the place where the user is most likely to act on the answer. A model that will helpfully invent a parking location or a ticket price is a model that will invent a dynasty.

The problem is therefore to make the platform personalized and proactive **without** paying either price: recommendation must be explainable from graph structure, and practical context must be typed, sourced data rather than generated prose.

General-purpose chatbots do not solve this. Without a specific local corpus, a model confuses Vietnamese place names, blends provinces, and asserts information present in no source. Retrieval-Augmented Generation addresses grounding by conditioning generation on retrieved external memory [1]. GraphRAG extends it by combining text extraction, network analysis and LLM summarization over graph structure [2], [3]. This project uses the graph for a second purpose beyond grounding: as the reasoning substrate for explainable cross-domain recommendation.

### 4.5. Why the Problem Matters

UNESCO notes that digital technology can widen access to culture and support documentation, protection, promotion and inventory of heritage [4]. Access, however, is not only availability — it is relevance and usability. A corpus nobody navigates is not accessible in any meaningful sense.

Personalized, explained navigation matters specifically for cultural transmission: it converts a single point of curiosity into a path through related heritage, which is how cultural literacy accumulates. Correct planning support matters because it is the step at which cultural interest becomes cultural participation — the difference between reading about a festival and attending one.

### 4.6. Proposed Response and Central Design Principle

The platform is built as three cooperating layers over one verifiable knowledge base:

1. **Grounded answer layer** — Hybrid RAG + GraphRAG retrieval, a domain fine-tuned Vietnamese model, mandatory sentence-level citation, and structural refusal gates that make the system abstain instead of guessing.
2. **Personalization layer** — an interest profile inferred from the user's own searching and browsing, with no preference form to fill in, and a recommender that scores candidates by graph affinity to the current subject, graph affinity to the profile, and an explicit bonus for candidates in a *different* cultural category that are nevertheless connected by a real path. Every suggestion is returned with the path that produced it, and the inferred profile is visible and correctable rather than hidden.
3. **Proactive advisory layer** — intent detection over the query, then a registry mapping intent to typed context blocks: schedule, venue map, weather, preparation checklist, viewpoint, parking, comparable artifacts, related crafts.

One rule governs the boundary between generation and fact, and it is referenced throughout this document:

> **The language model writes heritage narration only. Every practical or structured claim — date, coordinate, weather, parking, artifact attribute, recommendation — is rendered from a typed record carrying its own provenance, and never passes through generation.**

This preserves the trustworthiness of the answer layer while adding capabilities that would otherwise undermine it, and it yields a verification property that is structural rather than statistical: no field of any practical card can be fabricated, and this is asserted automatically in the test suite (NFR06).

## 5. Survey / Existing Solutions

### 5.1. Retrieval-Augmented Generation, Hybrid Retrieval and GraphRAG

Lewis et al. combine a parametric language model with a non-parametric memory retrieved from an external index, improving knowledge-intensive question answering and providing a retrieval basis for verification [1].

Practical RAG systems rarely rely on one retrieval channel. Sparse lexical retrieval in the BM25 family [8] is precise on proper names, rare terms and exact phrasing; dense embedding retrieval generalizes to paraphrase and synonymy. Fusing the two — **Hybrid RAG** — is the established way to obtain both behaviours, and reciprocal rank fusion [9] combines rankings of incompatible score scales without requiring normalization. Vietnamese adds a third requirement that neither channel handles: users frequently type without diacritics, so a diacritic-insensitive character n-gram channel is needed for the same document to be found whether the query is written *"lăng Khải Định"* or *"lang khai dinh"*.

Microsoft Research's GraphRAG combines text extraction, network analysis and LLM prompting or summarization to reason over dataset structure rather than isolated passages [2]; Edge et al. detail the local-to-global query-focused summarization approach [3]. **GraphRAG** contributes what no lexical or dense index can express: that a monument is in a particular ward, that two entities co-occur across documents, that an artifact and a craft belong to the same period. Those relations are the ones cultural questions actually turn on.

The platform therefore combines both: **Hybrid RAG supplies candidate passages, and GraphRAG anchors, expands and re-ranks them.** Section 12.3 specifies the pipeline.

### 5.2. Recommender Systems and the Explainability Requirement

Commercial recommendation is dominated by collaborative filtering and learned embeddings, which require scale and produce opaque output. Explainable recommendation is a recognized research direction with documented benefits for user trust and decision quality [11].

This platform uses **graph-path recommendation**: candidates are scored by weighted propagation over the heritage graph, and the propagation path is returned as the explanation. This works from the first session without a user base, it is auditable, and it directly supports cross-domain suggestion, since a bonus term rewards candidates reached by a real path but belonging to a different cultural category. Diversity re-ranking follows the maximal marginal relevance formulation [10] so the top of the list does not degenerate into five instances of the same kind of site.

### 5.3. Comparable Platforms

**Google Arts & Culture** aggregates digitized collections and curated place-based stories from museums worldwide [5], [6]. It shares HeritageGraph's goal of pairing images with narrative context. It differs in that relatedness is editorially curated, no entity–relation graph is exposed to the user, there is no citation-backed open-ended question answering over a specific local corpus, and there is no per-user interest model.

**Tourism and destination portals** supply practical logistics — hours, directions, booking — but they are commerce-first. They contain no cultural knowledge graph, no source citation, and no abstention behaviour; an absent fact is filled with marketing copy rather than an admission of ignorance.

**Digitized gazetteers and static heritage sites** are authoritative but inert: one document per object, no cross-linking, no query interface beyond keyword search.

**General-purpose LLM chatbots** appear to solve everything and verifiably do not. Without a local corpus they confuse Vietnamese proper names and provinces, and they cannot cite.

### 5.4. Comparison with Existing Approaches

| Criterion | Static heritage site / gazetteer | General-purpose LLM chatbot | Google Arts & Culture | Tourism / booking portal | **HeritageGraph** |
| --- | --- | --- | --- | --- | --- |
| Primary data | Isolated articles and captions | Knowledge inside model weights | Curated museum exhibits | Commercial listings | Local corpus + knowledge graph + typed cultural records |
| Person–place–event–time links | Usually absent | Not reliable | Editorially curated | Absent | Knowledge graph with provenance on every node |
| Retrieval | Keyword only | None (parametric) | Faceted browse | Keyword and filters | **Hybrid RAG (lexical + dense + accent-free) fused with GraphRAG** |
| Accent-free Vietnamese input | Fails | Tolerant but ungrounded | Not applicable | Partial | Dedicated n-gram channel |
| Personalization | None | Conversational memory only | Minimal | Commercial intent targeting | Interest profile + graph-path scoring |
| Explainable "why this?" | No | No | No | No | **Yes — the propagation path is returned** |
| Cross-domain suggestion | No | Unverifiable | Within curated exhibits | No | **Explicit cross-category bonus term** |
| Passage-level citation | Occasional | Not guaranteed | Exhibit-level credit only | No | **Mandatory and measured** |
| Abstention when evidence is missing | Not applicable | Rare | Not applicable | Not applicable | **Structural refusal gates, measured** |
| Practical planning context | No | Unverifiable | No | Yes, commerce-first | **Yes, typed and sourced** |
| Operates without an external AI API | Yes | No | No | No | Yes — analysis and generation run locally |

### 5.5. Project Differentiation

HeritageGraph does not claim to replace professional preservation systems or large aggregator platforms. Its contribution is the combination that none of the five comparators offers:

**Per-user personalization and proactive practical context, delivered on top of a verifiable, citation-backed, abstaining answer engine — with retrieval that fuses Hybrid RAG and GraphRAG, every recommendation explainable as a graph path, and every practical claim traceable to a typed source record.**

## 6. Objectives and Scope

### 6.1. General Objective

Build and evaluate a web-based AI platform for the culture of Huế and Đà Nẵng that answers Vietnamese-language questions from a curated local corpus using Hybrid RAG combined with GraphRAG, with sentence-level citations and explicit abstention; personalizes exploration for each user through an interest profile and an explainable graph-path recommender; and proactively supplies the typed practical context implied by the user's intent, so that cultural interest can become cultural participation.

### 6.2. Specific Objectives

**O1 — Cultural knowledge base.** Build a corpus of at least 80 documents across six cultural categories — heritage sites, cuisine, scenic sites, performing arts, festivals, craft villages — with at least 8 documents per category, normalized into passages with source locators and aliases.

**O2 — Knowledge graph.** Build a knowledge graph linking documents, entities, administrative units, regions, categories, years, events, venues and artifacts, in which every node traces to a literal span of a source document, with typed and weighted relations and no relation asserted without evidence.

**O3 — Structured cultural records.** Author venue records with coordinates, event records with calendar type, dates, organizer and ritual/festivity segments, and artifact records with period, material, holding museum and floor-plan position — every factual field carrying a source URL and the source sentence it was read from.

**O4 — Hybrid RAG + GraphRAG retrieval.** Implement three-channel retrieval — lexical sparse, dense semantic, and diacritic-insensitive n-gram — fused by reciprocal rank fusion, then anchored, expanded and re-ranked by graph propagation, with a trace endpoint exposing every scoring component for explainability.

**O5 — Grounded answering.** Provide Vietnamese question answering with mandatory citation in the form `[Nguồn: <verbatim sentence> — <url>]`, polite abstention when evidence is insufficient, correction of false premises in the first sentence, and four-type entity extraction as strict JSON.

**O6 — Personalization.** Infer interests from the user's own search and browsing behaviour with time decay, expose the inferred profile for inspection and correction, rank and expand per user, return with every recommendation the graph path justifying it, and achieve a measurable cross-domain rate rather than only intra-category suggestion. The user is never asked to declare preferences before using the platform.

**O7 — Proactive advisory.** Classify query intent into six classes and render intent-appropriate typed context blocks — event schedule, venue map, weather, preparation checklist, viewpoint, parking, comparable artifacts, related crafts — with zero fabricated fields, asserted by automated test.

**O8 — Interactive card interface.** Replace plain search-result lists with an interactive card-based chat, entity detail pages, a timeline view, a graph explorer, a map view and one museum floor plan with artifact hotspots.

**O9 — Curation and governance.** Provide administrator content and record management with source validation that rejects unsourced fields, review status, audit logging, and a corpus and graph health dashboard.

**O10 — Privacy.** Obtain consent before behavioural logging, store only what recommendation requires, and let users export and permanently delete their personal data.

**O11 — Evaluation.** Measure and report retrieval recall, entity F1, citation faithfulness and coverage, abstention accuracy, intent accuracy, recommendation precision@5 and nDCG@5 with inter-rater agreement, cross-domain rate, intra-list diversity, card field correctness, p95 latency and usability; and demonstrate that adding the personalization and advisory layers produces no regression in citation faithfulness or abstention accuracy.

### 6.3. In Scope

One pilot region pair (Huế and Đà Nẵng) across six cultural categories. Corpus ingestion, normalization, passage splitting and alias extraction. Deterministic entity, relation, administrative-unit and temporal extraction with evidence spans. Knowledge graph construction, statistics, subgraph inspection and retrieval tracing. Hybrid RAG with three retrieval channels fused and re-ranked by GraphRAG. A domain fine-tuned local Vietnamese model with citation, abstention and false-premise correction. User registration, authentication and session management. Implicit interest inference from behaviour with time decay, and an inspectable, correctable interest profile. An explainable graph-path recommender with cross-domain bonus and diversity re-ranking. Six-class intent classification. Typed advisory cards including weather and points of interest from free public APIs. Interactive card-based chat, entity detail pages, timeline, graph explorer, map view, and one museum floor plan with artifact hotspots. Administrator content and structured-record management with source validation, review status, audit log and health dashboard. Personal-data export and deletion. The evaluation suite, evaluation report, test suite and continuous integration.

End users submit text only. They do not upload images or documents through the chat interface.

### 6.4. Out of Scope

3D modelling, LiDAR scanning, photogrammetry, digital twins and virtual tours. Professional GIS mapping and routing. Video recognition and large-scale OCR of scanned documents. Multilingual translation and interface localization. Ticket or tour booking and any commercial transaction. Real-time crowd, traffic or transport data. Official historical certification of content. Collaborative-filtering recommendation requiring a large user base. Native mobile applications. Speech input or output. Automatic recognition of image content — images are managed through confirmed metadata and captions rather than computer vision.

3D is recorded as future work: once the metadata, knowledge graph, retrieval and citation quality are proven, 3D models can be linked to existing nodes without redesign.

## 7. Key Features & Requirements

### 7.1. Core Features

Features are grouped by actor: Administrator/Curator F01–F06, User F07–F16, internal AI exchanges F17–F18. Every request flow has a matching response flow, giving **18 request/response pairs** in the system context diagram (Section 12.2).

| Code | Feature | Actor | Request → Response |
| --- | --- | --- | --- |
| F01 | Login | Admin | Login Request → Login Response with session credential |
| F02 | Manage Cultural Content | Admin | CRUD on documents, aliases, category and region assignment → CRUD Result, with graph rebuild triggered |
| F03 | Manage Structured Records | Admin | CRUD on venues with coordinates, events with calendar and segments, artifacts with period, material and position → Validation Result that rejects any record containing an unsourced factual field |
| F04 | Review Extraction Results | Admin | Confirm or correct extracted entities, relations and aliases → Updated Status with audit-log entry |
| F05 | Manager Dashboard | Admin | Dashboard Request → Overview Data: document counts per category, graph statistics, unsourced-field count, review backlog, latest evaluation metrics |
| F06 | Run Evaluation Suite | Admin | Evaluation Request → Metrics Report recording model, adapter checkpoint, prompt version, corpus version and evaluation configuration |
| F07 | Register and Manage Account | User | Registration or Account Update → Account Confirmation |
| F08 | Interest Profile Inspection and Control | User | Request to view the inferred interest profile, or a correction such as removing or muting an inferred interest → Current Interest Profile showing, for each entry, the activity that produced it. The profile is built automatically from F09, F10 and F11 activity; there is no preference form and no setup step |
| F09 | Personalized Exploration | User | Selection of a topic, place, artifact, dish, craft or festival → Personalized Recommendation List, each item carrying the graph path that justifies it, including cross-category items |
| F10 | Interest-Based Hybrid Search | User | Keyword or natural-language search query → Ranked Results from Hybrid RAG fused with GraphRAG and re-ranked by the interest profile |
| F11 | Natural Language Query | User | Free-text Vietnamese cultural question → Answer with Source Citations, or an explicit statement that the available evidence is insufficient |
| F12 | Proactive Context | User | Intent detected on F09, F10 or F11 → Typed Advisory Cards: event schedule, venue map, weather and preparation checklist, best viewpoint, nearest parking, comparable artifacts, related crafts — each with its provenance |
| F13 | Entity Detail View | User | Entity or document selection → Detail Content: narration, citations, timeline of associated years, related entities, associated venue and events, and a related-content rail |
| F14 | Artifact Location | User | Artifact location question → Museum Floor Plan with the artifact's hotspot highlighted |
| F15 | Graph Exploration | User | Node and hop-count selection → Subgraph with typed, weighted relations for visual exploration, plus a retrieval trace explaining why a passage was chosen |
| F16 | Personal Data Export and Deletion | User | Export or deletion request → Machine-readable personal-data file, or confirmation of permanent deletion |
| F17 | Content Analysis | Internal | Document text → Extracted Entities, Relations, Administrative Units and Years with evidence spans, used to build the graph. Runs on F02 |
| F18 | Answer Generation | Internal | Assembled context and question → Generated Narration with citation. Runs on F11 |

**F17 and F18 are internal and local.** F17 is deterministic extraction with no model call at all: a curated entity list, a closed classifier vocabulary and regular expressions, so every extracted name is a literal substring of the source and cannot be invented. F18 is a locally hosted fine-tuned model. There is therefore no external AI service in the architecture, no API cost, and cultural corpus text never leaves the machine.

**F08 is inspection and control, not setup.** The platform deliberately has **no onboarding questionnaire**. Asking a first-time visitor to declare cultural preferences fails for three reasons. It asks about interests the user has not formed yet — someone who has never encountered Cham sculpture cannot select it from a list. It contradicts the platform's own premise, which is that the system *infers* what the user cares about from what they actually do, exactly as stated in Section 4.2. And it imposes a setup cost before any value is delivered, which is the standard reason preference forms are abandoned.

Interests are therefore inferred entirely from behaviour: what the user searches, which entities they open, how long they stay, which cards they click, save or dismiss. The user's *first search is the signal* — a query about a Cham statue immediately makes sculpture, the Cham period and the holding museum active interests, with no form in between. F08 exists so the inference is not opaque: the user can see each inferred interest together with the action that produced it, and can remove or mute anything wrong. Personalization is thus scrutable and correctable without ever being declared.

Cold start is handled by the structure of the scoring function rather than by a form. The recommender's seed term — graph affinity to the object the user is currently looking at — works from the very first interaction, so the first session is already useful. The profile term simply contributes nothing until there is behaviour to learn from, and grows in weight as evidence accumulates.

**F12 is the feature that must not be allowed to hallucinate.** Its cards are rendered from typed records and free public APIs and are never produced by generation. The trigger is intent detection rather than an explicit user click, which is what makes it proactive: the system infers the need the user has not stated.

**Dependencies.** F09 to F15 depend on the graph built by F17. F09, F10 and F13 additionally depend on the profile from F08. F12 and F14 additionally depend on the structured records from F03. F12's weather and parking cards degrade to an explicit unavailable state when an external service cannot be reached, and that degradation is itself a test case.

### 7.2. Functional Requirements

| Code | Requirement | Acceptance Criteria |
| --- | --- | --- |
| FR01 | A user can register, authenticate and manage an account | Password stored only as an argon2id hash; session credential issued as an HttpOnly cookie; protected endpoints reject unauthenticated requests |
| FR02 | An administrator can add or edit a corpus document | The document is normalized, split into passages with source locators, and the graph is rebuilt with new nodes linked to their source |
| FR03 | An administrator can add or edit venue, event and artifact records | The record is saved only if every factual field carries a source URL and source sentence; unsourced fields are rejected with a field-level error |
| FR04 | The system extracts entities, relations, administrative units and years from a document | Output matches the four-type schema, stores evidence spans, and every extracted name is a literal substring of the source |
| FR05 | The system builds and updates the knowledge graph | Nodes and edges are created, typed, weighted and linked to source documents; statistics are reported; no relation is created without a source span |
| FR06 | An administrator can confirm or correct extraction results | The change and the acting user are written to an audit log with before and after values |
| FR07 | The system infers an interest profile without asking the user to declare one | The platform is fully usable before any profile exists; after a user's first few searches or views the profile contains weighted interests derived from those actions |
| FR08 | The system records interaction implicitly, and the user can inspect and correct the result | View, dwell, card click, save and dismiss events are logged with timestamp and target node; profile weights update with time decay; the user can see each inferred interest together with the action that caused it, and can remove or mute it |
| FR09 | The system returns personalized recommendations | For a given subject and profile, a ranked list is returned in which **each item is accompanied by the graph path that produced it** |
| FR10 | Recommendations include cross-category items | For seeds whose category is connected in the graph, at least one of the top five recommendations belongs to a different cultural category |
| FR11 | Recommendations are diverse | The top five contain no more than three items of the same category unless fewer categories are reachable |
| FR12 | Hybrid search retrieves relevant passages | For an in-domain query the correct document is ranked first, whether the query is written with diacritics, without diacritics, by alias, or as a paraphrase |
| FR13 | Search results are re-ranked by interest profile | Two users with different profiles receive different orderings for the same query, and the ordering difference is attributable to profile weights |
| FR14 | A user can submit a Vietnamese text-only question | The chat interface accepts text only; the answer is generated solely from retrieved context |
| FR15 | Answers include citations or state insufficient evidence | No assertive answer is produced without a supporting cited sentence from a retrieved source |
| FR16 | The system corrects false premises | When a question contains an assumption contradicting the source, the correction appears in the first sentence of the answer |
| FR17 | The system classifies query intent | The query is assigned to one of six intent classes; the assigned class is recorded and inspectable |
| FR18 | The system returns advisory cards appropriate to intent | Cards match the intent-to-generator registry; **every card field equals the corresponding field of its source record or API response, with no generated field** |
| FR19 | The system supplies event schedule and venue detail | For an event in the knowledge base the system returns name, calendar type and dates, venue with coordinates, organizer, and ritual and festivity segments |
| FR20 | The system supplies weather and a preparation checklist for a dated event | The forecast is retrieved from a public weather API for the venue coordinates; the checklist is produced by explicit rules over the forecast, not by generation |
| FR21 | The system supplies nearby points of interest | Parking, viewpoints and craft or gift shops near a venue are returned with source and fetch time; an unavailable service yields an explicit unavailable state |
| FR22 | The system shows an artifact's position on a museum floor plan | The requested artifact's hotspot is highlighted on the floor plan of the holding museum |
| FR23 | A user can view an entity detail page | The page shows narration with citations, a timeline of associated years, related entities, associated venue and events, and a related-content rail |
| FR24 | A user can explore the knowledge graph | A subgraph around a chosen node is returned to a chosen hop depth with typed, weighted relations |
| FR25 | A user can inspect why a passage was retrieved | A trace exposes graph seeds, per-channel ranks, graph affinity, scoring components and whether the system would abstain |
| FR26 | A user can export and delete their own personal data | Profile and interaction history are returned in a machine-readable file and can be permanently deleted on request |
| FR27 | An administrator can view corpus and graph health | Document counts per category, graph statistics, unsourced-field count, review backlog and latest metrics are displayed |
| FR28 | The system can run the full evaluation suite | All metrics of Section 15.3 are computed and exported as a report recording model, adapter checkpoint, prompt version, corpus version and evaluation configuration |

### 7.3. Non-functional Requirements

| Code | Group | Requirement |
| --- | --- | --- |
| NFR01 | Performance | p95 end-to-end latency for a standard question does not exceed 8 s in the demo environment, measured continuously throughout development rather than at the end |
| NFR02 | Performance | Recommendation and advisory-card responses return within 2 s excluding model generation; external API calls run concurrently with generation so their latency is hidden |
| NFR03 | Performance | An entity detail page renders within 3 s using cached graph data and optimized thumbnails |
| NFR04 | Accuracy | Retrieval recall@1 on the in-domain question set is at least 95%, including accent-free, alias and paraphrase queries |
| NFR05 | Trustworthiness | Citation faithfulness at least 85%; citation coverage of answerable questions at least 90% |
| NFR06 | Safety | **Zero fabricated fields in advisory cards**, asserted automatically over the whole card test set |
| NFR07 | Safety | Abstention accuracy at least 90%; a fabricated assertive answer on an out-of-domain question counts as a failure |
| NFR08 | Explainability | Every recommendation exposes a human-readable graph path, and every retrieval decision is inspectable through the trace endpoint |
| NFR09 | Usability | A first-time visitor can ask a question and receive relevant recommendations immediately, with no setup step, no preference form and no written instructions |
| NFR10 | Accessibility | Text alternatives for non-text content; sufficient colour contrast; keyboard-navigable chat, cards and map; the chat transcript is announced to assistive technology, following WCAG 2.1 level AA where applicable [20] |
| NFR11 | Security | Authentication on every endpoint reading or writing personal data; input validation; file type and size limits; no unauthenticated write path; the server does not bind a public network interface in the demo configuration |
| NFR12 | Privacy | Behavioural logging requires informed consent; only data needed for recommendation is stored; export and deletion are supported |
| NFR13 | Provenance | Every displayed factual claim resolves to a source: a corpus sentence, a structured record field with its own source, or a named external API with a fetch timestamp |
| NFR14 | Data integrity | Structured records cannot be persisted with a missing source URL or source sentence; the constraint is enforced at the database level, not only in application code |
| NFR15 | Maintainability | Ingestion, graph, retrieval, generation, recommendation, advisory and interface remain separately interfaced modules |
| NFR16 | Reproducibility | Model identifier, adapter checkpoint, prompt version, corpus version, graph statistics and evaluation configuration are recorded in every report file |
| NFR17 | Scalability | A new region, category, event, venue or artifact can be added without code changes; a new advisory card type is added by registering one generator |
| NFR18 | Portability | The platform runs entirely on a single machine with no external AI service and no API key |

## 8. Constraints and Assumptions

### 8.1. Constraints

| Group | Description |
| --- | --- |
| Time | The project runs for about 15 weeks, so it covers one region pair and one theme set rather than many localities or data types |
| Team | One developer, so there are no parallel workstreams and no internal code review; two evaluation activities require an external second rater |
| Hardware | Development and demonstration on a single Apple Silicon laptop, which fixes the language model at the quantized 3-billion-parameter class and makes generation latency the dominant term in end-to-end response time |
| Data | Encyclopaedic sources are uneven by category: heritage sites are documented in depth while performing arts, craft villages and festivals are thin, so corpus balancing is scheduled work rather than an assumption |
| Data | Structured event, venue and artifact facts do not exist in machine-readable form in the sources and must be authored by hand with citations |
| Language | Vietnamese proper names, aliases, diacritics and accent-free typing are inconsistent, and administrative names changed in recent reorganizations |
| External data | Weather and points-of-interest APIs are free and keyless but rate-limited, and volunteer-mapped point-of-interest coverage in Vietnam is uneven |
| Calendar | Vietnamese festival dates are given in the lunar calendar, and general-purpose lunar libraries follow the Chinese calendar and can differ by one day at the UTC+7 boundary |
| Evaluation | With one developer and no user base, recommendation relevance and narration style cannot be measured at statistical scale; they are reported as small-sample judgements with agreement statistics and labelled as such |
| Rights | Sources are used under attribution for a non-commercial academic prototype, and content that cannot be attributed is not used |

### 8.2. Assumptions

- Encyclopaedic and official cultural sources for Huế and Đà Nẵng remain publicly accessible, and reuse for a non-commercial academic prototype is permissible with attribution.
- Structured event, venue and artifact facts can be sourced from monument-centre, museum and municipal publications, each recorded with a citable URL and sentence.
- Free public weather and mapping APIs remain keyless and available at demonstration request volume.
- The demonstration machine can run retrieval, the knowledge graph, the database and the local language model together at small scale.
- Users have a browser and network access, and they type text only without uploading files.
- The goal is to demonstrate pipeline feasibility and measurable trustworthiness, not to deploy a national-scale system of record.
- AI narration is a suggestion subject to curator confirmation, and structured records are authoritative only to the extent of their cited source.
- Behavioural logging is consented to, and a user may explore without a profile, in which case recommendations fall back to graph affinity to the current subject alone.
- A domain advisor can be secured for factual review of hand-authored festival and artifact records.
- Images are managed through confirmed metadata and captions rather than automatic recognition of image content.

## 9. Target Users / Stakeholders

| Group | Needs | How the platform helps |
| --- | --- | --- |
| Students and young people | Learn about culture quickly and visually, following their own curiosity rather than a fixed syllabus | Interests inferred from their own browsing, cross-domain recommendations with visible reasons, citation-backed answers, timeline and graph exploration |
| Domestic and cultural travellers | Decide what to see, and know how to actually attend it | Event schedule with calendar conversion, venue map, weather and preparation checklist, viewpoint and parking cards |
| Teachers | Visual, sourced material usable in lessons and extracurricular activities | Category and region browsing, entity detail pages with citations usable as references, entity extraction over supplied passages |
| Museums, libraries and cultural centres | Present collections and connect them to wider cultural context | Structured artifact records with floor-plan position, graph links from artifact to period, place and craft, curator review workflow |
| Researchers | Find relationships, cross-check sources, and identify gaps | Inspectable knowledge graph, retrieval traces, alias dictionary, provenance on every node, subgraph export |
| Artisans and local communities | Have their knowledge recorded accurately and attributed appropriately | Source URL and sentence on every structured field, curator review status, explicitly stated scope limits |
| Developer | A testable AI and software engineering problem with measurable outcomes | Modular architecture, typed API, evaluation harness, continuous integration |
| Supervisor and review panel | Assess feasibility, rigour and contribution | Documented architecture, quantitative evaluation with stated methodology, honest limitation reporting |

## 10. Technology Stack

| Layer | Component | Technology | Purpose |
| --- | --- | --- | --- |
| Frontend | Framework | Next.js 14 App Router, React 18, TypeScript | Card-based chat, exploration, interest profile view, detail pages, admin interface |
| Frontend | Styling | Tailwind CSS | Design system for cards, typography and responsive layout |
| Frontend | Mapping | Leaflet with OpenStreetMap tiles | Venue map, parking and viewpoint display |
| Frontend | Graph visualization | D3 force-directed layout | Interactive subgraph exploration |
| Frontend | Floor plan | Hand-authored SVG with hotspot coordinates | Artifact position display inside a museum |
| Backend | API framework | Python, FastAPI, Pydantic v2 | REST API, orchestration, validation, OpenAPI specification |
| Backend | Server | Uvicorn | ASGI server with threadpool offload for blocking generation |
| Data | Relational database | PostgreSQL 16 with SQLAlchemy and Alembic | Users, interest profiles, interaction events, venues, events, artifacts, points of interest, recommendation log, audit log |
| Data | Vector store | pgvector extension | Dense passage embeddings for the semantic retrieval channel |
| Data | Knowledge graph | NetworkX, constructed deterministically in memory at startup | Entities, documents, regions, categories, administrative units, years, provenance |
| Data | Corpus store | Normalized plain-text files with an index and alias dictionary | Source documents with passage-level locators |
| Retrieval | Sparse lexical | BM25 over word tokens | Precision on proper names, rare terms and exact phrasing |
| Retrieval | Accent-insensitive | BM25 over diacritic-stripped character 4-grams | Accent-free Vietnamese typing and misspelling tolerance |
| Retrieval | Dense semantic | Multilingual sentence-embedding model with pgvector similarity search | Paraphrase and synonym matching |
| Retrieval | Fusion | Reciprocal rank fusion [9] | Combines rankings of incompatible score scales without normalization |
| Retrieval | Graph re-ranking | Two-hop weighted propagation with hub damping over the knowledge graph | Anchoring, expansion and relation-aware re-ranking |
| AI | Language model | Qwen2.5-3B-Instruct, 4-bit quantized [17], with a LoRA adapter, served locally through MLX [18] | Vietnamese heritage narration, citation format, abstention, false-premise correction, entity JSON |
| AI | Fine-tuning | LoRA [7] via MLX, low-rank adapters on the upper transformer layers with prompt-masked loss | Teaches register, citation format and refusal behaviour rather than facts |
| AI | Extraction | Curated entity list, closed classifier vocabulary, regular expressions | Deterministic, non-fabricating entity, administrative-unit and year extraction |
| AI | Intent classification | Rule and lexicon based over diacritic-stripped text, six classes | Selects advisory card generators; auditable and inexpensive |
| AI | Recommendation | Graph propagation with profile affinity, cross-category bonus and maximal marginal relevance diversity [10] | Personalized, explainable suggestion |
| External | Weather | Open-Meteo, keyless [12] | Hourly precipitation probability and temperature for preparation advice |
| External | Points of interest | Overpass over OpenStreetMap [13] | Parking, viewpoints, craft and gift shops near a venue |
| External | Geocoding | Nominatim [14] with one-time caching, and Wikidata coordinates [15] | Venue coordinates |
| Security | Password hashing | argon2id [19] | Credential storage |
| Security | Session | JWT in an HttpOnly, SameSite cookie | Authenticated sessions without token exposure to scripts |
| Quality | Testing | pytest, Playwright | Unit, integration, API and end-to-end tests including the card-fabrication assertion |
| Quality | CI/CD | Git, GitHub, GitHub Actions, Docker Compose | Version control, automated checks, reproducible environments |
| Quality | Documentation | Markdown, Mermaid, OpenAPI | Requirements, architecture, API and evaluation reports |

Three stack decisions deserve explicit justification, because each departs from the default choice.

**Three retrieval channels rather than one.** Vietnamese cultural queries arrive in three shapes: exact proper names, accent-free transliteration, and paraphrase. Sparse lexical retrieval handles the first and fails on the third; dense retrieval handles the third and is weaker on rare proper names; neither handles the second, because stripping diacritics destroys the tokens a word-level index depends on. Fusing all three is the reason the platform can answer the same question whether the user writes *"lăng Khải Định ở đâu"*, *"lang khai dinh o dau"*, or *"vua Khải Định được chôn ở chỗ nào"*.

**PostgreSQL with pgvector rather than a dedicated vector database.** The corpus is on the order of hundreds of passages, and the platform already needs a relational database for users, profiles, events, venues and artifacts. Adding a second data store for embeddings at this scale would add operational cost without adding capability, and it would split provenance across two systems.

**A local model rather than an external AI API.** This removes API cost, removes dependence on an external provider, and keeps cultural corpus text on the machine — which matters because some cultural material is community-owned and its handling is a governance question, not only a technical one.

## 11. Methodology & Development Plan

### 11.1. Development Methodology

The project uses Agile with short one-week increments and a demonstration to the supervisor at each increment, including planning, development, testing and a retrospective. Short cycles are appropriate because extraction quality, retrieval quality, recommendation relevance and advisory usefulness can only be judged against real data and real interaction; they cannot be specified accurately in advance.

### 11.2. Two Sequencing Rules

**High-risk work goes first.** Corpus category balancing and the hand-authored structured records that every advisory card depends on are scheduled early, and end-to-end response time is measured from the moment the database and authentication land rather than in the testing phase, because a latency problem discovered in the final fortnight cannot be fixed architecturally.

**No layer is built on an unmeasured layer.** Retrieval is measured before generation is tuned; generation is measured before personalization is added; trustworthiness is re-measured after the advisory layer lands. This is what makes objective O11's non-regression claim possible.

### 11.3. Development Plan

| Phase | Weeks | Main content | Output |
| --- | --- | --- | --- |
| Initiation | 1–2 | Problem analysis, source survey, locality and theme selection, requirements, data schema, wireframes, evaluation methodology | Proposal, SRS, data dictionary, wireframes, evaluation plan |
| Sprint 1 — Foundation | 3 | PostgreSQL with migrations and Docker Compose; data model; registration, login and session management; consented interaction logging; personal-data export and deletion; design system; first latency measurement | Accounts, persistence, event logging, latency baseline |
| Sprint 2 — Knowledge base | 4 | Corpus expansion to full category balance; alias extraction; venue, event and artifact record authoring with source validation; graph rebuild; evaluation gold-set regeneration; retrieval re-measurement | Complete corpus, knowledge graph, three structured record sets, refreshed evaluation set |
| Sprint 3 — Retrieval and answering | 5 | Dense embedding channel with pgvector; three-channel fusion; graph re-ranking; refusal gates; trace endpoint; citation validation; retrieval and answer-quality measurement | Hybrid RAG + GraphRAG pipeline with measured recall, citation and abstention |
| Sprint 4 — Personalization | 6–7 | Implicit interest inference with time decay; profile inspection and correction; graph affinity, profile affinity, cross-category bonus, diversity re-ranking; recommendation endpoint returning explanation paths; recommendation logging; exploration and detail pages with a related-content rail | Personalized exploration and search, explainable recommendations |
| Sprint 5 — Proactive advisory | 8–9 | Six-class intent classifier with a labelled question set; intent-to-card registry; weather integration; points-of-interest integration with caching; preparation-checklist rules; concurrent external fetch overlapped with generation; graceful degradation | Typed advisory cards for research, attendance and trip-planning intents |
| Sprint 6 — Interface | 10 | Card renderer registry; entity detail pages; timeline; graph explorer; map view; museum floor plan with artifact hotspots; admin dashboard and review interface; accessibility pass | Complete interactive card-based interface |
| Sprint 7 — Journeys | 11 | End-to-end research journey (artifact → holding museum → same-period artifacts → related craft village) and attendance journey (festival → schedule → venue → weather → preparation → viewpoint → parking); buffer for slippage | Two complete demonstration journeys |
| Testing | 12–13 | Unit, integration, API and end-to-end suites with CI; card-fabrication assertion; full metric set including intent accuracy and recommendation precision with a second rater; user study; performance remediation | Test report and evaluation report |
| Closing | 14–15 | Architecture, API and schema documentation; privacy and ethics review; demonstration video, slides and user guide; final report | Final accepted version and report |

### 11.4. Quality, Review and Version Control

Source code is managed with Git. Any change to graph construction rules, prompts, the model, the adapter checkpoint, the corpus or the database schema is recorded in a changelog, because each of those invalidates previously reported metrics. Continuous integration runs linting and the test suite before merge, and pull requests are used for the retrieval, recommendation and advisory modules.

Because there is no second developer, two evaluation activities use an external rater. **Entity gold labels** generated automatically from the deterministic graph are marked as machine-prefilled and require human review before the final report, which must state which portion was reviewed; as they stand they measure whether the model learned the extraction rule set rather than whether extraction is correct. **Recommendation relevance** is judged by two raters over the same seed set, with inter-rater agreement reported alongside precision.

For cultural content, every structured field records its source URL and source sentence, and curator review status is stored. For AI components, every report file records model identifier, adapter checkpoint, prompt version, corpus version and evaluation configuration.

## 12. System Architecture Overview

### 12.1. Architecture Description

The architecture has seven layers.

**1. Presentation layer.** Card-based chat, personalized exploration, entity detail pages, timeline, graph explorer, map view, museum floor plan, citation panel, interest profile view, and the administrator content and review interface.

**2. Application and API layer.** Authentication and session management, chat orchestration, hybrid search, recommendation, advisory, graph inspection and tracing, content and structured-record management with validation, dashboard, evaluation, and personal-data export and deletion.

**3. Ingestion layer.** Source resolution and fetching with caching and retry, text normalization, section-aware passage splitting with source locators, alias extraction from redirects and lead-sentence patterns, and duplicate and disambiguation-page rejection.

**4. Knowledge processing layer.** Deterministic entity extraction with a curated list and closed classifier vocabulary, administrative-unit detection, temporal extraction, passage embedding for the dense channel, entity linking through the alias dictionary, and knowledge graph construction with typed, weighted, source-linked relations.

**5. Storage layer.** Corpus files with passage locators, the in-memory knowledge graph, passage embeddings in pgvector, and PostgreSQL for users, interest profiles, interaction events, venues, events with segments, artifacts, points of interest, the recommendation log and the audit log.

**6. AI orchestration layer.** Query analysis covering region and category scope, intent, and the distinction between the question's subject and any presupposition it contains; three-channel Hybrid RAG retrieval; graph seeding, propagation and re-ranking; context assembly; refusal gates; local generation; and citation validation.

**7. Personalization and advisory layer.** Profile maintenance with time decay, graph-path recommendation with cross-category bonus and diversity re-ranking, six-class intent classification, and the intent-to-card generator registry with external adapters for weather and points of interest.

The design principle of Section 4.6 is enforced at the boundary between layers 6 and 7: layer 6 produces narration prose, layer 7 produces typed card objects, and card objects never pass through layer 6.

### 12.2. System Context Diagram

*Figure 1. System Context Diagram (Level 0)*

```
        ┌───────────────────────────────┐
        │      Administrator /          │
        │      Curator                  │
        └───────────┬───────────────────┘
   F01 Login Request│  Login Response
   F02 Manage Content│ CRUD Result
   F03 Manage Records│ Validation Result
   F04 Review Extraction│ Updated Status
   F05 Dashboard Request│ Overview Data
   F06 Evaluation Request│ Metrics Report
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                  H e r i t a g e G r a p h                  │
│                                                             │
│  Internal stores (relational database, vector index,        │
│  knowledge graph) sit inside this boundary and appear       │
│  only in the Level 1 decomposition.                        │
│                                                             │
│  F17 Content Analysis   ─┐  deterministic extraction        │
│  F18 Answer Generation  ─┴─ local fine-tuned model          │
│                             (no external AI service)        │
│                                                             │
└──────┬───────────────────────────────────┬──────────────────┘
       │                                   │
       │ F07 Register / Manage Account      │ Weather Forecast Request
       │     → Account Confirmation         │     → Forecast Response
       │ F08 Profile Inspection / Control   │ Points-of-Interest Request
       │     → Inferred Interest Profile    │     → POI Response
       │ F09 Personalized Exploration       │ Geocoding Request
       │     → Recommendations + paths      │     → Coordinate Response
       │ F10 Interest-Based Hybrid Search   │
       │     → Ranked Personalized Results  ▼
       │ F11 Natural Language Query   ┌────────────────────────┐
       │     → Answer + Citations     │  External Data         │
       │       or Insufficient Evidence│  Services             │
       │ F12 Proactive Context        │  (weather, map/POI,    │
       │     → Typed Advisory Cards   │   geocoding)           │
       │ F13 Entity Detail Request    └────────────────────────┘
       │     → Detail + Timeline + Related
       │ F14 Artifact Location
       │     → Floor Plan + Hotspot
       │ F15 Graph Exploration
       │     → Subgraph + Retrieval Trace
       │ F16 Data Export / Deletion
       │     → Data File / Confirmation
       ▼
┌───────────────────────────────┐
│            User               │
└───────────────────────────────┘
```

The context diagram shows HeritageGraph as a single process exchanging data with three external entities: **Administrator/Curator**, **User**, and **External Data Services** for weather, mapping and geocoding. Internal components — the relational database, the vector index and the knowledge graph — are intentionally not shown at this level because they sit inside the system boundary; they appear in the Level 1 decomposition. Every request flow has a matching response flow, forming **18 request/response pairs** in total, corresponding to F01–F18 in Section 7.1.

Two properties of this diagram are worth stating explicitly at review.

**There is no external AI service.** Content analysis is deterministic extraction with no model call, and answer generation runs on a local fine-tuned model. Cultural corpus text therefore never leaves the system, and the only outbound requests carry a coordinate, a place name or a date. This is a governance property, not only a cost decision.

**Personalization is visible at Level 0 rather than hidden inside a ranking step.** The interest profile is data the User both writes, through F08, and reads back through the ranked output of F09, F10 and F13. Per-user adaptation is therefore part of the system's external behaviour, not an internal implementation detail.

### 12.3. Retrieval Pipeline: Hybrid RAG + GraphRAG

The retrieval pipeline is the technical core of the platform, so it is specified here in the order of execution.

**Stage 1 — Index construction, once at startup.** Documents are split into passages with section headings weighted more heavily than body text. Three indexes are built over the same passage set: a BM25 index over word tokens, a BM25 index over diacritic-stripped character 4-grams, and a dense embedding index in pgvector. The knowledge graph is constructed in the same pass from a curated entity list, a closed classifier vocabulary, administrative-unit detection and temporal extraction, with every node linked to the source span that produced it.

**Stage 2 — Query analysis.** The query is analysed along three axes: region and category scope; intent, one of research, attend-event, plan-trip, learn, compare or verify; and the separation of the question's subject from any presupposition it contains, so that a question of the form *"X is in Y, right?"* is answered about X rather than about Y.

**Stage 3 — Three-channel retrieval, Hybrid RAG.** Each channel independently ranks passages. The word channel is precise on proper names, the n-gram channel absorbs missing diacritics and spelling variation, and the dense channel matches paraphrase and synonymy. The three rankings are combined by reciprocal rank fusion [9], which requires no score normalization because it uses rank position rather than score magnitude.

**Stage 4 — Graph anchoring, GraphRAG.** Entity labels and aliases are matched against the query, longest-match first, producing graph seeds. Whether the query anchors to any known entity, document, region or category is recorded, because it is the primary signal separating in-domain from out-of-domain questions.

**Stage 5 — Graph propagation.** From the seeds, affinity propagates two hops over typed, weighted relations with decay and with damping on hub nodes so that a broad category node does not flood the result set. This is what surfaces documents that share an administrative unit, a period or a co-mention with the query subject even when they share little vocabulary with it.

**Stage 6 — Fusion and two-tier scoring.** Candidate passages receive a passage-level score from lexical and dense evidence plus intent-aligned heading bonuses, and a document-level score adding graph affinity and a bonus when the query names the document explicitly. The document score selects which document answers, and the passage score selects which passage within it — separating the two prevents lexical noise from choosing among near-identical passages of the correct document.

**Stage 7 — Refusal gates.** Before any answer is generated, the retrieved evidence must pass structural gates: the query must anchor to a known graph node; a named entity must have supporting evidence in the retrieved passage rather than merely a similar one; lexical coverage must exceed a threshold; and administrative units named in the query must be ones the corpus knows. If any gate fails, the context is empty and the model produces an explicit refusal — behaviour it was fine-tuned to produce, so abstention lives in the model weights and not only in a conditional statement.

**Stage 8 — Context assembly and generation.** Selected passages are assembled under a character budget, with intent-driven substitution so that a location question receives the passage naming the province and an administrative question receives the passage naming the ward. The assembled context and the question are sent to the local fine-tuned model, which produces narration ending in a citation quoting a verbatim source sentence with its URL.

**Stage 9 — Citation validation and tracing.** The produced citation is checked against the retrieved context. The full decision — graph seeds, per-channel ranks, graph affinity, scoring components, gate outcomes — is available through the trace endpoint, so any answer can be audited after the fact.

### 12.4. Main Processing Flow

**Content ingestion.** A curator adds a document; the system normalizes it, splits it into passages with source locators, extracts entities, administrative units and years deterministically with evidence spans, computes passage embeddings, and rebuilds the graph with new nodes linked to their sources. A curator adds a venue, event or artifact record; the system validates that every factual field carries a source URL and sentence, rejects the record otherwise, persists it, and links it to the corresponding graph node.

**Question answering.** The pipeline of Section 12.3 runs, producing either narration with a citation or an explicit statement that the available evidence is insufficient.

**Personalization.** In parallel with answering, the question's subject becomes a recommendation seed. Candidates are scored by graph affinity to the seed, graph affinity to the interest profile, a bonus for belonging to a different cultural category while still being connected by a real path, and a penalty for items already seen. The ranked list is then diversified. Each item is returned with the graph path that produced it, so the interface can state why it was suggested.

**Proactive advice.** The detected intent selects card generators from the registry. Generators read typed records and, where needed, call external services with the venue coordinate and event date. External calls are issued concurrently with model generation so their latency is absorbed. Preparation advice is produced by explicit rules over the forecast. Every card carries its provenance and fetch time, and an unreachable service produces an explicit unavailable state rather than an invented value.

### 12.5. Example User Scenarios

Both scenarios deliberately use a non-monument entry point, because the platform's premise is that the entry point may be any kind of cultural object: an artifact, a dish, a performing art, a craft, or a festival.

**Scenario A — researching an artifact.** A user asks about a Cham-period stone sculpture. The answer layer explains the object from the corpus and cites a verbatim source sentence. Intent is classified as research, so the advisory layer adds the museum holding the object with its position on the floor plan, other artifacts of the same period in the same collection, and craft villages whose surviving techniques relate to it. The personalization layer, having recorded interest in sculpture and Cham material culture, recommends across categories — a related monument, a craft village, and a performing art connected through the graph — each displayed with the path justifying it. Nothing in the practical block is generated: museum, period, material and position are record fields with their own sources.

**Scenario B — attending a festival.** A user asks about a fishing-village festival. The answer layer explains its meaning and ritual structure with a citation. Intent is classified as attend-event, so the advisory layer returns the calendar type and this year's dates, the venue with its coordinate and map, the ritual and festivity segments, the forecast for that date with a preparation checklist derived by rule from the precipitation probability, a recommended viewpoint, and the nearest parking. The personalization layer recommends related culture: the local cuisine associated with the village, a nearby monument, and the folk performance staged during the festivity segment. If the weather service is unreachable, the card states that the forecast is unavailable rather than guessing.

**Scenario C — a false premise.** A user asks *"Cao lầu is a Huế speciality, isn't it?"*. Retrieval anchors on the dish, the evidence gate confirms the retrieved passage is about that dish rather than a similar one, and the generated answer opens by correcting the assumption before continuing — because the model was fine-tuned on false-premise correction rather than being left to agree politely.

## 13. Data Model Overview

The platform stores three kinds of data with different integrity requirements.

**Corpus and knowledge graph.** Documents carry region, category, aliases and passages with source locators. Graph nodes are documents, entities, administrative units, regions, categories and years. Relations are structural and evidence-bearing: document-to-entity mention, document-to-administrative-unit, document-to-region, document-to-category, document-to-year, document-to-document co-mention, and document-to-canonical-entity. No semantic relation is inferred, so the graph never asserts a fact the source does not state.

**Structured cultural records.** Venues carry coordinates, ward and district. Events carry calendar type, start and end dates, organizer and venue reference, and decompose into ordered ritual and festivity segments. Artifacts carry period, material, holding museum, room and floor-plan position. Points of interest carry kind, coordinate, source and fetch time. Every factual field of every record in this group carries a source URL and the source sentence it was read from, enforced by a database constraint rather than by application convention.

**User and interaction data.** Accounts carry credentials and a consent timestamp. Interest entries carry node reference, weight, the interaction kind that produced them, and last update, so the profile can be shown back to the user with its own justification. Interaction events carry kind, target node, dwell time and timestamp. The recommendation log carries seed, item, explanation path, rank, display time and click time, which is what makes offline evaluation of recommendation quality possible. The audit log records every curator change with before and after values.

## 14. Potential Risks and Mitigation Strategies

| Risk | Type | Impact | Mitigation |
| --- | --- | --- | --- |
| Scope exceeds the 15-week timeline | Schedule | High | One region pair and one theme set; a fixed cut order decided in advance (Section 14.1); Sprint 7 reserved as buffer |
| Corpus coverage uneven across categories | Data / AI | High | Corpus balancing scheduled in Sprint 2, before the recommender is built, and treated as a gate on starting Sprint 4 |
| Structured event, venue and artifact data must be authored by hand | Data / Schedule | High | Record counts capped at a demonstrable scope; every field requires a source; authoring is scheduled work with a whole sprint, not incidental effort |
| Advisory cards reintroduce hallucination | AI / Trust | High | Cards are rendered from typed records and never generated; enforced by an automated zero-fabricated-field assertion over the whole card test set |
| Recommendation quality is hard to measure without a user base | Evaluation | High | Two-rater relevance judgement with reported agreement; cross-domain rate and diversity computed objectively without human judgement |
| Cold start — a new user has no interest profile | AI / UX | Low | The recommender's seed term operates from the first interaction, so the first session is already useful; the profile term activates after two or three interactions. No preference form is required, which avoids asking users to describe interests they have not yet formed |
| Dense retrieval degrades on rare Vietnamese proper names | AI | Medium | Three-channel fusion means the lexical and n-gram channels carry proper names; per-channel contribution is inspectable in the trace |
| Point-of-interest coverage in the pilot area is sparse | Data / External | Medium | Verify coverage for demonstration venues early in Sprint 5; fall back to hand-authored points of interest with sources |
| Weather or mapping service unavailable during demonstration | External | Medium | Cache all external responses; cards degrade to an explicit unavailable state; degradation is itself a test case |
| Lunar-to-solar date conversion off by one day | Data | Medium | Hand-authored conversion table for pilot events over the demonstration period, with the limitation stated |
| End-to-end latency exceeds the target once cards are added | Performance | High | Measure from Sprint 1; overlap external calls with generation; cap generated tokens; response streaming as remediation |
| Personal data handling becomes a real obligation once behaviour is logged | Ethical / Legal | High | Consent before logging; store only what recommendation requires; export and deletion from Sprint 1; privacy review in Closing |
| Unauthenticated endpoints while personal data exists | Security | High | Authentication lands in Sprint 1, before any personal data is stored; no unauthenticated write path; no public network binding in the demo configuration |
| Incorrect Vietnamese proper-name extraction | Technical | High | Curated entity list, closed classifier vocabulary, alias dictionary, minimum-mention threshold, compound-name guards, and the rule that every extracted name is a literal source substring |
| Duplicate or renamed administrative names | Technical | Medium | Alias dictionary, recorded renames, and a dedicated administrative-relation test suite |
| Graph asserts relations without evidence | Trust / AI | High | Only structural relations are created — membership, mention, administrative, temporal, co-mention — and every node and edge links to a source span |
| Sensitive cultural content or misattribution | Ethical | High | Source and sentence on every structured field; curator review; domain-advisor review of festival and artifact records; explicit scope disclaimer |
| Prototype mistaken for an authoritative historical source | Communication | Medium | Visible sources and provenance on every claim; scope and status disclaimer in the interface |
| Single developer unavailable through illness | Schedule | High | Sprint 7 is an explicit buffer; the cut order below is decided in advance so triage under pressure requires no new judgement |

### 14.1. Fixed Cut Order Under Schedule Pressure

Decided in advance so that triage does not become improvisation. Reduce in this order: museum floor-plan hotspots, keeping a static plan image; shop and gift points of interest, keeping parking and viewpoints; the graph explorer, keeping the trace endpoint; the user study, from eight participants to four; the administrator interface, replaced by command-line tools plus a read-only statistics page.

**Never reduced, at any level of schedule pressure:** the refusal gates, mandatory citation, the zero-fabricated-field assertion on cards, and the evaluation suite. These constitute the project's contribution; without them the result is an unverified demonstration.

## 15. Expected Outcomes / Deliverables

### 15.1. Expected Outcomes

The project is expected to produce a platform in which a user's cultural interest — in an artifact, a dish, a performing art, a craft or a festival — becomes a personalized, explained path through related culture, and in which the practical requirements of actually participating are supplied automatically, while every displayed claim remains traceable to a source.

Technically, the project delivers a measurable end-to-end pipeline: ingestion, deterministic knowledge extraction, knowledge graph construction, three-channel Hybrid RAG retrieval fused with GraphRAG re-ranking, domain fine-tuned generation with citation validation and abstention, graph-path recommendation, and intent-driven advisory rendering.

Academically, the project offers three contributions beyond an application.

1. **A comparative retrieval result** for a low-resource Vietnamese cultural corpus, measuring each retrieval channel alone and in combination — sparse lexical, accent-insensitive n-gram, dense semantic, and each fused with graph re-ranking — so the contribution of graph structure is quantified rather than assumed.
2. **An explainable cold-start recommender** for cross-domain cultural discovery, in which the explanation is the propagation path and cross-domain rate is reported as a first-class metric rather than treated as a side effect.
3. **Evidence that proactive advisory capability can be added to a grounded question-answering system without regression in trustworthiness**, by separating narration from typed data — supported by before-and-after measurement of citation faithfulness and abstention accuracy across the advisory layer's introduction.

### 15.2. Deliverables

| No. | Deliverable | Description |
| --- | --- | --- |
| 1 | Web platform | HeritageGraph running in the demonstration environment |
| 2 | Cultural corpus | At least 80 normalized documents across six categories with passage locators and an alias dictionary |
| 3 | Knowledge graph | Schema, nodes, typed weighted relations, aliases, provenance and verification status |
| 4 | Structured cultural records | Venues with coordinates, events with calendar and ritual/festivity segments, artifacts with period, material and floor-plan position, points of interest — every field sourced |
| 5 | Hybrid RAG + GraphRAG retrieval engine | Three-channel retrieval, reciprocal rank fusion, graph anchoring and propagation, two-tier scoring, refusal gates, trace endpoint |
| 6 | Fine-tuned model and adapter | Domain adapter with training configuration, data-generation pipeline, checkpoint-selection rationale and reproducibility record |
| 7 | Grounded question answering | Vietnamese chat with citation validation, abstention and false-premise correction |
| 8 | Personalization module | Interest profile with time decay, graph-path recommender with cross-category bonus and diversity re-ranking, explanation paths, recommendation log |
| 9 | Proactive advisory module | Six-class intent classifier, card generator registry, weather and points-of-interest adapters, rule-based preparation advice, graceful degradation |
| 10 | Interactive card interface | Card-based chat, personalized exploration, entity detail pages, timeline, graph explorer, map view, museum floor plan with artifact hotspots |
| 11 | Administrator and curator tools | Content and record management with source validation, extraction review, audit log, corpus and graph health dashboard |
| 12 | Evaluation dataset | Question sets for retrieval, entity extraction, citation, abstention, intent classification and recommendation relevance, with documented construction methodology |
| 13 | Evaluation report | All metrics of Section 15.3 with error analysis, ablation of retrieval channels, and stated limitations |
| 14 | Test suite and CI | Unit, integration, API and end-to-end tests including the card-fabrication assertion, running in continuous integration |
| 15 | Technical documentation | SRS, architecture document, API specification, data schema, deployment guide |
| 16 | Testing documents | Test plan, test cases, test report and defect log |
| 17 | Final report | Project report with results, limitations and future directions |
| 18 | Demonstration materials | Demonstration video, presentation slides, user guide, and privacy and ethics review |

### 15.3. Success Criteria and Metrics

The project is successful when a user can complete the end-to-end flow — a curator ingests documents and authors records; the system produces passages, entities, relations, embeddings and graph data; the user explores a cultural object, receives explained cross-domain recommendations, asks a question in Vietnamese, and receives either a cited answer or an explicit statement of insufficient evidence together with the practical cards their intent implies — **and** the metrics below are measured and reported.

A missed target that is measured and explained is an acceptable capstone outcome. An unmeasured target is not.

| Metric | Target |
| --- | --- |
| Retrieval recall@1 and recall@3, in-domain | recall@1 at least 95%, including accent-free, alias and paraphrase queries |
| Retrieval channel ablation | Each channel measured alone and fused, with and without graph re-ranking, to quantify the graph's contribution |
| Out-of-domain refusal rate | At least 95% |
| Evidence-in-passage rate | At least 95% — the retrieved passage contains the specific evidence, not merely the right document |
| Entity extraction micro-F1 | At least 0.75, with per-type precision and recall reported |
| Citation faithfulness | At least 85% |
| Citation coverage of answerable questions | At least 90% |
| Abstention accuracy | At least 90% |
| False-premise correction rate | At least 90% of counter-premise questions corrected in the first sentence |
| Intent classification macro-F1 | At least 85% over at least 100 labelled questions, with a confusion matrix |
| Recommendation precision@5 | At least 70%, two raters, inter-rater agreement reported |
| Recommendation nDCG@5 | Reported |
| Personalization activation point | Number of interactions after which the profile term measurably changes ranking, reported |
| Cross-domain recommendation rate | At least 30% of top-five items in a different cultural category from the seed |
| Intra-list diversity | Category entropy within the top five, reported |
| Advisory card field correctness | 100% — zero fabricated fields, asserted automatically |
| Trustworthiness non-regression | No decrease in citation faithfulness or abstention accuracy after the advisory layer lands |
| p95 end-to-end latency | At most 8 seconds for a standard question in the demo environment |
| Entity detail page load | At most 3 seconds |
| Usability | System Usability Scale over 6–8 participants, reported as formative rather than statistical |

### 15.4. Known Limitations to State in the Final Report

Stated in advance rather than discovered at the defence.

- **One region pair.** All results are for Huế and Đà Nẵng. Nothing in the recommender or retrieval pipeline is region-specific, so the mechanism transfers, but a claim about culture outside the pilot corpus would not be supported by evidence. Regional expansion is the first item of future work.
- **Small evaluation scale for subjective metrics.** Recommendation relevance and usability rest on tens of judgements rather than thousands of users, and are reported as formative with agreement statistics.
- **Machine-prefilled entity labels** require human review, and the report must state what proportion was reviewed. Categories with few gold labels are reported with their label counts so that a high score on a sparse category is not over-interpreted.
- **Deterministic extraction means no semantic relations.** The graph knows that two entities are mentioned together, not that one built the other, so recommendation explanations are structural rather than causal.
- **In-memory graph and single-machine model** cap scale. Both are appropriate at the size of the pilot corpus and are not proposed as general solutions.
- **Hand-authored lunar-date conversion** covers the pilot events over the demonstration period only.
- **Point-of-interest data quality** depends on volunteer mapping and is uneven across the pilot area.
- **Weather forecasts extend roughly two weeks**, so events further ahead are shown with historical climate averages explicitly labelled as such.
- **The platform does not certify historical accuracy.** It reports what its sources say, with citations, and abstains where sources are silent.

## 16. Note on Scope and the Breadth of Culture

Culture covers many object types, and the platform is deliberately designed so that the entry point may be any of them. A user may begin from a performing art, a dish, a craft, a monument, a festival or a museum artifact, and in every case the same three layers apply: grounded answering, personalized cross-domain recommendation, and proactive practical context.

For this reason the two primary demonstration journeys of Section 12.5 are built around an **artifact** and a **festival** rather than around a monument, which is the object type most heavily represented in encyclopaedic sources. Any performing art, dish or craft named in the corpus works identically, because the mechanism operates over the graph rather than over hand-written rules per object type.

The mechanism is also region-independent: propagation runs over category membership, co-mention, shared administrative unit and shared period, none of which is specific to the pilot region. Extending the platform to another region requires new corpus documents and new structured records, not new algorithms — which is why Section 6.4 places multi-region coverage out of scope for the 15-week timeline while Section 15.4 records it as the first item of future work.

## 17. References

[1] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *Advances in Neural Information Processing Systems 33*, 2020. arXiv:2005.11401. https://arxiv.org/abs/2005.11401

[2] Microsoft Research, "Project GraphRAG: LLM-Derived Knowledge Graphs." https://www.microsoft.com/en-us/research/project/graphrag/

[3] D. Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization," 2024. arXiv:2404.16130. https://arxiv.org/abs/2404.16130

[4] UNESCO, "Digital technologies in the culture sector," MONDIACULT. https://www.unesco.org/en/mondiacult/digital-technologies-culture-sector

[5] Google Arts & Culture, "About the project." https://artsandculture.google.com/

[6] Google Arts & Culture, "Explore collections and stories." https://artsandculture.google.com/explore

[7] E. J. Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models," *International Conference on Learning Representations*, 2022. arXiv:2106.09685. https://arxiv.org/abs/2106.09685

[8] S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," *Foundations and Trends in Information Retrieval*, vol. 3, no. 4, pp. 333–389, 2009. https://dl.acm.org/doi/10.1561/1500000019

[9] G. V. Cormack, C. L. A. Clarke and S. Buettcher, "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods," *SIGIR*, 2009. https://dl.acm.org/doi/10.1145/1571941.1572114

[10] J. Carbonell and J. Goldstein, "The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries," *SIGIR*, 1998. https://dl.acm.org/doi/10.1145/290941.291025

[11] Y. Zhang and X. Chen, "Explainable Recommendation: A Survey and New Perspectives," *Foundations and Trends in Information Retrieval*, vol. 14, no. 1, pp. 1–101, 2020. arXiv:1804.11192. https://arxiv.org/abs/1804.11192

[12] Open-Meteo, "Free Weather API Documentation." https://open-meteo.com/en/docs

[13] OpenStreetMap Foundation, "Overpass API Documentation." https://wiki.openstreetmap.org/wiki/Overpass_API

[14] Nominatim, "Nominatim Geocoding Documentation." https://nominatim.org/release-docs/latest/

[15] Wikidata, "Wikidata: Introduction." https://www.wikidata.org/wiki/Wikidata:Introduction

[16] Scrum.org, "The 2020 Scrum Guide." https://scrumguides.org/scrum-guide.html

[17] Qwen Team, Alibaba Cloud, "Qwen2.5 Technical Report," 2024. arXiv:2412.15115. https://arxiv.org/abs/2412.15115

[18] Apple, "MLX: An array framework for Apple silicon." https://github.com/ml-explore/mlx

[19] A. Biryukov, D. Dinu and D. Khovratovich, "Argon2: New Generation of Memory-Hard Functions for Password Hashing and Other Applications," *IEEE European Symposium on Security and Privacy Workshops*, 2016. https://doi.org/10.1109/EuroSPW.2016.31

[20] W3C, "Web Content Accessibility Guidelines (WCAG) 2.1," W3C Recommendation, 2018. https://www.w3.org/TR/WCAG21/

[21] pgvector, "Open-source vector similarity search for Postgres." https://github.com/pgvector/pgvector

[22] N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," *EMNLP*, 2019. arXiv:1908.10084. https://arxiv.org/abs/1908.10084

## Appendix A — Feature Traceability Matrix

Each feature maps to the requirements that specify it and the metrics that verify it.

| Feature | Functional requirements | Verifying metrics |
| --- | --- | --- |
| F01 Login | FR01 | Security test cases |
| F02 Manage Cultural Content | FR02, FR04, FR05 | Entity F1; graph statistics |
| F03 Manage Structured Records | FR03 | Source-validation test cases; unsourced-field count |
| F04 Review Extraction Results | FR06 | Audit-log test cases |
| F05 Manager Dashboard | FR27 | Interface test cases |
| F06 Run Evaluation Suite | FR28 | Reproducibility record completeness |
| F07 Register and Manage Account | FR01 | Security test cases |
| F08 Interest Profile Inspection and Control | FR07, FR08 | Personalization activation point; scrutability test cases |
| F09 Personalized Exploration | FR09, FR10, FR11 | Precision@5; nDCG@5; cross-domain rate; intra-list diversity |
| F10 Interest-Based Hybrid Search | FR12, FR13 | recall@1 and recall@3; channel ablation |
| F11 Natural Language Query | FR14, FR15, FR16 | Citation faithfulness and coverage; abstention accuracy; false-premise correction rate |
| F12 Proactive Context | FR17, FR18, FR19, FR20, FR21 | Intent macro-F1; card field correctness; degradation test cases |
| F13 Entity Detail View | FR23 | Page load time; interface test cases |
| F14 Artifact Location | FR22 | Interface test cases |
| F15 Graph Exploration | FR24, FR25 | Trace completeness |
| F16 Personal Data Export and Deletion | FR26 | Privacy test cases |
| F17 Content Analysis | FR04, FR05 | Entity F1; evidence-span coverage |
| F18 Answer Generation | FR15, FR16 | Citation faithfulness; abstention accuracy |

## Appendix B — Submission Checklist

| Item | Status |
| --- | --- |
| Project title, team member and student ID completed | ☑ |
| Supervisor and department completed; email addresses to be filled | ☐ |
| Pilot locality and theme selected — Huế and Đà Nẵng, six cultural categories | ☑ |
| Source usage rights and attribution approach confirmed | ☐ |
| Database, embedding, retrieval and model technology finalized | ☑ |
| Sample corpus and evaluation question set created | ☐ |
| System context diagram reviewed — 18 request/response pairs, no external AI service | ☑ |
| 3D confirmed as future work, not a required item | ☑ |
| Objectives and acceptance criteria reviewed | ☑ |
| Domain advisor secured for festival and artifact record review | ☐ |
| Privacy and consent approach for behavioural logging reviewed | ☐ |
| Final formatting checked before submission | ☐ |
