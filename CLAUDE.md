# Project: Multi-Agent Research Matchmaking Workflow

## Project Overview
This project is an agentic workflow designed to discover serendipitous, interdisciplinary research collaborations. It ingests the academic history of two distinct researchers, reduces their profiles into semantic dimensions (Methods, Open Questions, Stakes), computes a cross-factorial interaction matrix to find non-obvious overlaps, and synthesizes these insights into concrete joint research hypotheses.

## Architectural State Machine
The system follows a strict 8-stage Directed Acyclic Graph (DAG):
1. **Inputs:** Target researchers defined.
2. **Retrieval:** Google Scholar / Semantic Scholar API integration.
3. **Extraction:** Profiles distilled into `Methods`, `Open Questions`, and `Stakes`.
4. **Cross-Factorial Layer:** A 3x3 Cartesian product matrix comparing all dimensions.
5. **Post-Cross-Factorial Inputs:** Injection of explicit current-state "Researcher-Derived Prompts."
6. **Synthesis:** Combining the matrix and live prompts into actionable hypotheses.
7. **Refinement:** An adversarial loop (Review -> Refine).
8. **Final Outputs:** Ranked list of optimal research hypotheses.

## ⚠️ Core Architectural Constraints
* **The Denario Exception:** Stages 7 and 8 (Reviewer, Refiner, and Ranking agents) will ultimately be handled by proprietary local Denario agents from Cambridge. 
    * **Actionable Rule:** Do *not* hardcode standard API calls (like OpenAI or Anthropic) for these final stages. You must build Abstract Base Classes (ABCs) or standard interface wrappers for the Refinement and Ranking stages so the Denario endpoints can be seamlessly plugged in later. Use mock functions for these stages during initial development.
* **State Management:** Because this is a multi-step, multi-agent pipeline, state must be cleanly managed and auditable. Prefer explicit data handoffs over hidden state.

## Coding Conventions & Guidelines
* **Language:** Python (Assume 3.11+).
* **Data Validation:** Use `pydantic` extensively. Every intermediate handoff between agents (especially the inputs/outputs of the Cross-Factorial Layer) MUST be defined by strict Pydantic schemas.
* **Type Hinting:** Strict type hinting is mandatory for all functions and class methods.
* **Asynchronous I/O:** Use `asyncio` for all API calls (Scholar scraping, LLM generation) to ensure the system is performant when scaling to multiple agents.
* **Logging:** Agent workflows are notoriously difficult to debug. Implement verbose, structured logging (e.g., using `structlog` or standard `logging`) at every agent handoff boundary. 
* **Modularity:** Keep agent definitions, prompt templates, and data schemas in separate files/directories.

## CLI Interaction Mode
When asked to implement a feature, always draft the Pydantic schema for the data structures first, ask for approval if the domain logic seems ambiguous, and then proceed to implement the execution logic.