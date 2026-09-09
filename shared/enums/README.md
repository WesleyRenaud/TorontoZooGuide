# Shared wire enums

JSON files in this folder are the **only** definition of shared wire enum values.
API and frontend modules load them at runtime (they do not copy the values).

- Catalog: [`catalog.json`](catalog.json)
- Check: `python3 tools/checkSharedEnums.py` (also run from `npm run lint:py`)

Current shared enums:

| JSON | API | Frontend |
|---|---|---|
| `apiErrorType.json` | `ApiErrorType` | `ApiErrorType` |
| `animalViewingScope.json` | `AnimalViewingScope` | `AnimalViewingScope` |
| `enclosureType.json` | `EnclosureType` | `EnclosureType` |
| `itemType.json` | `ItemType` | `ItemType` |
| `itineraryAdjustmentType.json` | `ItineraryAdjustmentType` | `ItineraryAdjustmentType` |
| `itineraryErrorType.json` | `ItineraryErrorType` | `ItineraryErrorType` |
| `itineraryEventType.json` | `ItineraryEventType` | `ItineraryEventType` |
| `itinerarySaveIssueItemType.json` | `ItinerarySaveIssueItemType` | `ItinerarySaveIssueItemType` |
| `openingScheduleOverlapErrorType.json` | `OpeningScheduleOverlapErrorType` | `OpeningScheduleOverlapErrorType` |
| `openingScheduleOverlapResolution.json` | `OpeningScheduleOverlapResolution` | `OpeningScheduleOverlapResolution` |
| `itineraryTransportationStationRole.json` | `ItineraryTransportationStationRole` | `ItineraryTransportationStationRole` |
| `position.json` | `Position` | `Position` |
| `scheduleItemKind.json` | `ScheduleItemKind` | `ScheduleItemKind` |
| `transportationName.json` | `TransportationName` | `TransportationName` |
| `transportationRouteId.json` | `TransportationRouteId` | `TransportationRouteId` |

To add an enum:

1. Add `shared/enums/<name>.json` (`MEMBER_NAME` → wire value)
2. Register it in `catalog.json`
3. Add a thin API loader module and a thin JS class that imports the JSON
4. API modules listed in `catalog.json` are automatically skipped by the
   one-class-per-file linter (they load values from JSON rather than declaring a
   classic `class` body)

## Object-valued enums

Most JSON files map `MEMBER_NAME` to a plain wire value. An enum whose members
carry extra metadata instead maps `MEMBER_NAME` to an object and sets
`"valueShape": "object"` on its `catalog.json` entry:

```json
"GUARDIANS_TALK": { "kind": "guardians_talk", "itemType": "guardians_talks" }
```

- `kind` (required) is the wire value.
- `itemType` (optional) is the plural itinerary module name for that kind.
- `onboarding` / `offboarding` (optional booleans) mark transportation station
  roles that board or alight riders.

Load these with `SharedEnumValues.load_object_members( '<name>.json' )` on the
API side. The API enum takes its member values from `kind`; optional metadata
fields are consumed by that enum module. The JS class freezes one object per
member so members stay comparable with `===`. `checkSharedEnums.py` verifies
wire values (`kind`) and that both sides load the shared JSON.
