# Roadmap

## What I Would Keep In Production

- schema-first extraction design
- source traceability to report and page
- automated extraction quality checks
- vector search for similar historical observations
- Qdrant or another production vector store

## What I Would Replace In Production

- replace local JSON with PostgreSQL or a lakehouse table
- move LLM extraction to an asynchronous job queue
- add a React or Next.js frontend
- add authentication and document-level access control
- add audit logging for sensitive report access
- use managed infrastructure for deployment and monitoring

## Three-Month Roadmap

1. Add more public inspection reports and normalize the observation taxonomy.
2. Add human review sampling to estimate extraction precision.
3. Add OCR support for scanned or image-heavy reports.
4. Add trend dashboards for recurring defects, categories, and risk levels.
5. Add a React or Next.js frontend with role-based access.
6. Add production Docker Compose or cloud deployment.
7. Add an insight layer that summarizes recurring risks and recommended actions from retrieved cases.
8. Add support for images, plans, and heterogeneous construction data sources.

