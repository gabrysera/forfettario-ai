# ADR-001 — Deterministic fiscal core

## Status
Accepted.

## Context
LLMs are useful for conversation and extraction but are not suitable as the source of authoritative fiscal rules, arithmetic, deadlines or form mappings.

## Decision
All consequential fiscal logic must live in deterministic, versioned code and configuration. LLMs may call the fiscal engine and explain its outputs, but may not replace it.

Every fiscal rule must have an applicable period, source reference and tests.

## Consequences

- Removing or changing the LLM provider must not change fiscal truth.
- UI and prompts cannot contain authoritative fiscal constants.
- Rule changes require tests and source updates.
- The fiscal engine should expose explainable calculation components.
