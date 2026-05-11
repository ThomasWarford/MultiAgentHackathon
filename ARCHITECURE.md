### 1. System Workflow & Data Flow Diagram

The multi-agent research matchmaking workflow executes as a deterministic, linear Directed Acyclic Graph (DAG) managed via LangGraph. The pipeline ingests publication corpora and explicit researcher focus prompts, extracts cross-disciplinary connection points, generates collaborative hypotheses, executes an independent asynchronous critique/refinement loop, and ranks the final output.

```
===================================================================================================
                                      INGESTION LAYER
===================================================================================================
  [Raw PDF Corpus] ---> utils/pdf_to_markdown.py ---> [Markdown Corpus: papers/<id>/*.md]
                                                               |
                                                   LocalCorpusSource.fetch()
                                                               |
                                                               v
  [prompts_input/<id>.md] ---> parse_prompt_markdown() ---> ResearcherProfile (Stage 1)
                                                               |
===================================================================================================
                                    CONTEXT & STATE LAYER
===================================================================================================
                                                               |
    +----------------------------------------------------------+------------------------------+
    |                                                                                         |
    v                                                                                         v
Researcher A State                                                                    Researcher B State
    |                                                                                         |
    +---> ResearcherBackgroundAgent (Stage 2) ---> ResearcherBackground                       |
    |                                                     |                                   |
    +---> DimensionalExtractor (Stage 3 fan-out)          |                                   |
            |---> Methods Summary <-----------------------+                                   |
            |---> Open Questions Summary <----------------+                                   |
            |---> Stakes Summary <------------------------+                                   |
                                                                                              |
===================================================================================================
                                       SYNTHESIS LAYER
===================================================================================================
    |                                                                                         |
    +---------------------------------+-------------------------------------------------------+
                                      |
                                      v
                        CrossFactorialAgent (Stage 4)
             Executes 3x3 parallel LLM evaluations across all dimensions
                                      |
                                      v
                             CrossFactorialMatrix
                                      |
                                      +<--- load_researcher_prompt() (Stage 5)
                                      |
                                      v
                         HypothesesAgent (Stage 6)
          Synthesizes backgrounds, matrix cells, and prompts into candidate hypotheses
                                      |
                                      v
                              list[Hypothesis]
                                      |
===================================================================================================
                               REFINEMENT & EVALUATION LAYER
===================================================================================================
                                      |
                                      v
                        make_refine_loop_node() (Stage 7)
           Per-hypothesis bounded asynchronous while loop (early-exit on 'accept')
                                      |
           +--------------------------+--------------------------+
           |                                                     |
           v                                                     v
   ReviewerProtocol.review()                             RefinerProtocol.refine()
 (Generates severity: block/suggest/accept)             (Applies critique, updates notes)
           |                                                     |
           +--------------------------+--------------------------+
                                      |
                                      v
                           list[RefinedHypothesis]
                                      |
                                      v
                          RankerProtocol.rank() (Stage 8)
              Scores items on composite rigor, novelty, and feasibility
                                      |
===================================================================================================
                              OUTPUT & CONSOLIDATION LAYER
===================================================================================================
                                      |
                                      v
                       write_artifact() & render_final_report()
            Emits per-stage JSON payloads and consolidated Markdown summary

```

---

### 2. Codebase Structure, Classes, and Key Functions

#### Orchestration, Configuration & Entrypoint

* **Full File Path:** `src/matchmaker/config.py`
* **Core Classes:**
* `Settings`: Inherits from `BaseSettings` (Pydantic). Defines the immutable system-wide configurations loaded at startup. Manages external API keys (`anthropic_api_key`, `denario_api_key`), target LLM model bindings (`model_background`, `model_extraction`, `model_cross_factorial`, `model_hypotheses`, `model_refinement`, `model_ranking`), budget breakers (`cost_ceiling_usd`), refinement loop bounds (`max_iterations`), and target filesystem directories.


* **Key Functions:**
* `load_settings() -> Settings`: Initializes and returns the validated application settings instance.




* **Full File Path:** `src/matchmaker/cli.py`
* **Core Classes:** None. Uses Typer for CLI interface routing.
* **Key Functions:**
* `run(...)`: Synchronous CLI wrapper that parses input arguments (`--a`, `--b`, `--backend`) and triggers the async pipeline execution.
* `_run_async(...)`: Orchestrates the runtime environment. Instantiates the `LocalCorpusSource`, the shared `AnthropicClient`, and the requested `RefinementStack`. Initializes the immutable `GraphContext` and invokes the LangGraph instance via `graph.ainvoke(...)`. Finally, triggers `_write_all_artifacts(...)` and renders the final Markdown report via `render_final_report(...)`.
* `_write_all_artifacts(outputs_dir: Path, run_id: str, state: PipelineState) -> None`: Serializes all internal stage attributes from the terminal `PipelineState` into discrete disk-persisted JSON artifacts.




* **Full File Path:** `src/matchmaker/orchestrator/graph.py`
* **Core Classes:**
* `GraphContext`: Immutable dataclass carrying dependencies that every node closes over. Holds references to `settings`, `llm`, `source`, `stack`, input target slugs (`researcher_a_id`, `researcher_b_id`), and input directories.


* **Key Functions:**
* `build_graph(ctx: GraphContext) -> CompiledGraph`: Wires the LangGraph state execution pipeline. Instantiates a `StateGraph(PipelineState)` and maps the linear sequence of nodes: `ingest` $\rightarrow$ `background` $\rightarrow$ `extract_dimensions` $\rightarrow$ `cross_factorial` $\rightarrow$ `load_prompts` $\rightarrow$ `hypotheses` $\rightarrow$ `refine_loop` $\rightarrow$ `rank`. Returns the compiled execution graph.




* **Full File Path:** `src/matchmaker/orchestrator/nodes.py`
* **Core Classes:** None. Exposes async coroutine builders that act as LangGraph state transition handlers.
* **Key Functions:**
* `make_ingest_node(ctx: GraphContext)`: Returns a coroutine that concurrently fetches full `ResearcherProfile` objects via `ctx.source.fetch(...)` for both target researchers.
* `make_background_node(ctx: GraphContext)`: Concurrently triggers the `ResearcherBackgroundAgent` to generate narrative background distillations for both researchers.
* `make_extraction_node(ctx: GraphContext)`: Fans out 6 parallel asynchronous extraction jobs (3 dimensions $\times$ 2 researchers) via `DimensionalExtractor.run(...)` to populate structural dimension sets.
* `make_cross_factorial_node(ctx: GraphContext)`: Invokes the `CrossFactorialAgent` to run a 9-cell parallel cross-disciplinary intersection analysis.
* `make_load_prompts_node(ctx: GraphContext)`: Synchronously loads explicit focus prompts into the state dict via `load_researcher_prompt(...)`.
* `make_hypotheses_node(ctx: GraphContext)`: Invokes the `HypothesesAgent` to synthesize contextual profiles, the cross-factorial matrix, and target prompts into candidate collaboration claims.
* `_refine_one(hypothesis: Hypothesis, ctx: GraphContext) -> tuple[RefinedHypothesis, CritiqueHistory]`: Executes an independent, bounded asynchronous while loop for a single hypothesis. Repeatedly triggers `ctx.stack.reviewer.review(...)` and `ctx.stack.refiner.refine(...)` up to `max_iterations`, breaking early if the reviewer returns a severity of `"accept"`.
* `make_refine_loop_node(ctx: GraphContext)`: Concurrently maps `_refine_one` across all candidate hypotheses using `asyncio.gather` and populates the finalized `refined_hypotheses` and `critique_histories` in the pipeline state.
* `make_rank_node(ctx: GraphContext)`: Passes the refined hypotheses payload to `ctx.stack.ranker.rank(...)` to generate final ordinal scores.





---

#### Context/State & Memory Schemas

* **Full File Path:** `src/matchmaker/schemas/state.py`
* **Core Classes:**
* `PipelineState`: The global, mutable LangGraph Pydantic state container. Retains fields for each sequential step (`profile_a`, `profile_b`, `background_a`, `background_b`, `dimensions_a`, `dimensions_b`, `matrix`, `prompt_a`, `prompt_b`, `hypotheses`, `critique_histories`, `refined_hypotheses`, `iteration`, `ranking`, and `token_spend_usd`).




* **Full File Path:** `src/matchmaker/schemas/publication.py`
* **Core Classes:**
* `Publication`: Pydantic schema representing a single ingested paper. Retains `id`, `title`, `abstract`, `authors`, `year`, `doi`, `source`, `source_id`, and `full_text_md`.
* `ResearcherProfile`: Top-level ingested state carrying `researcher_id`, `display_name`, `affiliation`, and a list of `Publication` entities.




* **Full File Path:** `src/matchmaker/schemas/summary.py`
* **Core Classes:**
* `SummaryItem`: Pydantic representation of a distilled dimensional factor. Contains `item_id`, `title`, `description`, and evidentiary links (`evidence`).
* `DimensionalSummary`: Groups a list of `SummaryItem` objects bound to a specific `Dim` (`"methods"`, `"open_questions"`, or `"stakes"`).
* `ResearcherBackground`: Consolidates the initial narrative profile synthesis and extracted keyword lists.




* **Full File Path:** `src/matchmaker/schemas/matrix.py`
* **Core Classes:**
* `ConnectionCell`: Self-describing schema retaining paired axis indicators (`dim_a`, `dim_b`), active item references (`items_a`, `items_b`), a categorical `connection_type`, a textual `rationale`, and bounded floating-point scores (`novelty_score`, `confidence`).
* `CrossFactorialMatrix`: Flat container holding exactly 9 `ConnectionCell` instances. Uses a strict post-initialization validator (`_validate_full_coverage`) to assert that the Cartesian product of `DIMS` $\times$ `DIMS` is perfectly populated. Exposes a `.get(dim_a, dim_b)` lookup utility.




* **Full File Path:** `src/matchmaker/schemas/prompt.py`
* **Core Classes:**
* `ResearcherPrompt`: Encapsulates explicit focus directives parsed from raw Markdown input files. Carries `researcher_id`, `current_focus`, `recent_milestones`, `blockers`, and optional `free_text`.




* **Full File Path:** `src/matchmaker/schemas/hypothesis.py`
* **Core Classes:**
* `Hypothesis`: Collaborative claim structure retaining `hypothesis_id`, `title`, `statement`, `mechanism`, a list of active connection mappings (`leverages_cells`), addressed prompt links (`addresses_prompts`), and a `confidence` metric.
* `RefinedHypothesis`: Inherits from `Hypothesis`. Appends iterative revision trails (`revision_notes`) and a tracking array of consumed critique cycles (`prior_critique_iterations`).




* **Full File Path:** `src/matchmaker/schemas/critique.py`
* **Core Classes:**
* `Critique`: Evaluation payload retaining the targeting `hypothesis_id`, specific `iteration` index, categorical `severity` (`"block"`, `"suggest"`, or `"accept"`), structured arrays (`strengths`, `weaknesses`, `suggested_revisions`), and the execution source (`reviewer_id`).
* `CritiqueHistory`: Explicit stateless thread container retaining a history array of sequential `Critique` objects. Exposes a `.latest()` lookup utility.




* **Full File Path:** `src/matchmaker/schemas/ranking.py`
* **Core Classes:**
* `RankedHypothesis`: Ordinal evaluation payload carrying `hypothesis_id`, numeric `rank`, floating-point `composite_score`, a dictionary mapping specific axis weights (`dimension_scores`), and an explicit textual `justification`.
* `Ranking`: Top-level consolidation payload holding an ordered array of `RankedHypothesis` items, a descriptive `methodology` string, and the execution source identifier (`ranker_id`).





---

#### Ingestion & Parsing Layer

* **Full File Path:** `src/matchmaker/ingestion/source.py`
* **Core Classes:**
* `Source`: Abstract Base Class (ABC) establishing the interface contract for corpus parsers.


* **Key Functions:**
* `fetch(researcher_id: str) -> ResearcherProfile`: Abstract coroutine signature returning a fully populated researcher profile entity.




* **Full File Path:** `src/matchmaker/ingestion/local_corpus.py`
* **Core Classes:**
* `LocalCorpusSource`: Concrete implementation of the `Source` ABC. Scans local disk directories (`papers/<researcher_id>/`) for pre-converted `.md` payloads.


* **Key Functions:**
* `_extract_title(markdown: str, fallback: str) -> str`: Uses multi-line regular expressions (`_H1`, `_BOLD_H2`) to parse document headers, stripping formatting characters and skipping boilerplate sections to extract valid academic titles.
* `fetch(researcher_id: str) -> ResearcherProfile`: Asynchronously iterates over targeted `.md` files, hashes unique identifiers, extracts titles, reads complete Markdown texts into memory, and constructs the finalized `ResearcherProfile`.




* **Full File Path:** `src/matchmaker/ingestion/prompts_loader.py`
* **Core Classes:** None. Exposes parsing utilities.
* **Key Functions:**
* `_split_sections(text: str) -> dict[str, str]`: Uses multiline regular expressions to split text blocks by standard Markdown level-two headers (`## Heading`).
* `parse_prompt_markdown(text: str, *, researcher_id: str) -> ResearcherPrompt`: Parses structured sections (`Current focus`, `Recent milestones`, `Blockers`). Absorbs auxiliary text blocks into a cohesive `free_text` buffer.
* `load_researcher_prompt(prompts_dir: Path, researcher_id: str) -> ResearcherPrompt`: Reads the target input file from disk and triggers string parsing.




* **Full File Path:** `utils/pdf_to_markdown.py`
* **Core Classes:** None. Procedural script.
* **Key Functions:**
* Interrogates `papers/` subdirectories, utilizing `pymupdf4llm.to_markdown(...)` to convert native binary PDF files into accessible full-text UTF-8 Markdown files.





---

#### Autonomous Agents & Synthesis Layer

* **Full File Path:** `src/matchmaker/agents/llm.py`
* **Core Classes:**
* `CostCeilingExceeded`: Exception raised when token cost limits are breached.
* `TokenSpend`: Mutable tracking container computing aggregate financial expenditures (`usd`), execution tallies (`calls`), and model usage sub-totals based on hardcoded pricing rates (`MODEL_PRICING`).
* `AnthropicClient`: Core async interface wrapping `AsyncAnthropic`. Forces Pydantic-bound tool JSON schemas onto inference calls and strictly tracks downstream token accumulation.


* **Key Functions:**
* `structured(..., response_model: type[T], ...) -> T`: Formats the Pydantic target as an Anthropic tool schema, issues a native tool-choice API message call, calculates financial accumulation via `spend.add(...)`, validates the returned tool-use block, and returns the strictly instantiated Pydantic model. Intercepts calls exceeding the budget breaker.




* **Full File Path:** `src/matchmaker/agents/background.py`
* **Core Classes:**
* `_BackgroundOutput`: Internal validation schema expecting a textual `narrative` and a substantive array of `keywords`.
* `ResearcherBackgroundAgent`: Generates narrative profiles from raw input corpora.


* **Key Functions:**
* `run(profile: ResearcherProfile) -> ResearcherBackground`: Formats document abstracts and titles via prompt templates, calls `llm.structured(...)` at temperature `0.0`, and returns a consolidated `ResearcherBackground` instance.




* **Full File Path:** `src/matchmaker/agents/extraction.py`
* **Core Classes:**
* `_ItemsOutput`: Internal structured container expecting an array of `SummaryItem` entities.
* `DimensionalExtractor`: Parameterized agent targeting a discrete analytical dimension.


* **Key Functions:**
* `run(profile: ResearcherProfile, background: ResearcherBackground) -> DimensionalSummary`: Renders the target dimension prompt (`methods`, `open_questions`, or `stakes`) alongside narrative profiles, calls `llm.structured(...)` to enforce citation bindings, and populates the target `DimensionalSummary`.




* **Full File Path:** `src/matchmaker/agents/cross_factorial.py`
* **Core Classes:**
* `_CellOutput`: Internal schema mapping target items, connection categorizations, structural rationales, and metrics.
* `CrossFactorialAgent`: Manages Cartesian intersection evaluation.


* **Key Functions:**
* `_one_cell(...) -> _CellOutput`: Formats axis items into a targeted template and executes a structured inference evaluation.
* `run(...) -> CrossFactorialMatrix`: Concurrently maps `_one_cell` across all 9 possible combinations of `DIMS` $\times$ `DIMS` via `asyncio.gather`, gathers responses, binds active coordinate labels, and returns a validated `CrossFactorialMatrix`.




* **Full File Path:** `src/matchmaker/agents/hypotheses.py`
* **Core Classes:**
* `_CellRef` / `_HypothesisDraft` / `_HypothesesOutput`: Internal validation schemas mapping candidate hypothesis drafts.
* `HypothesesAgent`: Orchestrates the collaborative claim synthesis.


* **Key Functions:**
* `run(...) -> list[Hypothesis]`: Injects narrative summaries, explicit prompts, blockers, and the complete string-formatted cross-factorial matrix into a synthesis prompt. Calls `llm.structured(...)` at temperature `0.7` to yield 3 to 7 actionable, highly falsifiable `Hypothesis` entities.





---

#### Refinement & Evaluation Stack

* **Full File Path:** `src/matchmaker/refinement/protocols.py`
* **Core Classes:**
* `ReviewerProtocol` / `RefinerProtocol` / `RankerProtocol`: Stateless runtime-checkable `Protocol` definitions establishing strict data-in/data-out boundary contracts for evaluation modules. Decouples backends from orchestration dependencies.




* **Full File Path:** `src/matchmaker/refinement/factory.py`
* **Core Classes:**
* `RefinementStack`: Simple structural container holding active instances of the `ReviewerProtocol`, `RefinerProtocol`, and `RankerProtocol`.


* **Key Functions:**
* `build_refinement_stack(settings: Settings, *, llm: AnthropicClient | None = None) -> RefinementStack`: Evaluates `settings.refinement_backend` and instantiates the concrete evaluation stack (`mock`, `local`, or `denario`).




* **Full File Path:** `src/matchmaker/refinement/local.py`
* **Core Classes:**
* `_CritiqueOutput` / `_RefinedOutput` / `_RankingOutput`: Internal validation structures.
* `LocalLLMReviewer` / `LocalLLMRefiner` / `LocalLLMRanker`: Concrete implementations satisfying the refinement protocols via local Anthropic tool-use calls.


* **Key Functions:**
* `LocalLLMReviewer.review(hypothesis: Hypothesis, history: CritiqueHistory) -> Critique`: Injects hypothesis attributes and historic iteration trails into an adversarial prompt template, returning a categorized `Critique` payload.
* `LocalLLMRefiner.refine(hypothesis: Hypothesis, critique: Critique, history: CritiqueHistory) -> RefinedHypothesis`: Processes current claims against newly generated weaknesses and suggested revisions, generating an updated `RefinedHypothesis`.
* `LocalLLMRanker.rank(hypotheses: list[RefinedHypothesis]) -> Ranking`: Formats all refined candidates into a global comparison block, calling `llm.structured(...)` at temperature `0.2` to assign precise ordinal ranks and composite scoring distributions.




* **Full File Path:** `src/matchmaker/refinement/denario.py`
* **Core Classes:**
* `DenarioReviewer` / `DenarioRefiner` / `DenarioRanker`: Concrete structural stubs satisfying protocol type checks. Configured to interface with external endpoints upon production deployment.





---

#### Output, Reporting & Artifact Management

* **Full File Path:** `src/matchmaker/io/artifacts.py`
* **Core Classes:** None.
* **Key Functions:**
* `_to_jsonable(payload: Any) -> Any`: Recursively traverses Pydantic models, iterables, and dictionaries, invoking `.model_dump(mode="json")` to produce standard JSON primitives.
* `write_artifact(outputs_dir: Path, stage: str, run_id: str, payload: Any) -> Path`: Appends timestamped structures and explicit run identifiers to paths under `outputs/<stage>/`, serializing state payloads to disk with non-destructive, diffable write isolation.




* **Full File Path:** `src/matchmaker/io/reports.py`
* **Core Classes:** None.
* **Key Functions:**
* `_matrix_grid(matrix: CrossFactorialMatrix) -> str`: Renders a collapsed 3x3 Markdown ASCII matrix grid outlining categorical intersection typologies and scoring metrics.
* `_matrix_details(matrix: CrossFactorialMatrix) -> str`: Unrolls complete cell rationales into comprehensive Markdown sections.
* `render_final_report(state: PipelineState) -> str`: Parses the terminal state dictionary, consolidates financial metadata (`token_spend_usd`), maps matrix cells, and outputs an end-to-end human-readable Markdown summary.