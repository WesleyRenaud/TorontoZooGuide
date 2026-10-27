import { ZooClockTimeHelper } from '../shared/zooClockTimeHelper.js';
import { Strings } from '../strings.js';
import { VisitDateFormatter } from '../visitDates/visitDateFormatter.js';

export class MapTopBarVisitPresenter {
   static latestVisit = Symbol('latestVisit');

   static buildReadout({
      preset,
      isoDate,
      hours,
   } = {}) {
      if (preset !== Strings.map.presetIds.specificDay) {
         return null;
      }

      const dateLabel = VisitDateFormatter.formatShort(isoDate);
      const open = ZooClockTimeHelper.formatDisplay(hours?.openTime);
      const close = ZooClockTimeHelper.formatDisplay(hours?.closeTime);

      if (!dateLabel || !open || !close) {
         return dateLabel || null;
      }

      return Strings.map.visitDateAndHours(dateLabel, Strings.format.timeRange(open, close));
   }

   static apply(root, when) {
      if (!root) {
         return;
      }

      const readoutEl = root.querySelector('.map-date-readout');
      const whenEl = root.querySelector('.map-date-readout-when');

      if (!readoutEl || !whenEl) {
         return;
      }

      if (!when) {
         root.classList.remove('has-readout');
         readoutEl.hidden = true;
         whenEl.textContent = '';
         MapTopBarVisitPresenter.labelInput(root, '');
         return;
      }

      root.classList.add('has-readout');
      readoutEl.hidden = false;
      whenEl.textContent = when;
      MapTopBarVisitPresenter.labelInput(root, when);
   }

   static labelInput(root, when) {
      const input = root.querySelector('input');

      if (!input) {
         return;
      }

      if (when) {
         input.setAttribute('aria-label', when);
         return;
      }

      input.removeAttribute('aria-label');
   }

   static async loadHours(getZooHours, isoDate) {
      try {
         return await getZooHours(isoDate);
      }
      catch {
         return null;
      }
   }

   static async refresh(root, {
      preset,
      isoDate,
      getZooHours,
   } = {}) {
      if (!root) {
         return;
      }

      const visit = {};
      root[MapTopBarVisitPresenter.latestVisit] = visit;
      const show = (hours) => {
         MapTopBarVisitPresenter.apply(root, MapTopBarVisitPresenter.buildReadout({
            preset,
            isoDate,
            hours,
         }));
      };

      if (preset !== Strings.map.presetIds.specificDay || !isoDate) {
         show(null);
         return;
      }

      show(null);
      const hours = await MapTopBarVisitPresenter.loadHours(getZooHours, isoDate);

      if (root[MapTopBarVisitPresenter.latestVisit] !== visit) {
         return;
      }

      show(hours);
   }
}
