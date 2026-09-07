import { StoredSelection } from './base/storedSelection.js';

export class ScheduledOccurrenceSelectorFactory {
   static getOccurrenceName(row) {
      return row?.name ?? '';
   }

   static createStoredOccurrenceFromString(item, {
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

   static createStoredOccurrenceFromObject(item, {
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

   static createOccurrenceSelection(row, {
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
}
