# Security Policy

## Scope

This policy covers the Trimorious model repository, adapter artifacts and release workflow.

## Reporting a vulnerability

Please do not publish credentials, private datasets, personal information or exploitable details in a public issue.

Use GitHub's **Report a vulnerability** feature in the repository Security tab to submit a private report. Include:
- affected repository/file or release revision;
- a concise impact description;
- reproduction steps or a safe proof of concept;
- relevant logs with secrets and personal data removed.

## Model-specific considerations

- Treat model outputs as untrusted generated content.
- Do not put API keys, access tokens or confidential documents into public prompts or training examples.
- Validate retrieved documents and tool outputs as untrusted input.
- Run model-generated code and tool actions in a sandbox with explicit resource and network controls.
- Report suspected dataset exposure or credential leakage promptly; rotate exposed credentials.
