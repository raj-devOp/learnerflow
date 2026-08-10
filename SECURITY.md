# Security Posture — LearnerFlow

- Containers run as a non-root user (`appuser`), following least-privilege principles.
- Images are scanned for vulnerabilities using Docker Scout / Trivy on each build.
- Base images are kept current; scan recommendations are reviewed and applied.
- No real data is ever used — all learner records are synthetic (Faker), supporting GDPR-safe development.
- Secrets are never baked into images (to be managed via Azure Key Vault in later stages).
- Base images are scanned and compared; the version with the lowest overall severity profile is selected. Findings are reviewed on each build rather than assumed away.
