# V11.2 Architecture

Candidate implementation SHA: `56347ababaea5af5e088d26d52f61df807ae4f70`

The static builder now generates one canonical detail route for each active catalog product. `catalog.json` owns product identity and commercial facts, `discovery.json` owns departments and education links, `public-sources.json` owns evidence relationships, and `product-labels.json` owns verified-label state. `relationships.json` documents those joins and their evidence boundaries.

Product-specific source mappings are rendered distinctly from department context. No symptom graph, inferred disease link, rating, review, availability assertion, or fabricated offer schema is generated. Search, cards, articles, Evidence, departments, sitemap, validation, and the mobile dock all route through the generated system.
