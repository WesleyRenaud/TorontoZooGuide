import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFragment } from '../../../scripts/updates/exploreFragment.js';
import { ExploreUpdatesHelper } from '../../../scripts/updates/exploreUpdatesHelper.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';


test('Test_BuildDatePayload_TestContext_ExpectFields', () => {
   const month = 9;
   const day = 8;
   const year = 2026;
   const context = { month, day, year };

   const payload = ExploreUpdatesHelper.buildDatePayload(context);

   assert.deepEqual(payload, { month, day, year });
});


test('Test_BuildTodayDatePayload_TestFixedDate_ExpectLocalCalendarFields', () => {
   const year = 2026;
   const monthIndex = 8;
   const day = 10;
   const today = new Date(year, monthIndex, day, 12, 0, 0);

   const payload = ExploreUpdatesHelper.buildTodayDatePayload(today);

   assert.deepEqual(payload, {
      month: VisitDateValidator.getMonth(VisitDateValidator.toISODate(today)),
      day: VisitDateValidator.getDay(VisitDateValidator.toISODate(today)),
      year: VisitDateValidator.getYear(VisitDateValidator.toISODate(today)),
   });
});


test('Test_ResolveActiveTab_TestEmptyUpdates_ExpectEvents', () => {
   const updates = [];
   const events = [{ id: 1 }];
   const activeTab = ExploreFragment.EXPLORE_TAB.UPDATES;

   const tab = ExploreUpdatesHelper.resolveActiveTab(activeTab, updates, events);

   assert.equal(tab, ExploreFragment.EXPLORE_TAB.EVENTS);
});


test('Test_ResolveActiveTab_TestEmptyEvents_ExpectUpdates', () => {
   const updates = [{ id: 1 }];
   const events = [];
   const activeTab = ExploreFragment.EXPLORE_TAB.EVENTS;

   const tab = ExploreUpdatesHelper.resolveActiveTab(activeTab, updates, events);

   assert.equal(tab, ExploreFragment.EXPLORE_TAB.UPDATES);
});


test('Test_ResolveActiveTab_TestUpdatesAvailable_ExpectSameTab', () => {
   const updates = [{ id: 1 }];
   const events = [];
   const activeTab = ExploreFragment.EXPLORE_TAB.UPDATES;

   const tab = ExploreUpdatesHelper.resolveActiveTab(activeTab, updates, events);

   assert.equal(tab, activeTab);
});
