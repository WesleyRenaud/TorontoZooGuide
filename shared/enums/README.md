# Shared wire enums

JSON files in this folder are the **only** definition of shared wire enum values.
API and frontend modules load them at runtime (they do not copy the values).

- Catalog: [`catalog.json`](catalog.json)
- Check: `python3 tools/checkSharedEnums.py` (also run from `npm run lint:py`)

To add an enum:

1. Add `shared/enums/<name>.json` (`MEMBER_NAME` → wire value)
2. Register it in `catalog.json`
3. Add a thin API loader module and a thin JS class that imports the JSON
4. Exclude the API loader module from one-class-per-file if it uses `Enum(...)` construction
