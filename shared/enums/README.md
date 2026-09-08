# Shared wire enums

JSON files in this folder are the **only** definition of shared wire enum values.
API and frontend modules load them at runtime (they do not copy the values).

- Catalog: [`catalog.json`](catalog.json)
- Check: `python3 tools/checkSharedEnums.py` (also run from `npm run lint:py`)

Current shared enums:

| JSON | API | Frontend |
|---|---|---|
| `animalViewingScope.json` | `AnimalViewingScope` | `AnimalViewingScope` |
| `enclosureType.json` | `EnclosureType` | `EnclosureType` |
| `itemType.json` | `ItemType` | `ItemType` |
| `itineraryEventType.json` | `ItineraryEventType` | `ItineraryEventType` |
| `itinerarySaveIssueItemType.json` | `ItinerarySaveIssueItemType` | `ItinerarySaveIssueItemType` |

To add an enum:

1. Add `shared/enums/<name>.json` (`MEMBER_NAME` → wire value)
2. Register it in `catalog.json`
3. Add a thin API loader module and a thin JS class that imports the JSON
4. API modules listed in `catalog.json` are automatically skipped by the
   one-class-per-file linter (they load values from JSON rather than declaring a
   classic `class` body)
