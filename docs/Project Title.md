**International School**

**CAPSTONE PROJECT 1**

CMU-SE 450

**PROJECT DOCUMENT**

**Date: August 21, 2026**

**An AI-Powered Platform for Preserving and Storytelling Local Cultural Memories Using GraphRAG**

**Submitted by: C1SE.50**

Hung , Duong Thanh – 29219043370

**Approved by:**

**Msc. Nguyen Thi Thanh Tam**

**Proposal Review Panel Representative:**

Name:SignatureDate

**Capstone**** Project 1- Mentor:**

Name: **Msc.Nguyen Thi Thanh Tam**SignatureDate

**Da Nang 8,2026**

**PROJECT INFORMATION**

| Project title | AI-Powered Platform for Preserving and Storytelling Local Cultural Memories Using GraphRAG |
| --- | --- |
| Project acronym | CulturalMemoryGraph / CMG |
| Project duration | 27/08/2026 – 06/12/2026 |
| Institution | [School / Faculty / Program name] |
| Pilot locality / topic | [Selected local area or cultural theme] |
| Project status | Capstone project proposal |

**Note: ***Fields in square brackets must be updated with official information before submission.*

## 1. Project Title

**An AI-Powered Platform for Preserving and Storytelling Local Cultural Memories Using GraphRAG**

The project title reflects the system's true direction. “AI-powered” emphasizes that artificial intelligence supports digitization, organization, retrieval, and delivery of knowledge, rather than replacing experts or the communities who own the culture. “Storytelling local cultural memories” describes the goal of turning images, documents, people, places, and events into an accessible experience. “GraphRAG” refers to the core technology used to combine retrieval-augmented generation with a knowledge graph.

The proposed short name is CulturalMemoryGraph, or the shorter product name HeritageGraph.

## 2. Team Members

| Full name | Student ID | Role | Email |
| --- | --- | --- | --- |
| [Full name 1] | [Student ID] | Project Leader / Full-stack Developer | [Email] |
| [Full name 2] | [Student ID] | AI and GraphRAG Developer | [Email] |
| [Full name 3] | [Student ID] | Data and Knowledge Engineer | [Email] |
| [Full name 4] | [Student ID] | UI/UX and Frontend Developer | [Email] |
| [Full name 5] | [Student ID] | QA and Documentation | [Email] |

If the project has only one member, the roles above may be merged. In that case, the student is responsible for requirements analysis, development, testing, data management, and documentation, while the supervisor provides direction, feedback, and progress review.

## 3. Supervisor(s)

| Full name | Title / Department | Role | Email |
| --- | --- | --- | --- |
| [Degree, supervisor full name] | [Faculty / Department] | Project Supervisor | [Email] |
| [Degree, co-supervisor full name, if any] | [Faculty / Department] | Co-supervisor / Domain Advisor | [Email] |

The supervisor helps the team define scope, choose a development approach, review the architecture, assess data quality, monitor progress, and critique results. For cultural content, the team should also consult someone with local knowledge, such as a librarian, museum staff member, cultural center representative, history teacher, or community representative.

## 4. Problem Statement

### 4.1. Background

Local cultural materials such as traditional craft villages, folk songs, festivals, artisans, monuments, place names, and history are often already recorded in local gazetteers, festival yearbooks, articles, archival records, collected notes, or personal photo collections. However, these sources are usually scattered across many files and repositories. They may differ in format, spelling of proper names, level of detail, time coverage, and reliability.

Many current digital collections display images as isolated files. A user may see a photo of a festival, an artisan, or a location, but has no way of knowing where the photo was taken, when, who appears in it, what the event means, or which document explains it. Conversely, text documents are often long and dry, forcing younger readers to manually piece together the relationships between people, places, events, and time across many sources.

### 4.2. Core Problem

The project addresses the problem of **the lack of a platform capable of linking images and textual materials about local culture into contextual, explorable, and verifiable stori****es**.

General-purpose chatbots do not solve this problem either. Without being provided a specific local dataset, a chatbot may confuse place names, infer from general knowledge, or generate information that does not appear in the source material. Research on Retrieval-Augmented Generation shows that combining a language model with external memory can support knowledge-intensive question-answering tasks and provide a retrieval basis [1]. GraphRAG extends this direction by combining text extraction, network analysis, and LLM prompting/summarization [2].

### 4.3. Importance of the Problem

This problem matters because digitizing culture is not just about storing files. There must be a way for users to access, understand, and verify knowledge conveniently. UNESCO notes that digital technology can expand access to culture and support documentation, protection, promotion, and inventory of heritage [4]. A system capable of linking images, text, and knowledge relationships can support education, research, cultural communication, and community engagement.

### 4.4. Proposed Problem Response

The project proposes building an image-first platform. Images serve as the entry point for user exploration; metadata and the knowledge graph provide context; GraphRAG supports retrieval and answering; citations allow users to verify information. In the MVP, the system focuses on one specific locality or theme to keep the data controllable and measurable.

## 5. Survey / Existing Solutions

### 5.1. Retrieval-Augmented Generation and GraphRAG

RAG combines a language model with a non-parametric memory retrieved from an external source. Lewis et al. present the use of a dense vector index to retrieve relevant passages for knowledge-intensive question-answering and language generation tasks [1]. This is a suitable foundation for question-answering over a private cultural corpus.

GraphRAG is a development direction that combines graphs with RAG. Microsoft Research describes GraphRAG as a technique that combines text extraction, network analysis, and LLM prompting/summarization to deeply understand text datasets [2]. In this project, the knowledge graph represents relationships among people, places, events, time, traditional crafts, images, documents, and source passages.

### 5.2. Comparable Digital Storytelling Platforms

Google Arts & Culture is a platform close to HeritageGraph in its goal of making cultural heritage more accessible through digitized collections, curated online exhibits, and place-based stories from museums and archives worldwide [5]. It aggregates high-resolution images and narrative exhibits, letting users browse collections by theme, artist, or period and read curated stories built around selected artworks or artifacts [6].

HeritageGraph shares a similar experience layer with Google Arts & Culture: both aim to bring users closer to heritage by pairing images with narrative context. The key difference is depth of question-answering. Google Arts & Culture is built around browsing curated exhibits; it does not provide a knowledge graph of entities and relationships, nor a chatbot that answers open-ended questions with citations to a specific local corpus. HeritageGraph's MVP is built specifically around a knowledge graph, GraphRAG retrieval, and citation-backed Vietnamese question-answering for one local dataset, which is not the focus of general aggregator platforms.

### 5.3. Comparison with Existing Approaches

| Criterion | Static photo album / website | General-purpose LLM chatbot | Google Arts & Culture | HeritageGraph MVP |
| --- | --- | --- | --- | --- |
| Primary data | Scattered images and captions | Knowledge inside the model | Curated museum/archive exhibits | Images, TXT, DOCX, and metadata |
| Person–place–event links | Usually limited | Not reliable | Curated by exhibit editors | Knowledge graph with relations and provenance |
| Storytelling | Static page or album | Free-form conversation | Curated online exhibits | Image story, timeline, hotspots, and chatbot |
| Q&A on local data | Limited or none | Not guaranteed | Not a core feature | GraphRAG over a private corpus |
| Passage-level citation | Usually absent | Not guaranteed | Exhibit-level credit only | A core requirement |
| 3D / digital twin | None | None | Limited (select partners) | Future work, not required in the MVP |
| Feasibility as a capstone | High but low interactivity | High but hard to control sources | Requires large partner network | Fits the MVP timeline and resources |

### 5.4. Project Differentiation

HeritageGraph does not claim to replace professional heritage preservation systems or large aggregator platforms. Its differentiator is a focus on the gap between image collections, text archives, and a verifiable question-answering experience. Images provide a visual entry point; the graph links information; GraphRAG supports multi-step questions; citations let users verify information.

## 6. Objectives and Scope

### 6.1. General Objective

Build and evaluate a web-based AI prototype capable of organizing local cultural images and text materials, linking them through a knowledge graph, generating interactive image stories, and answering Vietnamese-language questions using GraphRAG with source citations.

### 6.2. Specific Objectives

- Build a pilot corpus of at least 30 images and 30 text documents or passages for one specific locality or cultural theme.

- Allow administrators to upload JPG, PNG, or WebP images with metadata such as title, description, location, time, source, author, and usage license.

- Allow TXT or DOCX upload, or direct text entry; normalize and split documents into passages with source locators.

- Extract entity groups covering people, places, events, time, and traditional crafts, with evidence spans and confidence scores.

- Build a knowledge graph linking images, documents, passages, and related entities.

- Implement vector search and graph retrieval, then combine both context sources in a GraphRAG pipeline.

- Build an image gallery, image stories, milestones, annotated hotspots, and related entities.

- Provide a Vietnamese-language, text-only chatbot with citations and an abstention mechanism when evidence is insufficient.

- Evaluate the system on correctness, citation precision, citation coverage, hallucination rate, latency, and story clarity.

### 6.3. In Scope

The MVP scope covers one specific locality or cultural theme; image and metadata management by administrators/curators; TXT/DOCX ingestion; entity and relation extraction; a vector database; a knowledge graph; text-only GraphRAG Q&A; an image gallery; image stories; basic hotspots; citations; admin review; testing; and an evaluation report. End users do not upload images through the chatbot interface.

### 6.4. Out of Scope

The MVP does not include 3D modeling, LiDAR scanning, photogrammetry, digital twins, virtual tours, professional GIS mapping, video recognition, large-scale OCR for scanned documents, multilingual translation, commercialization, or official historical certification of content.

3D is noted as future work. Once the MVP proves the quality of metadata, image stories, the knowledge graph, GraphRAG, and citations, the system can be extended to link 3D models with existing nodes and stories.

## 7. Key Features & Requirements

### 7.1. Core Features

Each feature is one request/response pair, matching exactly the system context diagram in Section 12.2. Admin features (F01–F04) and User features (F05–F08) each send a request to the System and receive a corresponding response back. The System, in turn, exchanges two request/response pairs with the External AI/LLM Service (F09–F10). AI is embedded directly in the User-facing features rather than treated as a hidden backend step — recommendations, search ranking, and chatbot answers are explicitly AI-driven and personalized to the user's selected topic and interest profile, not simple keyword matching.

| Code | Feature | Description |
| --- | --- | --- |
| F01 | Login Request | Admin logs in; the System returns a Login Response confirming authentication |
| F02 | Manage Cultural Content Request | Admin performs CRUD on images, documents, and metadata; the System returns the CRUD Result |
| F03 | Create And Edit Story | Admin creates or edits an image story from uploaded images and documents; the System returns Story Validation / Publication Status |
| F04 | Manager Dashboard Request | Admin requests the admin dashboard; the System returns Dashboard Overview Data (content status, activity) |
| F05 | Topic/Location Selection Request | User selects a cultural topic or location; the System returns an AI-Personalized Recommendation List |
| F06 | Interest-Based Semantic Search Query | User searches by keyword and personal interest; the System returns Ranked Personalized Search Results |
| F07 | Story Detail Request | User requests to view a specific story; the System returns Story Content (Milestones, Hotspots, Citations) |
| F08 | Natural Language Query (Text) | User submits a free-text cultural question; the System returns an AI-Generated Answer with Source Citations |
| F09 | Content Analysis Request | The System sends uploaded document text to the External AI/LLM Service for reading; the AI/LLM Service returns Extracted Information (Entities & Relations) used to build the knowledge graph |
| F10 | Answer Generation Request | The System sends retrieved context plus the user's interest profile to the External AI/LLM Service; the AI/LLM Service returns a Generated Personalized Answer |

F09 and F10 do not run on a direct user click; they are triggered indirectly. F09 runs whenever an admin uploads a new document (feeding F02), and F10 runs every time a user submits F08. Four of the eight Admin/User features depend on the knowledge graph that F09 builds: F05, F06, F07, and F08 would return empty or insufficient results if no document had been analyzed yet.

### 7.2. Functional Requirements

| Code | Functional Requirement | Acceptance Criteria |
| --- | --- | --- |
| FR01 | Admin can upload a valid image | The image is stored, a thumbnail is generated, and it displays correctly |
| FR02 | Admin can enter image metadata | Metadata is saved and displayed on the detail page |
| FR03 | User can filter the gallery by entity or metadata | Results match the applied filter |
| FR04 | Admin can create a story from multiple images | The story has an ordered sequence of valid milestones and content |
| FR05 | User can click a hotspot to view an annotation | The hotspot displays the entity, description, and related links |
| FR06 | The system can read TXT, DOCX, or pasted text | Content is converted into passages with source locators |
| FR07 | The system can extract entities and relations | Output matches the schema and stores evidence spans |
| FR08 | The system can build or update the knowledge graph | Nodes/edges are created and linked to their sources |
| FR09 | User can search by keyword or semantic meaning | The system returns relevant images, passages, or entities |
| FR10 | User can submit a text-only question in Vietnamese | The chatbot only processes text input and answers based on retrieved context |
| FR11 | Answers must include citations or state insufficient evidence | The system does not produce assertive answers without supporting sources |
| FR12 | The chatbot does not provide an image upload feature for end users | The chatbot UI only shows a text input field |
| FR13 | Admin can confirm or correct extraction results | Status changes are recorded in the audit log |
| FR14 | The system can run the evaluation suite | Metrics are saved and exported as a report |

### 7.3. Non-functional Requirements

| Code | Group | Requirement |
| --- | --- | --- |
| NFR01 | Performance | p95 latency for a standard question does not exceed 8 seconds in the demo environment |
| NFR02 | Performance | The first image story loads within 3 seconds using optimized thumbnails |
| NFR03 | Accuracy | Target correctness of at least 80% on the evaluation question set |
| NFR04 | Trustworthiness | Target citation precision of at least 85% and citation coverage of at least 90% |
| NFR05 | Safety | Target hallucination rate of no more than 10% on the evaluation question set |
| NFR06 | Usability | A new user can view a story and ask a question without lengthy instructions |
| NFR07 | Accessibility | Images have alt text; the UI has clear contrast, headings, and basic navigation |
| NFR08 | Security | File type/size limits, input validation, and no execution of uploaded files |
| NFR09 | Privacy | Images or documents are not published without an appropriate usage-rights status |
| NFR10 | Maintainability | Ingestion, extraction, graph, retrieval, generation, and UI modules have separate interfaces |
| NFR11 | Reproducibility | Model, prompt, schema, corpus version, and evaluation configuration are recorded |
| NFR12 | Scalability | New localities, themes, or data types can be added without rewriting the whole system |

## 8. Constraints and Assumptions

### 8.1. Constraints

| Constraint group | Description |
| --- | --- |
| Time | The project runs for about 15 weeks, so it cannot cover many localities or data types |
| Data | The corpus may be small, missing metadata, inconsistent, or contain conflicting versions of information |
| Language | Vietnamese proper names, local terms, aliases, and spelling are often inconsistent |
| Technology | GraphRAG quality depends on the model, embeddings, retrieval capability, and server configuration |
| Cost | LLM/embedding APIs, storage, and hosting may incur costs |

### 8.2. Assumptions

- The team can collect or obtain permission to use at least 30 images and 30 text documents for one specific locality or theme.

- Image and document sources have identifiable usage rights or a minimum license note.

- The demo infrastructure has enough resources to run embedding, vector database, knowledge graph, and LLM services at small scale.

- End users have a web browser and network connection in the demo environment; they only need to type a text question in the chatbot and do not need to upload images.

- The MVP goal is to demonstrate pipeline feasibility, not to deploy as a national-scale archival system.

- Images in the MVP are managed through metadata and annotation; the system does not yet need to automatically recognize all image content.

- AI outputs should be treated as suggestions that may be incorrect until confirmed by a curator or expert.

## 9. Target Users / Stakeholders

| Group | Needs | How the system helps |
| --- | --- | --- |
| Students and young people | Want to learn about culture quickly, visually, and interactively | Image gallery, image stories, hotspots, chatbot, and sourced answers |
| Teachers | Need visual content for lessons or extracurricular activities | Themed stories, timelines, contextual images, and references |
| Libraries, museums, cultural centers | Want to showcase local collections and materials | Manage images, documents, metadata, graph, and verification status |
| Researchers | Need to find relationships, cross-check sources, and spot gaps | Knowledge graph, passage retrieval, aliases, and citations |
| Artisans and local communities | Want their knowledge recorded accurately and passed on appropriately | Provenance, usage rights, verification mechanism, and sensitive-content warnings |
| Development team | Need a testable AI and software engineering problem | Modular design, APIs, test sets, metrics, and CI |
| Supervisor / review panel | Need to assess feasibility, quality, and contribution of the capstone | SRS, architecture, demo, test report, and quantitative results |

## 10. Technology Stack

| Component | Proposed technology | Purpose |
| --- | --- | --- |
| Frontend | React or Next.js, TypeScript, Tailwind CSS | Gallery, story, hotspot, chatbot, and admin interface |
| Backend | Python, FastAPI, Pydantic | REST API, ingestion, query orchestration, and evaluation |
| Image processing | Pillow, basic OpenCV | Validate images, resize, thumbnail, and metadata |
| Document parsing | python-docx, Unicode normalization | Read documents and generate passages |
| NLP / LLM | LLM with structured output, or Vietnamese NLP | Entity/relation extraction and answer generation |
| Embedding | Embedding model supporting Vietnamese or multilingual text | Generate vectors for passages and queries |
| Vector database | Qdrant or PostgreSQL with pgvector | Semantic search and metadata filtering |
| Knowledge graph | Neo4j or an equivalent graph store | Entities, relations, aliases, and provenance |
| Relational database | PostgreSQL | Users, document status, stories, evaluation, and audit log |
| File storage | Local object storage or S3-compatible storage | Images, thumbnails, and document files |
| Testing | pytest, Playwright, API test framework | Unit, integration, API, and UI testing |
| DevOps | Git, GitHub, GitHub Actions, Docker | Version control, CI, and reproducible environments |
| Documentation | Markdown, Mermaid, OpenAPI | Requirements, architecture, API, and reports |
| Deployment | Local server or cloud demo | Prototype demonstration and user testing |

The final choice between Neo4j and PostgreSQL/pgvector, as well as between candidate LLM/embedding models, will be finalized after the data trial phase. The application architecture must include an abstraction layer so providers or models can be swapped without affecting the entire codebase.

## 11. Methodology & Development Plan

### 11.1. Development Methodology

The project uses Agile/Scrum with short sprints. This approach fits because the quality of extraction, retrieval, stories, and the chatbot can only be accurately assessed after running on real data. Each sprint includes planning, development, testing, a demo with the supervisor, and a retrospective.

High-risk tasks are prioritized early, including checking image usage rights, designing metadata, Vietnamese-language extraction, entity resolution, provenance, and citations. The team does not wait until the end of the term to test GraphRAG; a baseline vector search and a minimal graph query must be implemented before the UI is finalized.

### 11.2. Development Plan

| Phase | Duration | Main content | Output |
| --- | --- | --- | --- |
| Initiation | Weeks 1–2 | Problem analysis, source survey, choosing the locality/theme, requirements, and schema | SRS, sample corpus, data dictionary, wireframe |
| Sprint 1 | Weeks 3–5 | Image upload, metadata, gallery, image story, and document ingestion | Basic image story and document pipeline |
| Sprint 2 | Weeks 6–8 | Extraction, evidence, aliases, vector index, and knowledge graph | Independent graph and retrieval |
| Sprint 3 | Weeks 9–11 | GraphRAG, chatbot, citation panel, hotspots, and related entities | End-to-end demo flow |
| Testing | Weeks 12–13 | Integration, scenario, performance, correctness, and hallucination evaluation | Test report and initial metrics |
| Closing | Weeks 14–15 | Tuning, ethics/privacy review, documentation, demo video, and presentation | Final accepted version and report |

### 11.3. Quality and Version Control

Source code is managed with Git. Any major change to the schema, prompts, model, corpus, or database must be recorded in a changelog. Pull requests or code review are used for critical modules. CI runs linting, unit tests, and basic checks before merging.

For cultural content, the team must record source locators, license notes, and verification status. For AI components, the team must record model version, prompt version, retrieval parameters, and evaluation set version. This information must be logged so results remain reproducible and explainable.

## 12. System Architecture Overview

### 12.1. Architecture Description

The system architecture has six layers. The presentation layer provides the image gallery, image story, chatbot, citation panel, and admin review. The application/API layer handles upload, story, search, Q&A, and evaluation. The ingestion layer reads images, TXT, DOCX, and metadata. The knowledge-processing layer performs chunking, embedding, entity/relation extraction, and entity linking. The storage layer holds images, passages, vectors, the graph, and the audit log. The AI orchestration layer coordinates query handling, graph traversal, context assembly, answer generation, and citation validation.

In the MVP, images do not necessarily need to be analyzed automatically using advanced computer vision. Images are managed by administrators or curators based on confirmed metadata, descriptions, captions, or annotations. The chatbot does not accept image uploads from end users; it only queries images and metadata already present in the system. This reduces complexity and keeps the focus on the core goal of linking images with cultural knowledge and source documents.

### 12.2. System Context Diagram

*Figure 1. System Context Diagram (Level 0)*

The context diagram shows HeritageGraph as a single process exchanging data with three external entities: Admin, User, and the External AI/LLM Service. Internal components such as the relational database, vector database, and knowledge graph are intentionally not shown at this level, since they sit inside the system boundary; they appear only in the Level 1 decomposition. Every request flow has a matching response flow, forming 10 request/response pairs in total (Section 7.1, F01–F10).

Admin sends a Login Request, a Manage Cultural Content Request, a Create And Edit Story request, and a Manager Dashboard Request, receiving back a Login Response, a CRUD Result, Story Validation / Publication Status, and Dashboard Overview Data. User sends a Topic/Location Selection Request, an Interest-Based Semantic Search Query, a Story Detail Request, and a Natural Language Query (Text), receiving back an AI-Personalized Recommendation List, Ranked Personalized Search Results, Story Content (Milestones, Hotspots, Citations), and an AI-Generated Answer with Source Citations. The System also exchanges two request/response pairs with the External AI/LLM Service: a Content Analysis Request answered with Extracted Information (Entities & Relations), and an Answer Generation Request answered with a Generated Personalized Answer.

This is what makes personalization explicit rather than implicit: the user's topic selection and interest profile flow all the way through to the external AI service as part of the Answer Generation Request, so recommendations, search ranking, and chatbot answers are tailored per user instead of being identical for everyone.

### 12.3. Main Processing Flow

When an admin uploads an image, the system validates the format, generates a thumbnail, stores metadata, and allows the image to be linked to an entity or story. When an admin uploads a document, the system parses the content, splits it into passages, generates embeddings, and extracts entities/relations. Entities and relations are stored together with evidence spans to trace back to the original document.

When a user submits a text question, the query orchestrator identifies keywords and entities, performs a vector search to retrieve semantically close passages, and simultaneously expands the knowledge graph to retrieve related nodes/edges. The combined context is passed to the answer generator. The answer is checked for citations before being displayed. If no suitable passage or relation is found, the system states that the current data does not provide sufficient evidence.

### 12.4. Example User Scenario

A user selects an image story about a local festival. The story begins with an image of the venue, continues with images of the rituals, artisans, or community practitioners, and ends with an image of the activity today. The user taps a hotspot on an image to view information about a person or artifact.

The user then types a text question: “Where did this festival originate and who keeps it alive today?” The system retrieves passages discussing its origin, expands the graph to related entities, and generates an answer in Vietnamese. The answer displays citations to the documents and excerpts used. If the sources only describe current activity without mentioning origin, the system must state that clearly instead of guessing.

## 13. Potential Risks and Mitigation Strategies

| Risk | Type | Impact | Mitigation strategy |
| --- | --- | --- | --- |
| Not enough suitable images or documents | Data / Schedule | High | Lock the sample corpus in weeks 1–2, limit to one locality/theme, prepare backup sources |
| Unclear image usage rights | Legal / Ethical | High | Record license notes, prioritize permitted sources, do not publish unverified data |
| Missing or incorrect image metadata | Technical / Data | High | Require minimum fields, allow an unknown status, use admin review |
| Incorrect Vietnamese proper-name extraction | Technical | High | Alias dictionary, structured output, evidence spans, human validation |
| Duplicate entity names or place names | Technical | Medium | Use context, time/place attributes, and a candidate status |
| Images linked incorrectly to documents | Technical | High | Reviewed linking, confidence scores, source panel, and test data |
| Graph creates relations without evidence | Trust / AI | High | Require evidence, verification status, and citation validation |
| Chatbot hallucination | AI / Trust | High | Context-only prompting, abstention, unanswerable test questions, dedicated evaluation |
| Vector search misses multi-step questions | AI | High | Graph expansion, query decomposition, comparison with a vector-only baseline |
| High latency | Performance | High | Caching, thumbnails, limited top-k, async ingestion, per-stage timing |
| API cost exceeds budget | Resource | Medium | Caching, batching, appropriate model choice, request limits, abstraction layer |
| Sensitive cultural content | Ethical | High | Community consultation, access control, and clearly stated usage scope |
| Poor mobile usability | UX | Medium | Responsive design, task testing, and iteration based on feedback |
| Scope exceeds the 15-week timeline | Schedule | High | Lock the image-first MVP; move 3D, GIS, and multimedia to future work |
| Prototype mistaken for an official historical source | Communication | Medium | Display sources, confidence, verification status, and scope disclaimers |

## 14. Expected Outcomes / Deliverables

### 14.1. Expected Outcomes

The project is expected to produce a prototype demonstrating that local cultural images and text materials can be linked into a structured exploration experience. Users can start from an image, follow related entities, read stories by milestone, and ask Vietnamese-language questions with citations.

Technically, the project is expected to deliver a measurable pipeline covering ingestion, metadata, extraction, vector retrieval, graph retrieval, GraphRAG generation, and citation validation. Academically, the project provides comparative results between baseline vector search and combined graph-augmented retrieval, along with error analysis across data, extraction, retrieval, generation, and UI issues.

### 14.2. Deliverables

| No. | Deliverable | Description |
| --- | --- | --- |
| 1 | Web prototype | The HeritageGraph web application running in the demo environment |
| 2 | Image management module | Admin image upload, thumbnail generation, metadata management, gallery, and source notes |
| 3 | Image story module | Milestones, hotspots, related entities, and story navigation |
| 4 | Document ingestion module | TXT, DOCX, pasted text, parsing, chunking, and source locators |
| 5 | Knowledge graph | Schema, nodes, relations, aliases, provenance, and verification status |
| 6 | Vector index | Embeddings, metadata filtering, and semantic search |
| 7 | GraphRAG Q&A | Vietnamese chatbot, context assembly, citations, and abstention |
| 8 | Admin review | Editing entities, relations, aliases, metadata, and verification status |
| 9 | Evaluation dataset | Questions, reference evidence/answers, and test scenarios |
| 10 | Evaluation report | Correctness, citation precision, hallucination rate, latency, and error analysis |
| 11 | Technical documents | SRS, architecture document, API documentation, data schema, deployment guide |
| 12 | Testing documents | Test plan, test cases, test report, and defect log |
| 13 | Final report | Project report, limitations, results, and future directions |
| 14 | Demonstration materials | Demo video, presentation slides, and user guide |

### 14.3. Success Criteria

The project is considered successful when a user can complete the end-to-end flow: an admin uploads images and documents; the system generates metadata, passages, entities, relations, vectors, and graph data; the user opens an image story; the user submits a Vietnamese-language text question; the system answers with citations or states that evidence is insufficient. End users must not, and cannot, upload images through the chatbot.

Initial quantitative targets include correctness of at least 80%, citation precision of at least 85%, citation coverage of at least 90%, a hallucination rate of no more than 10%, p95 latency of no more than 8 seconds, and a first image-story load time of no more than 3 seconds in the demo environment. These are prototype evaluation targets on a defined corpus, not quality commitments for large-scale deployment.

## 15. References

[1] P. Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” NeurIPS 2020, arXiv:2005.11401. https://arxiv.org/abs/2005.11401

[2] Microsoft Research, “Project GraphRAG: LLM-Derived Knowledge Graphs.” https://www.microsoft.com/en-us/research/project/graphrag/

[3] D. Edge et al., “From Local to Global: A Graph RAG Approach to Query-Focused Summarization,” arXiv:2404.16130. https://arxiv.org/abs/2404.16130

[4] UNESCO, “Digital technologies in the culture sector,” MONDIACULT. https://www.unesco.org/en/mondiacult/digital-technologies-culture-sector

[5] Google Arts & Culture, “About the project.” https://artsandculture.google.com/

[6] Google Arts & Culture, “Explore collections and stories.” https://artsandculture.google.com/explore

[7] Neo4j, “Neo4j Documentation.” https://neo4j.com/docs/

[8] Qdrant, “Qdrant Documentation.” https://qdrant.tech/documentation/

[9] Scrum.org, “The 2020 Scrum Guide.” https://scrumguides.org/scrum-guide.html

## Submission Checklist

| Checklist item | Status |
| --- | --- |
| Project name, team members, and student IDs completed | ☐ |
| Supervisor, department, and email completed | ☐ |
| Pilot locality/theme selected | ☐ |
| Image and document usage rights confirmed | ☐ |
| Database, embedding, and LLM technology finalized | ☐ |
| Sample corpus and evaluation question set created | ☐ |
| System context diagram reviewed and corrected | ☑ |
| 3D confirmed as future work, not a required MVP item | ☑ |
| Objectives and acceptance criteria reviewed | ☐ |
| Final formatting checked before submission | ☐ |
