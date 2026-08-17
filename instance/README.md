# Business Instance

Each BusinessOS VM has one private `instance/business.yaml` created from `business.example.yaml`.

`business.yaml` may contain company identifiers and source locations, so it is ignored by Git. Credentials belong only in `.env`. Runtime evidence, extracted records, reports, and communications belong in private storage on that VM.

The generic repository must continue to work when `business.yaml` is replaced with an entirely different industry and company.
