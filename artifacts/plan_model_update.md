# Plan: Global Model Name Update

This plan outlines the steps to update the default model names globally across the repository.

## Changes

### 1. Update `src/config.py`
Change the default values for Gemini and OpenAI models to the latest versions requested.
- `GEMINI_MODEL_NAME`: `"gemini-2.0-flash-exp"` -> `"gemini-3.0-flash"`
- `OPENAI_MODEL`: `"gpt-4o-mini"` -> `"gpt-5.2"`

### 2. Update `README.md`
Update badges and feature descriptions to reflect the switch to Gemini 3.
- Update the Gemini badge.
- Update references to "Gemini 2.0 Flash" to "Gemini 3.0 Flash".

### 3. Update `.antigravity/rules.md`
Ensure consistency in the AI persona and protocol descriptions. (Already mentions Gemini 3 in some places, but will verify).

## Execution Steps

1.  **Modify `src/config.py`**: Update the `Settings` class defaults.
2.  **Modify `README.md`**: Update version strings and badges.
3.  **Verification**: Grep the codebase for any remaining references to old model names to ensure none were missed.

## Success Criteria
- Grep search for "gemini-2.0" returns no relevant functional results.
- Grep search for "gpt-4o" returns no relevant functional results.
- `src/config.py` contains the new model names.
- Documentation is consistent with the latest models.
