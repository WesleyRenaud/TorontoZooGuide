import { ScheduleItemResultsBuilder } from './scheduleItemResultsBuilder.js';

export class ScheduleItemResults {
   static renderScheduleItemSearchResults({
      resultsEl,
      rows = [],
      emptyText = '',
      getId,
      selectedRowId = '',
      renderRowLeft,
      onSelectRow,
   } = {}) {
      if (!resultsEl) {
         return;
      }

      if (!Array.isArray(rows) || rows.length === 0) {
         resultsEl.replaceChildren(ScheduleItemResultsBuilder.createEmptyState(emptyText));
         return;
      }

      const fragment = document.createDocumentFragment();

      rows.forEach((row) => {
         fragment.appendChild(
            ScheduleItemResultsBuilder.createResultRow({
               row,
               getId,
               selectedRowId,
               renderRowLeft,
               onSelectRow,
            })
         );
      });

      resultsEl.replaceChildren(fragment);
   }
}
