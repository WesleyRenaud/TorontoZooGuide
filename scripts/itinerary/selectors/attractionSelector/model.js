import { AssetKeyNormalizer } from '../../../assets/assetKeyNormalizer.js';
import {
   migrateStoredSelectionItems,
   normalizeStoredBoolean,
   normalizeStoredId,
   normalizeStoredLink,
   normalizeStoredString,
} from '../base/storedSelection.js';
import { buildOccurrenceSubtitle } from '../../scheduledOccurrencePresentation.js';
import { buildScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { APP_STRINGS } from '../../../strings.js';

const DEFAULT_ATTRACTION_TITLE = 'Attraction';
const CLOSED_ATTRACTION_FALLBACK_NAME = 'This attraction';

export function getAttractionName(row) {
   return typeof row?.name === 'string'
      ? row.name
      : '';
}

export function getAttractionId(row) {
   return getAttractionName(row);
}

export function getAttractionTitle(row) {
   return getAttractionName(row) || DEFAULT_ATTRACTION_TITLE;
}

export function getAttractionInfoLink(row) {
   const value = row?.info_link ?? null;
   const link = typeof value === 'string' ? value.trim() : '';
   return link || null;
}

export function isFreeWithAdmission(row) {
   return row?.free_with_admission === true;
}

export function isSeasonalAttraction(row) {
   return row?.part_of_seasonal_attraction === true;
}

export function isClosedAttraction(row) {
   return row?.is_closed === true;
}

export function isAlsoTransportationAttraction(row) {
   return row?.is_also_transportation === true;
}

export function getAttractionSubtitle(row) {
   return buildOccurrenceSubtitle({
      primaryValue: isFreeWithAdmission(row)
         ? APP_STRINGS.search.freeWithAdmission
         : APP_STRINGS.search.extraCharge,
      timeRange: buildScheduledOccurrenceTimeRange({
         start_time: row?.open_time,
         end_time: row?.close_time,
      }),
   });
}

export function buildAttractionImageSrc(row) {
   const attractionFile = AssetKeyNormalizer.normalize(getAttractionName(row));

   if (!attractionFile) {
      return null;
   }

   return `../images/details/attractions/${attractionFile}.png`;
}

function createStoredAttractionFromString(item) {
   const name = normalizeStoredString(item);

   if (!name) {
      return null;
   }

   return {
      id: name,
      name,
      subtitle: '',
      freeWithAdmission: false,
      seasonal: false,
      isClosed: false,
      addedAsAttraction: false,
      infoLink: null,
      imageSrc: null,
   };
}

function createStoredAttractionFromObject(item) {
   const name = normalizeStoredString(item.name);
   const id = normalizeStoredId(item.id, name);

   if (!id) {
      return null;
   }

   return {
      id,
      name,
      subtitle: normalizeStoredString(item.subtitle),
      freeWithAdmission: normalizeStoredBoolean(item.freeWithAdmission),
      seasonal: normalizeStoredBoolean(item.seasonal),
      isClosed: normalizeStoredBoolean(item.isClosed),
      addedAsAttraction: normalizeStoredBoolean(item.addedAsAttraction),
      infoLink: normalizeStoredLink(item.infoLink),
      imageSrc: normalizeStoredLink(item.imageSrc),
   };
}

export function migrateStoredAttractions(items) {
   return migrateStoredSelectionItems(items, {
      fromString: createStoredAttractionFromString,
      fromObject: createStoredAttractionFromObject,
   });
}

export function makeAttractionSelection(row) {
   return {
      id: getAttractionId(row),
      name: getAttractionName(row),
      subtitle: getAttractionSubtitle(row),
      freeWithAdmission: isFreeWithAdmission(row),
      seasonal: isSeasonalAttraction(row),
      isClosed: isClosedAttraction(row),
      addedAsAttraction: isAlsoTransportationAttraction(row),
      infoLink: getAttractionInfoLink(row),
      imageSrc: buildAttractionImageSrc(row),
   };
}

export function shouldConfirmClosedAttraction({
   row,
   isSelected,
   includeClosedAttractions,
} = {}) {
   if (isSelected) {
      return false;
   }

   if (!includeClosedAttractions) {
      return false;
   }

   return isClosedAttraction(row);
}

export function shouldConfirmAlsoTransportationAttraction({
   row,
   isSelected,
} = {}) {
   if (isSelected) {
      return false;
   }

   return isAlsoTransportationAttraction(row);
}

export function buildClosedAttractionMessage(row) {
   const name = getAttractionName(row) || CLOSED_ATTRACTION_FALLBACK_NAME;
   return `The ${name} is closed on your visit date. Do you still want to add it to your itinerary?`;
}

export function buildAlsoTransportationAttractionMessage(row) {
   return APP_STRINGS.itinerary.confirmation.attractionAlsoTransportationMessage(
      getAttractionName(row)
   );
}
