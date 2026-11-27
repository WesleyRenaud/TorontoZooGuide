import assert from 'node:assert/strict';
import test from 'node:test';

import { MapTopBarVisitPresenter } from '../../../scripts/map/mapTopBarVisitPresenter.js';
import { Strings } from '../../../scripts/strings.js';
import { VisitDateFormatter } from '../../../scripts/visitDates/visitDateFormatter.js';
import { ZooClockTimeHelper } from '../../../scripts/shared/zooClockTimeHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

const _TODAY_ISO = '2026-10-25';
const _LATER_ISO = '2026-10-27';
const _OPEN = '9:30 AM';
const _CLOSE = '6:00 PM';


function _hoursLabel(openTime, closeTime) {
   return Strings.format.timeRange(
      ZooClockTimeHelper.formatDisplay(openTime),
      ZooClockTimeHelper.formatDisplay(closeTime),
   );
}


function _hours() {
   return {
      openTime: _OPEN,
      closeTime: _CLOSE,
   };
}


function _visitLabel(isoDate, hours = null) {
   const dateLabel = VisitDateFormatter.formatShort(isoDate);

   if (!hours) {
      return dateLabel;
   }

   return Strings.map.visitDateAndHours(
      dateLabel,
      _hoursLabel(hours.openTime, hours.closeTime),
   );
}


function _labelledBy() {
   return (
      `${MapTopBarVisitPresenter.LABEL_ID} ${MapTopBarVisitPresenter.READOUT_WHEN_ID}`
   );
}


function _root() {
   const root = document.createElement('div');
   const label = document.createElement('label');
   label.id = MapTopBarVisitPresenter.LABEL_ID;
   label.htmlFor = 'mapDate';
   label.textContent = Strings.itinerary.selectors.visitDate;
   const input = document.createElement('input');
   input.id = 'mapDate';
   const readoutEl = document.createElement('span');
   readoutEl.className = 'map-date-readout';
   readoutEl.hidden = true;
   readoutEl.setAttribute('aria-hidden', 'true');
   const whenEl = document.createElement('span');
   whenEl.className = 'map-date-readout-when';
   whenEl.id = MapTopBarVisitPresenter.READOUT_WHEN_ID;
   readoutEl.append(whenEl);
   root.append(label, input, readoutEl);
   return root;
}


function _deps({ hoursByDate = {} } = {}) {
   return {
      getZooHours: async (isoDate) => hoursByDate[isoDate] ?? null,
   };
}


test('Test_BuildReadout_TestOpenDay_ExpectDateAndHours', () => {
   const hours = _hours();

   const readout = MapTopBarVisitPresenter.buildReadout({
      preset: Strings.map.presetIds.specificDay,
      isoDate: _TODAY_ISO,
      hours,
   });

   assert.equal(readout, _visitLabel(_TODAY_ISO, hours));
});


test('Test_BuildReadout_TestSeasonPreset_ExpectHidden', () => {
   const readout = MapTopBarVisitPresenter.buildReadout({
      preset: Strings.map.presetIds.summer,
      isoDate: _TODAY_ISO,
      hours: _hours(),
   });

   assert.equal(readout, null);
});


test('Test_BuildReadout_TestMissingHours_ExpectDateOnly', () => {
   const readout = MapTopBarVisitPresenter.buildReadout({
      preset: Strings.map.presetIds.specificDay,
      isoDate: _TODAY_ISO,
      hours: { openTime: _OPEN },
   });

   assert.equal(readout, _visitLabel(_TODAY_ISO));
});


test('Test_BuildReadout_TestInvalidDate_ExpectHidden', () => {
   const readout = MapTopBarVisitPresenter.buildReadout({
      preset: Strings.map.presetIds.specificDay,
      isoDate: 'tomorrow',
      hours: _hours(),
   });

   assert.equal(readout, null);
});


test('Test_BuildReadout_TestUnpaddedDate_ExpectHidden', () => {
   const readout = MapTopBarVisitPresenter.buildReadout({
      preset: Strings.map.presetIds.specificDay,
      isoDate: '2026-10-5',
      hours: _hours(),
   });

   assert.equal(readout, null);
});


test('Test_Apply_TestReadout_ExpectVisibleText', () => {
   const root = _root();
   const readout = _visitLabel(_TODAY_ISO, _hours());

   MapTopBarVisitPresenter.apply(root, readout);

   assert.equal(root.classList.contains('has-readout'), true);
   assert.equal(root.querySelector('.map-date-readout').hidden, false);
   assert.equal(root.querySelector('.map-date-readout-when').textContent, readout);
   assert.equal(root.querySelector('.map-date-readout').hasAttribute('aria-hidden'), false);
   assert.equal(root.querySelector('input').hasAttribute('aria-label'), false);
   assert.equal(root.querySelector('input').getAttribute('aria-labelledby'), _labelledBy());
});


test('Test_Apply_TestEmpty_ExpectHidden', () => {
   const root = _root();
   MapTopBarVisitPresenter.apply(root, _visitLabel(_TODAY_ISO, _hours()));

   MapTopBarVisitPresenter.apply(root, null);

   assert.equal(root.classList.contains('has-readout'), false);
   assert.equal(root.querySelector('.map-date-readout').hidden, true);
   assert.equal(root.querySelector('.map-date-readout').getAttribute('aria-hidden'), 'true');
   assert.equal(root.querySelector('.map-date-readout-when').textContent, '');
   assert.equal(root.querySelector('input').hasAttribute('aria-label'), false);
   assert.equal(root.querySelector('input').hasAttribute('aria-labelledby'), false);
});


test('Test_Apply_TestReadout_ExpectNameIncludesLabelAndDate', () => {
   const root = _root();
   const readout = _visitLabel(_TODAY_ISO, _hours());

   MapTopBarVisitPresenter.apply(root, readout);

   const input = root.querySelector('input');
   const labelledBy = input.getAttribute('aria-labelledby').split(/\s+/);
   const name = labelledBy
      .map((id) => root.querySelector(`#${id}`)?.textContent ?? '')
      .join(' ')
      .replace(/\s+/g, ' ')
      .trim();

   assert.equal(name, `${Strings.itinerary.selectors.visitDate} ${readout}`);
});


test('Test_Apply_TestMissingInput_ExpectReadout', () => {
   const root = document.createElement('div');
   const readoutEl = document.createElement('span');
   readoutEl.className = 'map-date-readout';
   const whenEl = document.createElement('span');
   whenEl.className = 'map-date-readout-when';
   readoutEl.append(whenEl);
   root.append(readoutEl);

   MapTopBarVisitPresenter.apply(root, _visitLabel(_TODAY_ISO));

   assert.equal(root.classList.contains('has-readout'), true);
   assert.equal(whenEl.textContent, _visitLabel(_TODAY_ISO));
});


test('Test_Apply_TestMissingRoot_ExpectNoThrow', () => {
   const apply = () => MapTopBarVisitPresenter.apply(null, null);

   assert.doesNotThrow(apply);
});


test('Test_Apply_TestMissingChildren_ExpectUnchanged', () => {
   const root = document.createElement('div');

   MapTopBarVisitPresenter.apply(root, _visitLabel(_TODAY_ISO));

   assert.equal(root.classList.contains('has-readout'), false);
});


test('Test_Refresh_TestSpecificDay_ExpectHoursForThatDay', async () => {
   const root = _root();
   const hours = _hours();
   const fetched = [];
   const deps = _deps({
      hoursByDate: { [_TODAY_ISO]: hours },
   });
   const getZooHours = deps.getZooHours;
   deps.getZooHours = async (isoDate) => {
      fetched.push(isoDate);
      return getZooHours(isoDate);
   };

   await MapTopBarVisitPresenter.refresh(root, {
      preset: Strings.map.presetIds.specificDay,
      isoDate: _TODAY_ISO,
      ...deps,
   });

   assert.deepEqual(fetched, [_TODAY_ISO]);
   assert.equal(
      root.querySelector('.map-date-readout-when').textContent,
      _visitLabel(_TODAY_ISO, hours),
   );
});


test('Test_Refresh_TestSeasonPreset_ExpectHiddenWithoutFetch', async () => {
   const root = _root();
   let calls = 0;
   const deps = _deps();
   deps.getZooHours = async () => {
      calls += 1;
      return _hours();
   };

   await MapTopBarVisitPresenter.refresh(root, {
      preset: Strings.map.presetIds.summer,
      isoDate: _TODAY_ISO,
      ...deps,
   });

   assert.equal(calls, 0);
   assert.equal(root.classList.contains('has-readout'), false);
   assert.equal(root.querySelector('.map-date-readout').hidden, true);
});


test('Test_Refresh_TestHoursFailure_ExpectDateOnly', async () => {
   const root = _root();
   const deps = _deps();
   deps.getZooHours = async () => {
      throw new Error('hours unavailable');
   };

   await MapTopBarVisitPresenter.refresh(root, {
      preset: Strings.map.presetIds.specificDay,
      isoDate: _TODAY_ISO,
      ...deps,
   });

   assert.equal(
      root.querySelector('.map-date-readout-when').textContent,
      _visitLabel(_TODAY_ISO),
   );
});


test('Test_Refresh_TestStaleRequest_ExpectLatestDay', async () => {
   const root = _root();
   let releaseFirst;
   const firstHours = new Promise((resolve) => {
      releaseFirst = resolve;
   });
   const deps = _deps({
      hoursByDate: {
         [_LATER_ISO]: { openTime: '10:00 AM', closeTime: '5:00 PM' },
      },
   });
   const firstDeps = {
      ...deps,
      getZooHours: () => firstHours,
   };

   const first = MapTopBarVisitPresenter.refresh(root, {
      preset: Strings.map.presetIds.specificDay,
      isoDate: _TODAY_ISO,
      ...firstDeps,
   });
   await MapTopBarVisitPresenter.refresh(root, {
      preset: Strings.map.presetIds.specificDay,
      isoDate: _LATER_ISO,
      ...deps,
   });
   releaseFirst(_hours());
   await first;

   assert.equal(
      root.querySelector('.map-date-readout-when').textContent,
      _visitLabel(_LATER_ISO, { openTime: '10:00 AM', closeTime: '5:00 PM' }),
   );
});


test('Test_Refresh_TestMissingRoot_ExpectNoThrow', async () => {
   const refresh = () => MapTopBarVisitPresenter.refresh(null, {
      preset: Strings.map.presetIds.specificDay,
      isoDate: _TODAY_ISO,
      ..._deps(),
   });

   await assert.doesNotReject(refresh);
});


test('Test_Refresh_TestMissingDate_ExpectHidden', async () => {
   const root = _root();
   let calls = 0;
   const deps = _deps();
   deps.getZooHours = async () => {
      calls += 1;
      return _hours();
   };

   await MapTopBarVisitPresenter.refresh(root, {
      preset: Strings.map.presetIds.specificDay,
      isoDate: '',
      ...deps,
   });

   assert.equal(calls, 0);
   assert.equal(root.classList.contains('has-readout'), false);
});
