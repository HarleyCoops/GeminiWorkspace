# Implementation Plan - Transforming Workspace into a GitHub Template

This plan outlines the steps to make the `antigravity-workspace-template` a truly "plug-and-play" repository for any user who clones or uses it as a GitHub template.

## 1. Environment Configuration
- **Create `.env.example`**: Define all necessary environment variables without sensitive values.
- **Ensure `.gitignore` is correct**: Verify that `.env`, `agent_memory.json`, and personal artifacts are ignored.

## 2. Model Context Protocol (MCP) Portability
- **Standardize `mcp_servers.json`**:
    - Replace hardcoded absolute paths with `npx` commands where available (e.g., `@modelcontextprotocol/server-github`).
    - Move machine-specific configurations to a `mcp_servers.json.example` or use environment variables within the config.
    - Ensure commands are cross-platform (using `npx` or `python` instead of direct paths to Windows-specific executables).

## 3. GitHub Template Activation
- **Instruction**: Explain how to go to repository settings and check "Template repository".
- **GitHub Actions**: Add a basic CI workflow to verify the project structure or run tests, showing community competence.

## 4. Documentation Polish
- **Update README.md**:
    - Add a "How to use this as a template" section (already partially exists).
    - Clarify the "Clone -> Rename -> Prompt" workflow for users using the "Use this template" button.
- **Project Mission**: Ensure `mission.md` is generic enough or has clear "Replace me" instructions.

## 5. Cleanup
- Remove any lingering personal research logs or specific project artifacts that shouldn't be in a clean slate template.
