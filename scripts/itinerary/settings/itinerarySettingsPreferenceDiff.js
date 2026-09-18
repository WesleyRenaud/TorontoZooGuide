export class ItinerarySettingsPreferenceDiff {
   static changesFromCheckboxes(statuses = [], checkboxEls = []) {
      const originalByStatus = new Map(
         statuses.map((entry) => [entry.status, Boolean(entry.isSuppressed)])
      );

      return checkboxEls.flatMap((checkboxEl) => {
         const status = checkboxEl?.dataset?.status;

         if (!status || !originalByStatus.has(status)) {
            return [];
         }

         const showWarning = Boolean(checkboxEl.checked);
         const originallyShown = !originalByStatus.get(status);

         if (showWarning === originallyShown) {
            return [];
         }

         return [{ status, showWarning }];
      });
   }
}
