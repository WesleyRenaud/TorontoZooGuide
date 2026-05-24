import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import {
   migrateStoredSelectionItems,
   normalizeStoredId,
   normalizeStoredLink,
   normalizeStoredString,
} from './base/storedSelection.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';
import { buildScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import { APP_STRINGS } from '../../strings.js';

function getOccurrenceName(row) {
   return row?.name ?? '';
}

function buildOccurrenceImageSrc(imageDirectory, name) {
   const file = normalizeAssetKey(name || '');

   if (!file) {
      return null;
   }

   return `../images/details/${imageDirectory}/${file}.png`;
}

function buildOccurrenceSubtitle({
   primaryLabel,
   primaryValue = '',
   timeRange = '',
} = {}) {
   const primaryLine = primaryValue
      ? `${primaryLabel}: ${primaryValue}`
      : `${primaryLabel}: -`;

   return timeRange
      ? `${primaryLine}  •  Time: ${timeRange}`
      : primaryLine;
}

function createStoredOccurrenceFromString(item, {
   emptyStoredFields,
   buildImageSrc,
} = {}) {
   const name = normalizeStoredString(item);

   if (!name) {
      return null;
   }

   return {
      id: name,
      name,
      ...emptyStoredFields,
      imageSrc: buildImageSrc(name),
   };
}

function createStoredOccurrenceFromObject(item, {
   buildImageSrc,
   includeLink = false,
   readStoredFields,
} = {}) {
   const name = normalizeStoredString(item.name);
   const id = normalizeStoredId(item.id, name);

   if (!id) {
      return null;
   }

   const storedOccurrence = {
      id,
      name,
      ...readStoredFields(item),
      imageSrc: normalizeStoredString(item.imageSrc) || buildImageSrc(name),
   };

   if (includeLink) {
      storedOccurrence.link = normalizeStoredLink(item.link);
   }

   const startTime = normalizeStoredString(item.start_time);

   if (startTime) {
      storedOccurrence.start_time = startTime;
   }

   const endTime = normalizeStoredString(item.end_time);

   if (endTime) {
      storedOccurrence.end_time = endTime;
   }

   const maximumDuration = Number(item.maximum_duration);

   if (Number.isFinite(maximumDuration) && maximumDuration > 0) {
      storedOccurrence.maximum_duration = maximumDuration;
   }

   return storedOccurrence;
}

function createOccurrenceMigration({
   emptyStoredFields,
   buildImageSrc,
   includeLink = false,
   readStoredFields,
} = {}) {
   return (items) => migrateStoredSelectionItems(items, {
      fromString: (item) => createStoredOccurrenceFromString(item, {
         emptyStoredFields,
         buildImageSrc,
      }),
      fromObject: (item) => createStoredOccurrenceFromObject(item, {
         buildImageSrc,
         includeLink,
         readStoredFields,
      }),
   });
}

function createOccurrenceSelection(row, {
   getId,
   getLink = null,
   getName,
   buildImageSrc,
   buildSelectionFields,
   getTimeOfDay,
} = {}) {
   const name = getName(row);
   const startTime = normalizeStoredString(getTimeOfDay(row));
   const selection = {
      id: getId(row),
      name,
      ...buildSelectionFields(row),
      imageSrc: buildImageSrc(name),
   };

   const link = getLink?.(row) ?? null;

   if (link) {
      selection.link = link;
   }

   const maximumDuration = Number(row?.maximum_duration);

   if (Number.isFinite(maximumDuration) && maximumDuration > 0) {
      selection.maximum_duration = maximumDuration;
   }

   if (startTime) {
      selection.start_time = startTime;
   }

   const endTime = normalizeStoredString(row?.end_time);

   if (endTime) {
      selection.end_time = endTime;
   }

   return selection;
}

export function createScheduledOccurrenceSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
   hideNextButton = false,
   storageKey,
   responseKey,
   searchFlag,
   imageDirectory,
   defaultTitle,
   heading,
   subtitle,
   emptyText,
   primaryLabel,
   getName = getOccurrenceName,
   getId = getName,
   getPrimaryValue,
   getTimeOfDay = (row) => normalizeStoredString(row?.start_time),
   getLink = null,
   emptyStoredFields = {},
   readStoredFields,
   buildSelectionFields,
} = {}) {
   const buildImageSrc = (name) => (
      buildOccurrenceImageSrc(imageDirectory, name)
   );

   const migrateSelected = createOccurrenceMigration({
      emptyStoredFields,
      buildImageSrc,
      includeLink: typeof getLink === 'function',
      readStoredFields,
   });

   const makeSelection = (row) => createOccurrenceSelection(row, {
      getId,
      getLink,
      getName,
      getTimeOfDay,
      buildImageSrc,
      buildSelectionFields,
   });

   return createItinerarySelectorController({
      mountEl,
      onPrev,
      onNext,
      onFinish,
      onClose,
      hideNextButton,

      storageKey,
      migrateSelected,

      getContext: getItineraryDateSearchContext,

      buildSearchPayload: (query) => ({
         query,
         [searchFlag]: true,
      }),

      extractRows: (response) => sortScheduledOccurrencesByStartTime(
         response[responseKey],
         getTimeOfDay),

      getId,
      getTitle: (row) => getName(row) || defaultTitle,
      getSubtitle: (row) => buildOccurrenceSubtitle({
         primaryLabel,
         primaryValue: getPrimaryValue(row),
         timeRange: buildScheduledOccurrenceTimeRange(row),
      }),
      getImageSrc: (row) => buildImageSrc(getName(row)),
      getInfoLink: getLink || undefined,
      makeSelection,

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: heading,
      subtitle,
      emptyText,
   });
}
