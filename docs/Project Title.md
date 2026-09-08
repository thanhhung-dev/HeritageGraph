**International School**

**CAPSTONE PROJECT 1**

CMU-SE 450

**PROJECT DOCUMENT**

**Version 2.0 — Revised: September 5, 2026** (v1.0: August 21, 2026)

**A Personalized GraphRAG Assistant for Exploring, Understanding and Planning Local Cultural Experiences**

**Submitted by: C1SE.50**

Hung, Duong Thanh – 29219043370

**Approved by:**

**Msc. Nguyen Thi Thanh Tam**

**Proposal Review Panel Representative:**

Name: Signature: Date:

**Capstone Project 1 - Mentor:**

Name: **Msc. Nguyen Thi Thanh Tam** Signature: Date:

**Da Nang 9, 2026**

---

**PROJECT INFORMATION**

| Field | Value |
| --- | --- |
| Project title | A Personalized GraphRAG Assistant for Exploring, Understanding and Planning Local Cultural Experiences |
| Project acronym | CulturalMemoryGraph / CMG — product name **HeritageGraph** |
| Project duration | 27/08/2026 – 06/12/2026 (15 weeks; 13 weeks remaining as of this revision) |
| Institution | International School, CMU-SE 450 |
| Pilot locality / topic | **Huế and Đà Nẵng** — heritage sites, cuisine, performing arts, craft villages, festivals, museum artifacts |
| Project status | Capstone project proposal, revision 2.0 after mentor review |

**Note:** *This is a scope revision, not a new project. The retrieval engine, knowledge graph, fine-tuned model and evaluation harness described in Section 12.5 are already built and measured. Sections 6, 7, 11 and 14 have been rewritten to add the four capabilities requested in mentor review; Section 16 records exactly what was added and what was removed to keep the 15-week budget intact.*

---

## 1. Project Title

**A Personalized GraphRAG Assistant for Exploring, Understanding and Planning Local Cultural Experiences**

Each part of the title corresponds to a measurable capability rather than a slogan:

- **Personalized** — the system builds a per-user interest profile from explicit onboarding and implicit interaction, and uses it to rank and expand what the user sees. Two users typing the same query receive different, individually justified result sets. This is the primary differentiator identified in mentor review.
- **GraphRAG** — retrieval is anchored on a knowledge graph of entities, places, administrative units, time and documents, not on keyword matching alone. The graph is what makes cross-domain suggestion possible: recommendations travel along real, inspectable edges.
- **Exploring, Understanding** — citation-backed question answering in Vietnamese, with explicit abstention when evidence is insufficient.
- **Planning** — the system does not stop at explaining a cultural object. When it detects that the user is preparing to *attend* something, it proactively supplies the practical context needed to actually go: schedule, location, what to bring, where to stand, where to park.

The short name remains CulturalMemoryGraph (CMG); the product name remains HeritageGraph.

Title changed from v1.0 (*"An AI-Powered Platform for Preserving and Storytelling Local Cultural Memories Using GraphRAG"*) because v1.0 named the artifact (a storytelling archive) while the project's actual contribution is the behaviour: personalized, graph-explained, proactively contextual cultural guidance.

## 2. Team Members

| Full name | Student ID | Role | Email |
| --- | --- | --- | --- |
| Duong Thanh Hung | 29219043370 | All roles — requirements, AI/GraphRAG, data engineering, frontend, QA, documentation | *[to be filled before submission]* |

This is a one-member project. All roles listed in the standard template are merged into a single responsibility set: requirements analysis, development, testing, data management, evaluation and documentation. The supervisor provides direction, feedback and progress review. Because there is no peer reviewer inside the team, Section 11.3 defines an external review step for the two places where a single author is structurally unreliable: gold-label review and recommendation relevance judgement.

## 3. Supervisor(s)

| Full name | Title / Department | Role | Email |
| --- | --- | --- | --- |
| Msc. Nguyen Thi Thanh Tam | International School | Project Supervisor / Mentor | *[to be filled before submission]* |
| *[Domain advisor, if appointed]* | Museum / cultural centre | Domain Advisor — heritage content review | *[to be filled]* |

For cultural content the project additionally needs one domain contact with local knowledge — a museum staff member at the Museum of Cham Sculpture or the Museum of Royal Antiquities, a Huế Monuments Conservation Centre representative, or a history teacher — to review the structured festival and artifact records introduced in this revision (Section 7.1, F03).

## 4. Problem Statement

### 4.1. Background

Local cultural material about Huế and Đà Nẵng is abundant but structurally flat. Encyclopaedia articles, festival yearbooks, museum labels, gazetteers and tourism pages each describe one object at a time. A reader who arrives interested in one thing — a form of theatre, a dish, a statue, a festival — is given a single article and left to discover related culture by themselves.

Two distinct failures follow from this, and they are the two failures this project addresses.

**The first is that discovery is not personalized.** Search engines and heritage portals return the same ranked list to everybody. Interest in Huế royal court music and interest in Cham stone sculpture produce the same generic "related links" block, because relatedness is computed from text similarity or editorial curation, not from the user. Culture, however, is exactly the domain where interest is idiosyncratic and cross-cutting: a person drawn to one traditional performing art is usually also open to the costume, the instruments, the venue, the craft village that produces the props, and the festival where it is performed — but those live in different categories and different articles, so no existing tool connects them for that specific person.

**The second is that understanding is not actionable.** Existing cultural information systems answer "what is this?" and stop. The user's actual need is usually one step further and is never stated out loud. Somebody reading about a museum artifact implicitly wants to know which museum holds it, what else from the same period is there, and whether there is a comparable object or replica they can see or buy. Somebody reading about a festival implicitly wants to know when it happens this year, where to stand, whether it will rain, and where to leave a motorbike. Every one of those questions is answerable from data, and none of them is answered by a cultural corpus alone.

### 4.2. Core Problem

The project addresses **the absence of a cultural information system that adapts to the individual user and that anticipates the practical need behind a cultural query — while remaining verifiable.**

The final clause is what makes this hard rather than merely unbuilt. The two obvious ways to add personalization and proactivity both fail:

- **Collaborative filtering** (the standard commercial recommender) requires a large user base this project will never have, and produces unexplainable suggestions — it can tell a user *that* something is related but never *why*, which in a heritage and education context is a defect, not a cosmetic gap.
- **Letting a general-purpose language model improvise** the extra context reintroduces exactly the failure mode the project has already measured and eliminated. A model that will helpfully invent a parking location or a ticket price is a model that will invent a dynasty.

The problem is therefore to make a system personalized and proactive **without** buying either of those failures: recommendation must be explainable from graph structure, and practical context must be typed, sourced data rather than generated prose.

General-purpose chatbots do not solve this. Without a specific local corpus a model confuses Vietnamese place names, blends provinces, and states information that appears in no source. Retrieval-Augmented Generation addresses this by grounding generation in retrieved external memory [1]; GraphRAG extends it by combining text extraction, network analysis and LLM summarization over a graph structure [2], [3]. This project uses the graph for a second purpose beyond grounding: as the reasoning substrate for personalized cross-domain recommendation.

### 4.3. Importance of the Problem

UNESCO notes that digital technology can widen access to culture and support documentation, protection, promotion and inventory of heritage [4]. Access, however, is not only availability — it is also relevance and usability. A corpus nobody navigates is not accessible in any meaningful sense.

Personalized, explained navigation matters for cultural transmission specifically: it converts a single point of curiosity into a path through related heritage, which is how cultural literacy actually accumulates. And practical, correct planning support matters because it is the step at which cultural interest becomes cultural participation — the difference between reading about a festival and attending it.

### 4.4. Proposed Problem Response

The system is built as three layers over one verified knowledge substrate.

1. **A grounded answer layer** (already built and measured): graph-anchored retrieval, a domain fine-tuned Vietnamese model, mandatory sentence-level citation, and three structural refusal gates.
2. **A personalization layer** (new): an interest profile, and a recommender that scores candidates by graph affinity to the current subject, graph affinity to the profile, and an explicit bonus for candidates in a *different* cultural category that are nevertheless connected by a real path. Every suggestion is returned together with the path that produced it.
3. **A proactive advisory layer** (new): intent detection over the query, then a registry that maps intent to typed context blocks — schedule, venue, weather, preparation checklist, viewpoint, parking, comparable artifacts, related crafts.

The layer boundary is enforced by one architectural rule, stated here because it is the project's main design commitment and is referenced throughout this document:

> **The language model writes heritage narration only. Every practical or structured claim — date, coordinate, weather, parking, artifact attribute, recommendation — is rendered from a typed record carrying its own provenance, and never passes through generation.**

This keeps the measured trustworthiness of the answer layer intact while adding capabilities that would otherwise destroy it, and it yields a metric that is strong precisely because it is structural: no field of any practical card can be fabricated, and this is asserted automatically in the test suite (Section 14.3).

## 5. Survey / Existing Solutions

### 5.1. Retrieval-Augmented Generation and GraphRAG

Lewis et al. combine a parametric language model with a non-parametric memory retrieved from an external index, improving knowledge-intensive question answering and providing a retrieval basis for verification [1]. Microsoft Research's GraphRAG combines text extraction, network analysis and LLM prompting/summarization to reason over a dataset's structure rather than isolated passages [2]; Edge et al. detail the local-to-global query-focused summarization approach [3].

This project diverges from the reference GraphRAG implementation on one point, for a measured reason recorded in `docs/architecture.md`: the graph here is constructed **deterministically** from curated entity lists, a closed classifier vocabulary and regular expressions, not by LLM extraction. LLM extraction over this corpus on local hardware was estimated at 8–12 hours per index build, used English-language prompts on Vietnamese text, and could introduce entities absent from the source. The deterministic graph builds in 0.23 s and every node traces to a literal substring of a source document — which is a precondition for the recommendation explanations in F06.

### 5.2. Recommender Systems and the Explainability Requirement

Commercial recommendation is dominated by collaborative filtering and learned embeddings, which need scale and produce opaque output. This project uses **graph-path recommendation** instead: candidates are scored by weighted propagation over the heritage graph, and the propagation path is returned as the explanation. This is feasible for a cold-start, single-locality system with no user base, is auditable, and directly supports the cross-domain requirement — a bonus term rewards candidates reached through a real path but belonging to a different cultural category, which is the mechanical definition of "suggest related culture, not more of the same".

### 5.3. Comparable Platforms

Google Arts & Culture aggregates digitized collections and curated place-based stories from museums worldwide [5], [6]. It shares HeritageGraph's experience goal of pairing images with narrative context, but relatedness is editorially curated, there is no entity–relation graph exposed to the user, no citation-backed open-ended Q&A over a specific local corpus, and no per-user interest model.

Tourism platforms (booking and destination portals) do supply practical logistics, but they are commerce-first: they contain no cultural knowledge graph, no source citation, and no abstention behaviour.

### 5.4. Comparison with Existing Approaches

| Criterion | Static heritage site / gazetteer | General-purpose LLM chatbot | Google Arts & Culture | Tourism / booking portal | **HeritageGraph v2** |
| --- | --- | --- | --- | --- | --- |
| Primary data | Isolated articles and captions | Knowledge inside model weights | Curated museum exhibits | Commercial listings | Local corpus + knowledge graph + typed records |
| Person–place–event–time links | Usually absent | Not reliable | Editorially curated | Absent | Deterministic graph with provenance per node |
| Personalization | None | Conversational memory only | Minimal | Commercial intent targeting | Interest profile + graph-path scoring |
| Explainable "why this?" | No | No | No | No | **Yes — propagation path is returned** |
| Cross-domain suggestion | No | Unverifiable | Within curated exhibits | No | **Explicit cross-category bonus term** |
| Passage-level citation | Occasional | Not guaranteed | Exhibit-level credit | No | **Mandatory, measured** |
| Abstention when evidence is missing | N/A | Rare | N/A | N/A | **Three structural gates, measured** |
| Practical planning context | No | Unverifiable | No | Yes, commerce-first | **Yes, typed and sourced** |
| Feasibility as a capstone | High, low value | High, uncontrollable sources | Needs partner network | Needs commercial data | Fits the remaining 13 weeks |

### 5.5. Project Differentiation

HeritageGraph does not claim to replace professional preservation systems or large aggregators. Its contribution is the combination that none of the four comparators has: **per-user personalization and proactive practical context, delivered on top of a verifiable, citation-backed, abstaining answer engine — with every recommendation explainable as a graph path and every practical claim traceable to a typed source record.**

## 6. Objectives and Scope

### 6.1. General Objective

Build and evaluate a web-based AI prototype for the culture of Huế and Đà Nẵng that (a) answers Vietnamese-language questions from a local corpus with sentence-level citations and explicit abstention, (b) personalizes what each user is shown using an interest profile and an explainable graph-path recommender, and (c) proactively supplies the typed practical context implied by the user's intent — schedule, venue, weather, preparation, viewpoint, parking, comparable artifacts and related crafts.

### 6.2. Specific Objectives

**Knowledge base**

- Maintain a corpus of at least **80 documents** covering all six cultural categories with at least **8 documents per category**, so that cross-domain recommendation has depth in every direction. *(Current: 45 documents / 349 passages, with Performing Arts at 4, Festivals at 2 and Craft Villages at 2 — the category imbalance is the single largest data risk to the personalization objective and is scheduled first, Section 11.2 Week 4.)*
- Maintain the deterministic knowledge graph over documents, entities, administrative units, regions, categories and years, with every node traceable to a literal source span. *(Current: 510 nodes / 1135 edges, 1 connected component, 0 isolated documents, build time 0.23 s.)*
- Author three new structured record sets, each field carrying a source URL and the source sentence it was read from: **≥ 50 venues with coordinates**, **≥ 20 festivals/events with calendar type, dates, organizer and ritual/festivity segments**, and **≥ 35 museum artifacts with period, material, holding museum and floor-plan position**.

**Answer layer (built; to be re-measured on the final corpus)**

- Vietnamese text-only question answering with mandatory citation in the form `[Nguồn: <verbatim sentence> — <url>]` and abstention when evidence is insufficient.
- Entity extraction over four types (person, place, event, time) as strict JSON.

**Personalization layer (new)**

- Capture interests explicitly at onboarding and implicitly from interaction, with time decay.
- Rank and expand results per user; return with every recommendation the graph path that justifies it.
- Achieve a measurable **cross-domain rate** — the proportion of recommendations belonging to a different cultural category than the seed — rather than only intra-category "more of the same".

**Advisory layer (new)**

- Classify query intent into six classes (research, attend event, plan trip, learn, compare, verify).
- Render intent-appropriate typed context blocks, with zero fabricated fields, asserted by automated test.

**Evaluation**

- Report entity F1, citation faithfulness, abstention accuracy, retrieval recall, intent accuracy, recommendation precision@5 and nDCG@5 with inter-rater agreement, cross-domain rate, card field correctness, and p95 latency.

### 6.3. In Scope

One pilot region pair (Huế and Đà Nẵng) across six cultural categories; Vietnamese text-only chat; the deterministic knowledge graph; graph-anchored hybrid retrieval; the domain fine-tuned model with citation and abstention; user accounts with authentication; the interest profile and explainable recommender; intent classification; typed advisory cards including weather and points of interest from free public APIs; **one** museum floor plan with hotspots; a curator/admin content review path; the evaluation suite and report.

End users submit text only; they do not upload images or documents through the chat interface.

### 6.4. Out of Scope

3D modelling, LiDAR, photogrammetry, digital twins and virtual tours; professional GIS; video recognition; large-scale OCR of scanned documents; multilingual translation and interface localization; ticket or tour booking and any commercial transaction; real-time crowd or transport data; official historical certification of content; collaborative-filtering recommendation requiring a user base; native mobile applications.

Also explicitly removed from v1.0 scope in this revision, in exchange for the four new capability groups (full accounting in Section 16): the image-first gallery and image-upload pipeline, multi-image stories with camera paths and milestones, the DOCX ingestion pipeline, and the separate vector index. Rationale for each removal is recorded in Section 16.2; all four are listed as future work.

## 7. Key Features & Requirements

### 7.1. Core Features

Features are grouped by actor. Admin/Curator features are F01–F04, User features F05–F10, and internal AI service exchanges F11–F12. Every request flow has a matching response flow, giving **12 request/response pairs** in the system context diagram (Section 12.2) — v1.0 had 10; F06 was split and F09 and F10 are new.

| Code | Feature | Actor | Description | Status |
| --- | --- | --- | --- | --- |
| F01 | Login Request | Admin | Admin authenticates; system returns a Login Response and a session credential | New |
| F02 | Manage Cultural Content Request | Admin | CRUD over documents, aliases and category/region assignment; system returns the CRUD Result and triggers a graph rebuild | New |
| F03 | Manage Structured Records Request | Admin | CRUD over the three new typed record sets — venues with coordinates, events with calendar and segments, artifacts with period/material/position — each field requiring a source URL and source sentence; system returns a Validation Result that **rejects any record with an unsourced field** | New |
| F04 | Manager Dashboard Request | Admin | Admin requests corpus and graph health; system returns Dashboard Overview Data (document counts per category, graph statistics, unsourced-field count, latest evaluation metrics) | New |
| F05 | Interest Onboarding / Profile Update | User | User selects cultural categories and specific items of interest, or edits an existing profile; system returns the stored Interest Profile. Solves cold start | New |
| F06 | Personalized Exploration Request | User | User opens a topic, place, artifact, dish or festival; system returns a **Personalized Recommendation List with a graph-path explanation per item**, including cross-category items | New |
| F07 | Interest-Based Search Query | User | User searches by keyword; system returns Ranked Results re-ranked by the interest profile | New |
| F08 | Natural Language Query (Text) | User | User submits a free-text cultural question in Vietnamese; system returns an Answer with Source Citations, or an explicit statement that evidence is insufficient | **Built** |
| F09 | Proactive Context Request | User | Triggered by detected intent on F06 or F08; system returns **typed Advisory Cards** — event schedule, venue map, weather and preparation checklist, best viewpoint, nearest parking, comparable artifacts, related crafts — each card carrying its provenance | New |
| F10 | Artifact Location Request | User | User asks where an artifact is displayed; system returns the museum floor plan with the hotspot highlighted | New |
| F11 | Content Analysis Request | Internal | System sends document text to the analysis component; returns Extracted Entities & Relations used to build the graph. Runs on F02 | **Built** (deterministic, local) |
| F12 | Answer Generation Request | Internal | System sends assembled context and question to the local fine-tuned model; returns Generated Narration. Runs on F08 | **Built** (local model) |

Two notes the review panel will ask about.

**F11 and F12 are internal and local.** v1.0 drew them as an "External AI/LLM Service". Both now run in-process on local hardware: F11 is deterministic graph construction with no model call at all, F12 is a locally hosted 3-billion-parameter model with a domain adapter. This removes the API-cost risk from v1.0 and removes any dependency on an external provider — cultural corpus text never leaves the machine.

**F09 is the feature that must not be allowed to hallucinate.** Its cards are rendered from typed records and free public APIs (weather, points of interest) and are never produced by generation. The trigger is intent detection, not an explicit user click, which is what makes it "proactive" in the sense requested at mentor review — the system infers the unstated need.

Dependency: F06, F07, F08, F09 and F10 all depend on the graph built by F11; F06 and F07 additionally depend on the profile from F05; F09 additionally depends on the structured records from F03. F09's weather and parking cards degrade gracefully to "not available" when an external API is unreachable, and this degradation is itself a test case.

### 7.2. Functional Requirements

| Code | Functional Requirement | Acceptance Criteria |
| --- | --- | --- |
| FR01 | A user can register and authenticate | Password stored only as an argon2id hash; session credential issued as an HttpOnly cookie; protected endpoints reject unauthenticated requests |
| FR02 | Admin can add or edit a corpus document | Document is normalized, split into passages with source locators, and the graph is rebuilt with the new nodes linked to their source |
| FR03 | Admin can add structured venue, event and artifact records | The record is saved only if every factual field carries a source URL and source sentence; unsourced fields are rejected with a field-level error |
| FR04 | The system extracts entities and relations from a document | Output matches the four-type schema and every extracted name is a literal substring of the source |
| FR05 | The system builds and updates the knowledge graph | Nodes and edges are created, typed, weighted and linked to source documents; graph statistics are reported |
| FR06 | A user can complete interest onboarding | At least three categories and three specific items can be selected; the profile is persisted and editable |
| FR07 | The system records interaction implicitly | View, dwell, card click, save and dismiss events are logged with timestamp and target node; profile weights update with time decay |
| FR08 | The system returns personalized recommendations | For a given subject and profile, the system returns a ranked list in which **each item is accompanied by the graph path that produced it** |
| FR09 | Recommendations include cross-category items | For seeds whose category is connected in the graph, at least one of the top five recommendations belongs to a different cultural category |
| FR10 | A user can submit a Vietnamese text-only question | The chat interface accepts text only; the answer is generated solely from retrieved context |
| FR11 | Answers include citations or state insufficient evidence | No assertive answer is produced without a supporting cited sentence from a retrieved source |
| FR12 | The system classifies query intent | The query is assigned to one of six intent classes; the assigned class is recorded and inspectable |
| FR13 | The system returns advisory cards appropriate to intent | Cards match the intent-to-generator registry; **every card field equals the corresponding field of its source record or API response, with no generated field** |
| FR14 | The system supplies event schedule and venue detail | For an event in the corpus the system returns name, calendar type and dates, venue with coordinates, organizer, and ritual/festivity segments |
| FR15 | The system supplies weather and a preparation checklist for a dated event | Forecast is retrieved from a public weather API for the venue coordinates; the checklist is produced by explicit rules over the forecast, not by generation |
| FR16 | The system shows an artifact's position on a museum floor plan | The requested artifact's hotspot is highlighted on the floor plan of the holding museum |
| FR17 | Admin can confirm or correct extraction and record data | The change and the acting user are written to an audit log |
| FR18 | The system can run the full evaluation suite | All metrics in Section 14.3 are computed and exported as a report file recording model, adapter checkpoint, prompt version, corpus version and evaluation configuration |
| FR19 | A user can export and delete their own personal data | Profile and interaction history are returned in a machine-readable file and can be permanently deleted on request |

### 7.3. Non-functional Requirements

| Code | Group | Requirement |
| --- | --- | --- |
| NFR01 | Performance | p95 end-to-end latency for a standard question does not exceed 8 s in the demo environment; measured continuously from Week 3, not at the end |
| NFR02 | Performance | Recommendation and advisory-card responses return within 2 s excluding language-model generation; external API calls run concurrently with generation |
| NFR03 | Accuracy | Retrieval recall@1 on the in-domain question set is at least 95% |
| NFR04 | Trustworthiness | Citation faithfulness is at least 85% and citation coverage of answerable questions at least 90% |
| NFR05 | Safety | Abstention accuracy is at least 90%; a fabricated assertive answer on an out-of-domain question counts as a failure |
| NFR06 | Safety | **Zero fabricated fields in advisory cards**, asserted automatically over the whole card test set |
| NFR07 | Explainability | Every recommendation exposes a human-readable graph path; a recommendation without a path is a defect |
| NFR08 | Usability | A new user can complete onboarding and ask a question without written instructions |
| NFR09 | Accessibility | Text alternatives for all non-text content; sufficient contrast; keyboard-navigable chat and cards; the chat transcript is announced to assistive technology |
| NFR10 | Security | Authentication on every endpoint that reads or writes personal data; input validation; no unauthenticated write path; the server does not bind a public interface in the demo configuration |
| NFR11 | Privacy | Interaction logging requires informed consent; only data needed for recommendation is stored; export and deletion are supported (FR19) |
| NFR12 | Provenance | Every displayed factual claim resolves to a source — a corpus sentence, a structured record field with its source, or a named external API with a fetch timestamp |
| NFR13 | Maintainability | Ingestion, graph, retrieval, generation, recommendation, advisory and interface concerns remain separately interfaced modules |
| NFR14 | Reproducibility | Model identifier, adapter checkpoint, prompt version, corpus version, graph statistics and evaluation configuration are recorded in every report file |
| NFR15 | Scalability | A new region, category, event, venue or artifact can be added without code changes; a new advisory card type is added by registering one generator |

## 8. Constraints and Assumptions

### 8.1. Constraints

| Constraint group | Description |
| --- | --- |
| Time | 13 of the original 15 weeks remain as of this revision. This is the binding constraint and the reason Section 16.2 removes four v1.0 feature groups rather than adding four on top |
| Team | One developer. No parallel workstreams; no internal code review; relevance judgement and gold-label review require an external second rater (Section 11.3) |
| Hardware | Development and demonstration on a single Apple Silicon laptop. This fixes the model at a 4-bit quantized 3-billion-parameter class and makes generation latency the dominant term in NFR01 |
| Corpus | Encyclopaedic sources are uneven by category: heritage sites are deep, performing arts and craft villages are thin, festivals are almost absent. Structured event, venue and artifact data does not exist in the sources at all and must be authored by hand with citations |
| Language | Vietnamese proper names, aliases, diacritics and accent-free typing are inconsistent; administrative names changed in recent reorganizations |
| External data | Weather and points-of-interest APIs are free and unauthenticated but have rate limits, and open-map point-of-interest coverage in Vietnam is uneven — parking and shop data may be absent for a given venue |
| Calendar | Vietnamese festival dates are given in the lunar calendar; general-purpose lunar libraries follow the Chinese calendar and can differ by one day at the UTC+7 boundary |
| Evaluation | With one developer and no user base, recommendation relevance and narration style cannot be measured at statistical scale; they are reported as small-sample judgements with agreement statistics, and labelled as such |

### 8.2. Assumptions

- Encyclopaedic and official cultural sources for Huế and Đà Nẵng remain publicly accessible for the corpus expansion in Week 4, and their reuse for a non-commercial academic prototype is permissible with attribution.
- Structured event, venue and artifact facts can be sourced from official monument-centre, museum and municipal publications, each recorded with a citable URL and sentence.
- Free public weather and map APIs remain available without an API key at the request volume of a demonstration.
- The demonstration machine can run retrieval, graph, database and local model together at small scale.
- Users have a browser and network access; they only type text and never upload files.
- The goal is to demonstrate pipeline feasibility and measurable trustworthiness, not to deploy an archival system of record.
- AI narration is treated as a suggestion subject to curator confirmation; structured records are treated as authoritative only to the extent of their cited source.
- Interaction logging is consented to; a user may explore without a profile, in which case recommendations fall back to graph affinity to the current subject alone.

## 9. Target Users / Stakeholders

| Group | Needs | How the system helps |
| --- | --- | --- |
| Students and young people | Learn about culture quickly, visually, following their own curiosity | Interest profile, cross-domain recommendations with visible reasons, citation-backed answers |
| Domestic and cultural travellers | Decide what to see and how to actually attend it | Event schedule, venue map, weather and preparation checklist, viewpoint and parking cards |
| Teachers | Visual, sourced material for lessons | Category and region browsing, citations usable as references, entity extraction over supplied passages |
| Museums, libraries, cultural centres | Present collections and connect them to wider context | Structured artifact records with floor-plan position; graph links from artifact to period, place and craft |
| Researchers | Find relationships, cross-check sources, spot gaps | Inspectable graph, passage-level retrieval traces, aliases, provenance on every node |
| Artisans and local communities | Have their knowledge recorded accurately and attributed | Source URL and sentence on every structured field; curator review; stated scope limits |
| Developer | A testable AI and software engineering problem | Modular architecture, typed API, evaluation harness, measurable objectives |
| Supervisor / review panel | Assess feasibility, rigour and contribution | Explicit v1.0→v2.0 scope accounting (Section 16), measured baselines, honest limitation reporting (Section 14.4) |

## 10. Technology Stack

| Component | Technology | Purpose | Status |
| --- | --- | --- | --- |
| Frontend | Next.js (App Router), React, TypeScript, Tailwind CSS | Chat with cards, exploration, onboarding, map, floor plan, admin | Chat exists as a single minimal page; Tailwind and the card system are new |
| Backend | Python, FastAPI, Pydantic | REST API, retrieval, orchestration, recommendation, evaluation | Built; extended |
| Relational database | PostgreSQL with SQLAlchemy and Alembic migrations | Users, interest profiles, interaction events, venues, events, artifacts, points of interest, audit log, recommendation log | **New — the project currently has no database at all; all state is files plus an in-memory cache** |
| Knowledge graph | NetworkX, built deterministically in memory at startup | Entities, documents, regions, categories, administrative units, years, provenance | Built |
| Retrieval | Two hand-implemented BM25 indexes (word tokens and accent-stripped character n-grams) fused by reciprocal rank fusion, then re-ranked by graph propagation | Tolerates accent-free typing; anchors on graph entities | Built |
| Language model | Locally hosted 4-bit quantized Qwen2.5-3B-Instruct with a LoRA adapter, served through MLX | Vietnamese heritage narration, citation format, abstention, entity JSON | Built |
| Fine-tuning | MLX LoRA, rank 16 over the last 16 layers, prompt-masked loss | Teaches register, citation format, abstention and false-premise correction — not facts | Built |
| Intent classification | Rule and lexicon based, six classes, over accent-stripped text | Chooses which advisory cards to render; auditable and cheap | New; extends the existing four-signal intent function |
| Recommendation | Graph propagation with profile affinity, cross-category bonus and diversity re-ranking | Personalized, explainable suggestion | New |
| Weather | Open-Meteo (no key required) | Hourly precipitation probability and temperature for the preparation checklist | New |
| Map and points of interest | OpenStreetMap via Overpass; Nominatim for one-time geocoding with caching; Leaflet for display | Parking, viewpoints, craft and gift shops, venue map | New |
| Museum floor plan | Hand-authored SVG with hotspot coordinates | Artifact position display | New |
| Testing | pytest, Playwright, GitHub Actions | Unit, integration, API, end-to-end, and the card-fabrication assertion | **New — the project currently has no test framework and no CI** |
| Deployment | Docker Compose for the database; local server for the demonstration | Reproducible environment | New |
| Documentation | Markdown, Mermaid, OpenAPI | Requirements, architecture, API, evaluation reports | Partial |

Two deliberate departures from the v1.0 stack table, both already validated by measurement and recorded in `docs/architecture.md`:

**No separate vector database and no embedding model.** v1.0 proposed Qdrant or pgvector. The implemented hybrid — word BM25 plus accent-stripped n-gram BM25, fused and then re-ranked by graph propagation — reaches recall@1 of 30/30 on the in-domain question set including accent-free and alias queries, which leaves a vector index with no measurable deficit to fix. It is recorded as future work rather than removed silently.

**No Neo4j.** The graph is 510 nodes and 1135 edges and rebuilds in 0.23 s in memory. A graph database at this scale adds an operational dependency and no capability; PostgreSQL holds persistent application state instead. Both decisions are revisited in Section 14.4 as scalability limits.

## 11. Methodology & Development Plan

### 11.1. Development Methodology

Agile with one-week increments and a demonstration to the supervisor at each increment. Short cycles are appropriate because recommendation quality, intent accuracy and advisory usefulness can only be judged against real data and real interaction, not specified in advance.

Two sequencing rules govern the remaining weeks.

**Risk first.** The three highest-risk items are scheduled earliest: the scope agreement with the supervisor (Week 2), the corpus category imbalance and the hand-authored structured records that every advisory card depends on (Week 4), and continuous latency measurement from the moment the database and authentication land (Week 3) rather than in the testing phase.

**No feature is built on an unmeasured baseline.** Week 2 closes the measurement debt in the existing system before any new capability is added, because a personalization result presented on top of an unverified answer layer is not defensible at review.

### 11.2. Development Plan

Thirteen weeks remain. Week numbering continues from the original plan.

| Week | Phase | Main content | Output |
| --- | --- | --- | --- |
| 2 | Scope and measurement debt | Agree the v2.0 scope and the four removals with the supervisor in writing; correct all stale figures in the documentation; fix the one known retrieval leak; re-measure the base model on the current evaluation set so the before/after comparison is valid; record the adapter checkpoint in report files | Signed scope delta; corrected documents; retrieval suite passing; comparable baseline |
| 3 | Foundation | PostgreSQL with Docker Compose and migrations; data model; registration and login with argon2id and HttpOnly session cookie; interaction-event logging with consent; Tailwind; extended chat response schema; **first latency measurement** | Working accounts, persistence, event log, latency baseline |
| 4 | Domain data | Expand the corpus toward 80 documents with at least 8 per category; author venues with coordinates, events with calendar and segments, and artifacts with period, material and position — every field sourced; rebuild graph; regenerate the evaluation gold set; re-run retrieval evaluation | Balanced corpus, three structured record sets, refreshed evaluation set — **F03 and F14 complete** |
| 5–6 | Personalization | Interest profile with decay; onboarding; graph affinity, profile affinity, cross-category bonus, diversity re-ranking; recommendation endpoint returning explanation paths; recommendation logging; exploration and detail interface with a related-content rail | **F05, F06, F07 complete** |
| 7–8 | Proactive advisory | Six-class intent classifier and its labelled question set; intent-to-card registry; weather integration; points-of-interest integration with caching; preparation-checklist rules; concurrent external fetch overlapped with generation; graceful degradation when an API is unavailable | **F09 complete** |
| 9–10 | Card interface and floor plan | Card renderer registry; map display; one museum floor plan as authored SVG with hotspots; artifact-position interaction; accessibility pass on chat and cards | **F04, F10 complete** |
| 11 | Artifact and festival journeys, buffer | End-to-end research journey (artifact → holding museum → same-period artifacts → related craft village) and attendance journey (festival → schedule → venue → weather → preparation → viewpoint → parking); absorb slippage | Two complete demonstration journeys |
| 12–13 | Testing and evaluation | pytest and Playwright suites with CI; the card-fabrication assertion; full metric set including intent accuracy and recommendation precision with a second rater; small user study; latency remediation if NFR01 fails | Test report and evaluation report |
| 14–15 | Closing | Architecture, API and schema documentation; privacy and ethics review including consent, minimization, export and deletion; demonstration video, slides and user guide; final report | Final accepted version |

### 11.3. Quality, Review and Version Control

Source is managed with Git. Any change to the graph construction rules, prompt, model, adapter checkpoint, corpus or database schema is recorded in a changelog, because each one invalidates previously reported metrics. Continuous integration runs linting and the test suite before merge.

Because there is no second developer, two places where single authorship is structurally unreliable use an external rater:

- **Entity gold labels** are currently machine pre-filled from the deterministic graph and are marked as such. As they stand they measure whether the model learned the extraction rule set, not whether extraction is correct. They require human review before the final report, and the report must state which portion was reviewed.
- **Recommendation relevance** is judged by two raters over the same seed set, and inter-rater agreement is reported alongside precision. A single-rater relevance number authored by the developer of the recommender is not evidence.

For cultural content, every structured field records its source URL and source sentence, and the curator review status is stored. For AI components, every report file records model identifier, adapter checkpoint, prompt version, corpus version and evaluation configuration (NFR14).

## 12. System Architecture Overview

### 12.1. Architecture Description

Seven layers. The three in bold are new in v2.0.

1. **Presentation** — chat with typed cards, exploration and detail pages, onboarding, map, museum floor plan, citation panel, admin review.
2. **Application / API** — authentication, chat, personalized exploration, search, recommendation, advisory, graph inspection, admin content and record management, evaluation.
3. **Ingestion** — source resolution and fetching, normalization, passage splitting with source locators, alias extraction.
4. **Knowledge processing** — deterministic entity and year extraction with a closed classifier vocabulary, administrative-unit detection, graph construction with typed weighted edges and provenance.
5. **Storage** — corpus files, the in-memory graph, and PostgreSQL for users, interest profiles, interaction events, venues, events, artifacts, points of interest, recommendation log and audit log.
6. **AI orchestration** — query analysis (scope, intent, subject versus presupposition), hybrid retrieval, graph propagation, context assembly, three refusal gates, generation, citation validation.
7. **Personalization and advisory** — profile maintenance with decay, graph-path recommendation with cross-category bonus and diversity, intent classification, and the intent-to-card generator registry with external adapters for weather and points of interest.

The architectural rule from Section 4.4 is enforced at the layer boundary: layer 6 produces narration prose; layer 7 produces typed card objects. Card objects never pass through layer 6.

### 12.2. System Context Diagram

*Figure 1. System Context Diagram (Level 0)*

HeritageGraph is shown as one process exchanging data with three external entities: **Admin/Curator**, **User**, and **External Data Services** (weather and map/points-of-interest providers). Internal stores — the relational database and the knowledge graph — sit inside the system boundary and appear only in the Level 1 decomposition. Every request has a matching response, giving 12 request/response pairs (Section 7.1).

Admin/Curator sends a Login Request, a Manage Cultural Content Request, a Manage Structured Records Request and a Manager Dashboard Request, receiving a Login Response, a CRUD Result, a Validation Result and Dashboard Overview Data.

User sends an Interest Onboarding / Profile Update, a Personalized Exploration Request, an Interest-Based Search Query, a Natural Language Query, a Proactive Context Request and an Artifact Location Request, receiving the stored Interest Profile, a Personalized Recommendation List with graph-path explanations, Ranked Personalized Results, an Answer with Source Citations or an insufficient-evidence statement, typed Advisory Cards with provenance, and a Floor Plan with the artifact hotspot highlighted.

The System sends a Weather Forecast Request and a Points-of-Interest Request to External Data Services and receives a Forecast Response and a Points-of-Interest Response.

Two changes from the v1.0 diagram must be pointed out at review. **The "External AI/LLM Service" entity is gone**: content analysis and answer generation are internal, deterministic and local respectively, so both flows moved inside the boundary. **A new "External Data Services" entity appears**, carrying only non-cultural logistics data. The direction of the change matters — cultural content no longer leaves the system, while the only outbound calls carry a coordinate and a date.

Personalization is explicit in this diagram rather than hidden: the interest profile is an entity the User both writes (F05) and reads back through ranked output (F06, F07), so per-user adaptation is visible at Level 0 instead of buried in an internal ranking step.

### 12.3. Main Processing Flow

**Content ingestion.** A curator adds a document; the system normalizes it, splits it into passages with source locators, extracts entities and years deterministically, detects administrative units, and rebuilds the graph with new nodes linked to their sources. A curator adds a venue, event or artifact record; the system validates that every factual field carries a source URL and sentence, rejects the record otherwise, writes it to the database, and links it to the corresponding graph node.

**Question answering.** The query is analysed for region and category scope, intent, and the distinction between its subject and any presupposition it contains. Two BM25 rankings are computed and fused; graph seeds are matched from entity labels and aliases; propagation over the graph produces document affinities; candidates are scored with graph affinity and named-document bonuses; the best passages are assembled into context. Three gates then decide whether to answer at all: the query must anchor to a known graph node, a named entity must have supporting evidence in the retrieved passage, and lexical coverage must exceed a threshold. If any gate fails, context is empty and the model answers with an explicit refusal — a behaviour it was fine-tuned to produce, so the refusal is in the weights and not only in a conditional statement.

**Personalization.** In parallel with answering, the subject is used as a recommendation seed. Candidates are scored by graph affinity to the seed, graph affinity to the interest profile, a bonus for belonging to a different cultural category while still being connected by a real path, and a penalty for items already seen; the ranked list is diversified so it does not return five instances of the same kind of site. Each returned item carries the path that produced it.

**Proactive advice.** The detected intent selects card generators from the registry. Generators read typed records and, where needed, call external services for the venue coordinate and event date. Weather and points-of-interest calls are issued concurrently with model generation so their latency hides inside generation time. Preparation advice is produced by explicit rules over the forecast. Every card is returned with its provenance and fetch time; an unavailable service yields an explicit unavailable state rather than an invented value.

### 12.4. Example User Scenarios

The two scenarios below are the demonstration journeys built in Week 11, and they correspond directly to the two examples raised at mentor review. Both are deliberately shown with a *non-heritage-site* entry point, because the point of the personalization layer is that the entry point can be any kind of cultural object — an artifact, a dish, a performing art, a craft, or a festival.

**Scenario A — research on an artifact.** A user reads about a Cham-period stone sculpture. The answer layer explains the object from the corpus with a cited sentence. Intent is classified as research, so the advisory layer adds: the museum that holds it with its position on the floor plan, other artifacts of the same period in the same collection, and the craft villages whose surviving techniques relate to it. The personalization layer, seeing an interest in sculpture and Cham material culture, recommends across categories — a related monument, a craft village, and a performing art connected through the graph — each shown with the path that justifies it. Nothing in the practical block is generated: museum, period, material and position are record fields with sources.

**Scenario B — attending a festival.** A user asks about a fishing-village festival. The answer layer explains its meaning and ritual structure from the corpus with a citation. Intent is classified as attend-event, so the advisory layer returns the calendar type and this year's dates, the venue with its coordinate and map, the ritual and festivity segments, the forecast for that date with a preparation checklist derived by rule from the precipitation probability, a recommended viewpoint, and the nearest parking. The personalization layer recommends related culture — the local cuisine associated with the village, a nearby monument, the folk performance staged during the festivity segment. If the weather service is unreachable, the card states that the forecast is unavailable; it never guesses.

### 12.5. Implementation Baseline

Because this is a revision rather than a proposal for unstarted work, the current measured state is recorded here so that the review panel can distinguish what exists from what is planned, and so that later results can be compared against a stated baseline.

| Component | Measured state |
| --- | --- |
| Corpus | 45 usable documents, 349 passages; 30 Huế / 15 Đà Nẵng; by category — heritage sites 22, cuisine 9, scenic sites 6, performing arts 4, festivals 2, craft villages 2 |
| Knowledge graph | 510 nodes, 1135 edges, 1 connected component, 0 isolated documents, built in 0.23 s. Nodes: 235 entities, 222 years, 45 documents, 6 categories, 2 regions. Edges: 443 year, 242 mentions, 123 related, 98 administrative, 92 region, 92 category, 45 is-about |
| Retrieval | In-domain 68/70; paraphrase 9/39; evidence-in-passage 34/34; ward/commune 18/20; out-of-domain 31/38. Paraphrase is the primary bottleneck |
| Model | 4-bit Qwen2.5-3B-Instruct with a rank-16 LoRA adapter over the last 16 layers; adapter checkpoint selected at iteration 200 on validation loss 0.414 rather than the final iteration 720 at 0.473, because validation loss rose from roughly iteration 250 onward |
| Answer quality | Entity micro-F1 0.786 versus 0.104 for the base model; citation faithfulness 0.704 and coverage 0.741; abstention accuracy 0.917 versus 0.375 for the base model |
| Not yet measured | p95 latency; narration style score; every metric belonging to the three new capability layers |
| Not yet built | Database, authentication, interest profile, recommender, intent classifier, advisory cards, structured records, floor plan, test framework, CI |

Two honesty notes are carried forward into the final report. Base and LoRA were measured under controlled conditions on the same 76 samples, prompt and corpus on 8 September 2026. However, the event entity type has **zero** gold labels, so the four-type entity claim is in practice a three-type result. Entity gold labels are machine pre-filled and pending human review.

## 13. Potential Risks and Mitigation Strategies

| Risk | Type | Impact | Mitigation strategy |
| --- | --- | --- | --- |
| Scope exceeds the remaining 13 weeks | Schedule | **Highest** | Section 16 removes four v1.0 feature groups in exchange; scope delta agreed in writing with the supervisor in Week 2; Section 13.1 defines a fixed cut order |
| Corpus category imbalance limits cross-domain recommendation | Data / AI | High | Corpus expansion to at least 8 documents per category is scheduled in Week 4, before the recommender is built, and is a gate on starting Week 5 |
| Structured event, venue and artifact data must be authored by hand | Data / Schedule | High | Scope capped at 20 events, 50 venues, 35 artifacts, one museum floor plan; every field requires a source; authoring is a whole scheduled week, not an incidental task |
| Advisory cards reintroduce hallucination | AI / Trust | **High** | Architectural rule: cards are rendered from typed records and never generated. Enforced by the automated zero-fabricated-field assertion (NFR06). This is the project's central safety commitment |
| Recommendation quality is unmeasurable with one developer and no users | Evaluation | High | Two-rater relevance judgement with reported agreement; cross-domain rate and diversity are computed objectively without human judgement |
| Cold start — a new user has no profile | AI / UX | Medium | Explicit onboarding (F05); fall back to graph affinity to the current subject alone when no profile exists |
| Point-of-interest coverage in the pilot area is sparse | Data / External | Medium | Verify coverage for the demonstration venues at the start of Week 7; fall back to hand-authored points of interest with sources where coverage is missing |
| Weather or map service unavailable during demonstration | External | Medium | Cache all external responses; cards degrade to an explicit unavailable state; degradation is itself a test case |
| Lunar-to-solar date conversion is wrong by one day | Data | Medium | Hand-author the conversion table for the pilot events across the demonstration period rather than relying on a general lunar library; note the limitation |
| p95 latency exceeds 8 s once cards are added | Performance | High | Measure from Week 3, not Week 12; overlap external calls with generation; cap generated tokens; add response streaming as the remediation if the target is missed |
| Personal data handling becomes a real obligation once interaction is logged | Ethical / Legal | High | Consent before logging; store only what recommendation needs; export and deletion (FR19); privacy review scheduled in Week 14 |
| Unauthenticated endpoints while personal data exists | Security | High | Authentication lands in Week 3, **before** any personal data is stored; no unauthenticated write path; the server does not bind a public interface in the demo configuration |
| Incorrect Vietnamese proper-name extraction | Technical | High | Curated entity list, closed classifier vocabulary, alias dictionary, minimum-mention threshold, compound-name guards, and the constraint that every extracted name is a literal source substring |
| Duplicate or renamed administrative names | Technical | Medium | Alias file; recorded renames; administrative-relation test suite |
| Graph creates relations without evidence | Trust / AI | High | Only structural relations are created — membership, mention, administrative, temporal, co-mention — and no semantic relation is inferred; every node traces to a source span |
| Sensitive cultural content or misattribution | Ethical | High | Source and sentence on every structured field; curator review; explicit scope disclaimer; domain-advisor review of festival and artifact records |
| Prototype mistaken for an authoritative historical source | Communication | Medium | Visible sources and provenance on every claim; explicit scope and status disclaimer in the interface |
| Single developer unavailable through illness | Schedule | High | Week 11 is an explicit buffer; the cut order in Section 13.1 is decided in advance so triage under pressure does not require new judgement |

### 13.1. Fixed Cut Order Under Schedule Pressure

Decided in advance so that triage does not become improvisation. Cut in this order: museum floor-plan hotspots (keep a static plan image); shop and gift points of interest (keep parking and viewpoint); reduce the user study from eight participants to four; replace the admin interface with command-line tools plus a read-only statistics page; reduce the corpus target from 80 documents to 65 while keeping the per-category minimum.

**Never cut, at any level of schedule pressure:** the three refusal gates, mandatory citation, the zero-fabricated-field assertion on cards, and the evaluation suite. These are the project's contribution; without them it is an unverified demonstration.

## 14. Expected Outcomes / Deliverables

### 14.1. Expected Outcomes

A working prototype in which a user's cultural interest — in an artifact, a dish, a performing art, a craft or a festival — is turned into a personalized, explained path through related culture, and in which the practical requirements of actually participating are supplied automatically, while every displayed claim remains traceable to a source.

Technically, the project delivers an end-to-end measurable pipeline from ingestion through deterministic graph construction, hybrid retrieval, domain fine-tuning, citation-validated generation, graph-path recommendation and intent-driven advisory rendering.

Academically, the project contributes three things beyond an application. First, evidence that a deterministic, provenance-preserving knowledge graph is sufficient for graph-augmented retrieval in a low-resource Vietnamese setting, with no LLM extraction and no vector index, at a fraction of the index cost. Second, an explainable cold-start recommender for cross-domain cultural discovery, with cross-domain rate reported as a first-class metric rather than treated as a side effect. Third, a demonstration that proactive advisory capability can be added to a grounded question-answering system **without** measurable regression in trustworthiness, by separating narration from typed data — supported by before-and-after measurement of citation faithfulness and abstention accuracy across the advisory feature's introduction.

### 14.2. Deliverables

| No. | Deliverable | Description | Status |
| --- | --- | --- | --- |
| 1 | Web prototype | HeritageGraph running in the demonstration environment | Partial |
| 2 | Corpus and knowledge graph | At least 80 documents across six categories; deterministic graph with provenance; alias dictionary | Partial |
| 3 | Structured record sets | Venues with coordinates, events with calendar and segments, artifacts with period, material and position — every field sourced | New |
| 4 | Retrieval engine | Hybrid BM25 with reciprocal rank fusion, graph propagation re-ranking, three refusal gates | Built |
| 5 | Fine-tuned model and adapter | Domain adapter with training configuration, data-generation pipeline and checkpoint selection rationale | Built |
| 6 | Question answering with citations and abstention | Vietnamese text-only chat, context assembly, citation validation | Built |
| 7 | Personalization module | Interest profile with decay, graph-path recommender with cross-category bonus and diversity, explanation paths | New |
| 8 | Proactive advisory module | Six-class intent classifier, card generator registry, weather and points-of-interest adapters, rule-based preparation advice | New |
| 9 | Card-based interface | Chat with typed cards, exploration and detail pages, onboarding, map, museum floor plan | New |
| 10 | Admin and curator tools | Content and record management with source validation, review status, audit log, statistics dashboard | New |
| 11 | Evaluation dataset and harness | Question sets for retrieval, entity extraction, citation, abstention, intent and recommendation relevance | Partial |
| 12 | Evaluation report | All metrics of Section 14.3 with error analysis and stated limitations | Partial |
| 13 | Test suite and CI | Unit, integration, API and end-to-end tests including the card-fabrication assertion | New |
| 14 | Technical documentation | Requirements, architecture, API specification, data schema, deployment guide | Partial |
| 15 | Final report and demonstration materials | Report, video, slides, user guide, privacy and ethics review | Planned |

### 14.3. Success Criteria and Metrics

The project succeeds when both demonstration journeys of Section 12.4 complete end to end for an authenticated user with a profile, and the metrics below are measured and reported — whether or not every target is met. A missed target that is measured and explained is an acceptable capstone outcome; an unmeasured target is not.

| Metric | Target | Baseline / current |
| --- | --- | --- |
| Retrieval recall@1, in-domain | ≥ 95% | 68/70 |
| Out-of-domain refusal | ≥ 95% | 31/38 |
| Entity extraction micro-F1 | ≥ 0.75 | 0.786 (labels pending human review) |
| Citation faithfulness | ≥ 85% | 0.704 — improvement expected from corpus expansion |
| Citation coverage of answerable questions | ≥ 90% | 0.741 |
| Abstention accuracy | ≥ 90% | 0.917 |
| Intent classification macro-F1 | ≥ 85% over 100 labelled questions | New |
| Recommendation precision@5 | ≥ 70%, two raters, agreement reported | New |
| Recommendation nDCG@5 | Reported, no target on first measurement | New |
| Cross-domain recommendation rate | ≥ 30% of top-five items in a different category | New |
| Advisory card field correctness | **100% — zero fabricated fields, automatically asserted** | New |
| p95 end-to-end latency | ≤ 8 s | Not yet measured |
| Usability | System Usability Scale on 6–8 participants, reported as formative | New |

### 14.4. Known Limitations to State in the Final Report

Listed here rather than discovered at the defence.

- **Single locality pair.** All results are for Huế and Đà Nẵng. The mentor's own example of a southern performing art is *structurally* supported — nothing in the recommender is region-specific — but is not *demonstrable*, because the corpus contains no southern Vietnamese culture. Section 16.3 records the mapping that shows the mechanism transfers, and regional expansion is future work.
- **Small evaluation scale.** Recommendation relevance and usability rest on tens of judgements, not thousands of users. Reported as formative, with agreement statistics.
- **Machine pre-filled entity labels**, and zero gold labels for the event type — the four-type claim is in practice three types.
- **No vector index**, so purely paraphrastic queries sharing no lexical or graph anchor with the corpus will fail. The refusal gates make this failure safe (the system abstains) but it is still a recall limitation.
- **Deterministic extraction means no semantic relations.** The graph knows that two entities are mentioned together, not that one built the other. Recommendation explanations are therefore structural, not causal.
- **In-memory graph and single-machine model** cap scale; both are architectural choices justified at current size, not general solutions.
- **Hand-authored lunar-date conversion** covers only the pilot events and demonstration period.
- **Point-of-interest data quality** depends on volunteer mapping and is uneven.

## 15. References

[1] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS 2020, arXiv:2005.11401. https://arxiv.org/abs/2005.11401

[2] Microsoft Research, "Project GraphRAG: LLM-Derived Knowledge Graphs." https://www.microsoft.com/en-us/research/project/graphrag/

[3] D. Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization," arXiv:2404.16130. https://arxiv.org/abs/2404.16130

[4] UNESCO, "Digital technologies in the culture sector," MONDIACULT. https://www.unesco.org/en/mondiacult/digital-technologies-culture-sector

[5] Google Arts & Culture, "About the project." https://artsandculture.google.com/

[6] Google Arts & Culture, "Explore collections and stories." https://artsandculture.google.com/explore

[7] E. J. Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models," ICLR 2022, arXiv:2106.09685. https://arxiv.org/abs/2106.09685

[8] S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," Foundations and Trends in Information Retrieval, 2009. https://dl.acm.org/doi/10.1561/1500000019

[9] G. V. Cormack, C. L. A. Clarke and S. Buettcher, "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods," SIGIR 2009. https://dl.acm.org/doi/10.1145/1571941.1572114

[10] J. Carbonell and J. Goldstein, "The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries," SIGIR 1998. https://dl.acm.org/doi/10.1145/290941.291025

[11] Y. Zhang and X. Chen, "Explainable Recommendation: A Survey and New Perspectives," Foundations and Trends in Information Retrieval, 2020, arXiv:1804.11192. https://arxiv.org/abs/1804.11192

[12] Open-Meteo, "Free Weather API Documentation." https://open-meteo.com/en/docs

[13] OpenStreetMap Foundation, "Overpass API Documentation." https://wiki.openstreetmap.org/wiki/Overpass_API

[14] Scrum.org, "The 2020 Scrum Guide." https://scrumguides.org/scrum-guide.html

## 16. Scope Revision Record (v1.0 → v2.0)

Recorded explicitly so the review panel can verify that the four capabilities requested at mentor review were added by **exchange**, not by expansion of an already tight 15-week plan.

### 16.1. Added

| # | Capability requested at mentor review | Where it now lives |
| --- | --- | --- |
| 1 | Personalization per user; cross-domain suggestion inferred from interest | F05, F06, F07; FR06–FR09; NFR07; recommendation metrics in 14.3 |
| 2 | AI as a proactive consultant that infers the unstated practical need | F09; FR12–FR15; NFR06; intent and card metrics in 14.3 |
| 3 | Query and detailed display of cultural events with schedule, venue, organizer and structure | F03, F14; the event and venue record sets in deliverable 3 |
| 4 | Interactive card-based chat replacing plain search | F09, F10; deliverable 9; Scenario A and B in 12.4 |

### 16.2. Removed, With Rationale

| Removed from v1.0 | Rationale |
| --- | --- |
| Image-first gallery and image upload pipeline with thumbnails and per-image metadata | The four requested capabilities are all text-and-structure driven. Retaining an image CRUD pipeline would consume roughly two weeks that the recommender and advisory layers need, while adding nothing to any of them. Cards display a representative image per entity, so the visual entry point survives without the management pipeline |
| Multi-image stories with milestones and camera paths | Superseded in function by the personalized exploration path of F06, which is generated per user rather than authored per story — and is the actual differentiator. Authored linear stories would compete with it for the same interface surface |
| DOCX ingestion | The corpus is encyclopaedic text; no DOCX source is in use. Kept as future work with no loss to any measured objective |
| Separate vector index and embedding model | The implemented hybrid retrieval reaches recall@1 of 30/30 in-domain including accent-free and alias queries. Adding an index with no measured deficit to fix is unjustified at this scale. Recorded as future work and as a stated limitation in 14.4 |
| External LLM/embedding API dependency | Both analysis and generation are local. Eliminates the v1.0 API-cost risk and keeps cultural corpus text on the machine |
| Full admin dashboard as originally specified | Reduced to content and record management with source validation, review status, audit log and a statistics page. Curator function is preserved; presentation scope is not |

Net effect on the 15-week budget: four capability groups added, six scope items removed or reduced, and the highest-risk item — hand authoring of sourced structured records — given a dedicated week rather than being absorbed implicitly.

### 16.3. Note on the Mentor's Example Domain

The example discussed at review used a southern Vietnamese performing art, with suggestions spanning its associated music form, traditional costume, and a historic house — an illustration of interest-driven cross-domain recommendation.

The mechanism this requires is region-independent: propagation over category membership, co-mention and shared administrative or temporal context. Nothing in the recommender is specific to Huế or Đà Nẵng. The corpus, however, contains no southern Vietnamese culture, and expanding to a third region would require re-crawling, re-categorizing, regenerating the evaluation set and re-running every retrieval measurement — several weeks, and it would add no new mechanism.

The pilot region pair is therefore retained, consistent with the single-locality scope rule, and the equivalent structure is demonstrated within it:

| Structural role in the mentor's example | Equivalent in the pilot corpus |
| --- | --- |
| A traditional performing art as the entry point | Royal court music, classical theatre |
| An associated music or instrument form | Related performing-art documents in the same category |
| Associated traditional costume or material culture | Craft-village and artifact records |
| A historic house or monument to visit | Monument and heritage-site documents in the same administrative unit |
| A place where the art is performed | Venue records with coordinates, and festival events whose festivity segment includes the performance |

Regional expansion is listed as the first item of future work, and the limitation is stated explicitly in Section 14.4 rather than left for the panel to discover.

## Submission Checklist

| Checklist item | Status |
| --- | --- |
| Project name, team member and student ID completed | ☑ |
| Supervisor and department completed; email addresses to be filled | ☐ |
| Pilot locality/theme selected — Huế and Đà Nẵng, six categories | ☑ |
| Source usage rights and attribution approach confirmed | ☐ |
| Database, model and retrieval technology finalized — PostgreSQL, local Qwen2.5-3B with LoRA, hybrid BM25 with graph re-ranking, no vector database | ☑ |
| Sample corpus and evaluation question set created — 45 documents, 349 passages, 76 gold samples; expansion to 80 documents scheduled Week 4 | ☑ partial |
| System context diagram updated to 12 request/response pairs with the External AI/LLM entity removed | ☑ |
| 3D confirmed as future work, not a required MVP item | ☑ |
| Objectives and acceptance criteria reviewed against measured baseline | ☑ |
| **v2.0 scope delta agreed in writing with the supervisor (Section 16)** | ☐ **— Week 2 blocking item** |
| Privacy and consent approach for interaction logging reviewed | ☐ |
| Final formatting checked before submission | ☐ |
