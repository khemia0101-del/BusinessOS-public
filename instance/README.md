# Business Instance

Each BusinessOS VM has one private `instance/business.yaml` created from `business.example.yaml`.

`business.yaml` may contain company identifiers and source locations, so it is ignored by Git. Credentials belong only in `.env`. Runtime evidence, extracted records, reports, and communications belong in private storage on that VM.

The generic repository must continue to work when `business.yaml` is replaced with an entirely different industry and company.

The business stage is set only by `BUSINESS_STAGE` in the VM's `.env`, loaded into service processes. Do not duplicate stage in YAML. Use `pre_acquisition`, `transition`, or `operating`; see `acquisition-mode.md` for authority boundaries.

Copy the root `employees.json` template to `instance/employees.json` before adding real people. This private roster is ignored by Git. The gateway uses this path by default; a custom `BUSINESSOS_EMPLOYEES_FILE` must also be communicated to Hermes and its employee profiles.
