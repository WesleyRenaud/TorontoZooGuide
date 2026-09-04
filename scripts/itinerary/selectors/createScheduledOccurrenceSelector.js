import { StoredSelection } from './base/storedSelection.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ScheduledOccurrencePresentation } from '../scheduledOccurrencePresentation.js';
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import { ScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import { APP_STRINGS } from '../../strings.js';

function getOccurrenceName(row) {
   return row?.name ?? '';
}

function createStoredOccurrenceFromString(item, {
   emptyStoredFields,
   buildImageSrc,
} = {}) {
   const name = StoredSelection.normalizeStoredString(item);

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
   getId,
} = {}) {
   const name = StoredSelection.normalizeStoredString(item.name);
   const id = StoredSelection.normalizeStoredString(getId(item));

   if (!id) {
      return null;
   }

   const storedOccurrence = {
      id,
      name,
      ...readStoredFields(item),
      imageSrc: StoredSelection.normalizeStoredString(item.imageSrc) || buildImageSrc(name),
   };

   if (includeLink) {
      storedOccurrence.link = StoredSelection.normalizeStoredLink(item.link);
   }

   const startTime = StoredSelection.normalizeStoredString(item.start_time);

   if (startTime) {
      storedOccurrence.start_time = startTime;
   }

   const endTime = StoredSelection.normalizeStoredString(item.end_time);

   if (endTime) {
      storedOccurrence.end_time = endTime;
   }

   const maximumDuration = Number(item.maximum_duration);

   if (Number.isFinite(maximumDuration) && maximumDuration > 0) {
      storedOccurrence.maximum_duration = maximumDuration;
   }

   return storedOccurrence;
}

export function createScheduledOccurrenceMigration({
   emptyStoredFields,
   buildImageSrc,
   includeLink = false,
   readStoredFields,
   getId,
} = {}) {
   return (items) => StoredSelection.migrateStoredSelectionItems(items, {
      fromString: (item) => createStoredOccurrenceFromString(item, {
         emptyStoredFields,
         buildImageSrc,
      }),
      fromObject: (item) => createStoredOccurrenceFromObject(item, {
         buildImageSrc,
         includeLink,
         readStoredFields,
         getId,
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
   const startTime = StoredSelection.normalizeStoredString(getTimeOfDay(row));
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

   const endTime = StoredSelection.normalizeStoredString(row?.end_time);

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
   getName = getOccurrenceName,
   getId = getName,
   getPrimaryValue,
   getTimeOfDay = (row) => StoredSelection.normalizeStoredString(row?.start_time),
   getLink = null,
   emptyStoredFields = {},
   readStoredFields,
   buildSelectionFields,
} = {}) {
   const buildImageSrc = (name) => (
      ScheduledOccurrencePresentation.buildOccurrenceDetailImageSrc(imageDirectory, name)
   );

   const migrateSelected = createScheduledOccurrenceMigration({
      emptyStoredFields,
      buildImageSrc,
      includeLink: typeof getLink === 'function',
      readStoredFields,
      getId,
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

      getContext: ItinerarySearchContext.getItineraryDateSearchContext,

      buildSearchPayload: (query) => ({
         query,
         [searchFlag]: true,
      }),

      extractRows: (response) => ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(
         response[responseKey],
         getTimeOfDay),

      getId,
      getTitle: (row) => getName(row) || defaultTitle,
      getSubtitle: (row) => ScheduledOccurrencePresentation.buildOccurrenceSubtitle({
         primaryValue: getPrimaryValue(row),
         timeRange: ScheduledOccurrenceTimeRange.buildScheduledOccurrenceTimeRange(row),
      }),
      getImageSrc: (row) => buildImageSrc(getName(row)),
      getInfoLink: () => null,
      onTitleClick: typeof getLink === 'function'
         ? (row) => {
            const link = getLink(row);

            if (link) {
               window.open(link, '_blank');
            }
         }
         : null,
      makeSelection,

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: heading,
      subtitle,
      emptyText,
   });
}
