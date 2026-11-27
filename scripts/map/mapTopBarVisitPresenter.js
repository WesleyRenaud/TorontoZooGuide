import { ZooClockTimeHelper } from '../shared/zooClockTimeHelper.js';
import { Strings } from '../strings.js';
import { VisitDateFormatter } from '../visitDates/visitDateFormatter.js';

export class MapTopBarVisitPresenter {
   static latestVisit = Symbol('latestVisit');
   static LABEL_ID = 'mapDateLabel';
   static READOUT_WHEN_ID = 'mapDateReadoutWhen';

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
         readoutEl.setAttribute('aria-hidden', 'true');
         whenEl.textContent = '';
         MapTopBarVisitPresenter.labelInput(root, '');
         return;
      }

      root.classList.add('has-readout');
      readoutEl.hidden = false;
      readoutEl.removeAttribute('aria-hidden');
      whenEl.textContent = when;
      MapTopBarVisitPresenter.labelInput(root, when);
   }

   static labelInput(root, when) {
      const input = root.querySelector('input');

      if (!input) {
         return;
      }

      input.removeAttribute('aria-label');

      if (when) {
         input.setAttribute(
            'aria-labelledby',
            `${MapTopBarVisitPresenter.LABEL_ID} ${MapTopBarVisitPresenter.READOUT_WHEN_ID}`
         );
         return;
      }

      input.removeAttribute('aria-labelledby');
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
