import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleTimeConflictContentBuilder } from '../../../../scripts/itinerary/panel/scheduleTimeConflictContentBuilder.js';
import { ScheduleTimeConflictButtonStore } from '../../../../scripts/itinerary/panel/scheduleTimeConflictButtonStore.js';
import { ScheduleTimeConflictView } from '../../../../scripts/itinerary/panel/scheduleTimeConflictView.js';
import { RowPresenter } from '../../../../scripts/itinerary/panel/rowPresenter.js';
import { ScheduledOccurrenceSorter } from '../../../../scripts/itinerary/scheduledOccurrenceSorter.js';
import { ResultRenderer } from '../../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { ScheduleOverrideSelectionFragment } from '../../../../scripts/itinerary/wizard/scheduleOverrideSelectionFragment.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

const wildItem = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Mayan Temple',
   link: '/w',
};

const talkItem = {
   name: 'African Lion',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   location: 'Africa Savanna',
};

test('Test_RefreshConflictSelectionButtons_TestEntries_ExpectStoreApplied', () => {
   const originalState = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState;
   const originalApply = ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState;
   const applies = [];

   ScheduleTimeConflictButtonStore.getConflictSelectionButtonState = () => 'selected';
   ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState = (...args) => {
      applies.push(args);
   };

   try {
      const button = document.createElement('button');
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(
         [{ button, item: wildItem }],
         { items: [] }
      );
      assert.deepEqual(applies, [[button, 'selected']]);
   } finally {
      ScheduleTimeConflictButtonStore.getConflictSelectionButtonState = originalState;
      ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState = originalApply;
   }
});

test('Test_HandleConflictItemButtonClick_TestSelectedToggle_ExpectRefresh', () => {
   const originalSelected = ScheduleConflictChecker.isConflictItemSelected;
   const originalToggle = ScheduleConflictChecker.toggleConflictItemSelection;
   const originalRefresh = ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons;
   const toggles = [];
   const refreshes = [];

   ScheduleConflictChecker.isConflictItemSelected = () => true;
   ScheduleConflictChecker.toggleConflictItemSelection = (...args) => {
      toggles.push(args);
   };
   ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = (...args) => {
      refreshes.push(args);
   };

   try {
      ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick(
         { items: [wildItem] },
         wildItem,
         []
      );
      assert.equal(toggles.length, 1);
      assert.equal(refreshes.length, 1);
   } finally {
      ScheduleConflictChecker.isConflictItemSelected = originalSelected;
      ScheduleConflictChecker.toggleConflictItemSelection = originalToggle;
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = originalRefresh;
   }
});

test('Test_HandleConflictItemButtonClick_TestTrimOverride_ExpectConfirmation', () => {
   const originalSelected = ScheduleConflictChecker.isConflictItemSelected;
   const originalRequires = ScheduleConflictChecker.conflictItemRequiresTrimOverride;
   const originalShow = ScheduleOverrideSelectionFragment.showScheduleOverrideSelectionConfirmation;
   const originalToggle = ScheduleConflictChecker.toggleConflictItemSelection;
   const originalRefresh = ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons;
   let confirmHandler = null;
   const toggles = [];

   ScheduleConflictChecker.isConflictItemSelected = () => false;
   ScheduleConflictChecker.conflictItemRequiresTrimOverride = () => true;
   ScheduleOverrideSelectionFragment.showScheduleOverrideSelectionConfirmation = ({ onConfirm }) => {
      confirmHandler = onConfirm;
   };
   ScheduleConflictChecker.toggleConflictItemSelection = (...args) => {
      toggles.push(args);
   };
   ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = () => {};

   try {
      ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick({ items: [] }, talkItem, []);
      assert.equal(typeof confirmHandler, 'function');
      confirmHandler();
      assert.equal(toggles.length, 1);
   } finally {
      ScheduleConflictChecker.isConflictItemSelected = originalSelected;
      ScheduleConflictChecker.conflictItemRequiresTrimOverride = originalRequires;
      ScheduleOverrideSelectionFragment.showScheduleOverrideSelectionConfirmation = originalShow;
      ScheduleConflictChecker.toggleConflictItemSelection = originalToggle;
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = originalRefresh;
   }
});

test('Test_HandleConflictItemButtonClick_TestDirectSelect_ExpectToggle', () => {
   const originalSelected = ScheduleConflictChecker.isConflictItemSelected;
   const originalRequires = ScheduleConflictChecker.conflictItemRequiresTrimOverride;
   const originalToggle = ScheduleConflictChecker.toggleConflictItemSelection;
   const originalRefresh = ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons;
   const toggles = [];

   ScheduleConflictChecker.isConflictItemSelected = () => false;
   ScheduleConflictChecker.conflictItemRequiresTrimOverride = () => false;
   ScheduleConflictChecker.toggleConflictItemSelection = (...args) => {
      toggles.push(args);
   };
   ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = () => {};

   try {
      ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick({ items: [] }, wildItem, []);
      assert.equal(toggles.length, 1);
   } finally {
      ScheduleConflictChecker.isConflictItemSelected = originalSelected;
      ScheduleConflictChecker.conflictItemRequiresTrimOverride = originalRequires;
      ScheduleConflictChecker.toggleConflictItemSelection = originalToggle;
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = originalRefresh;
   }
});

test('Test_CreateScheduleConflictSubtitle_TestTalkAndWild_ExpectLabels', () => {
   const originalField = RowPresenter.buildScheduledTimeFieldLine;
   RowPresenter.buildScheduledTimeFieldLine = () => '1:00 PM – 1:30 PM';

   try {
      const talkSubtitle = ScheduleTimeConflictContentBuilder.createScheduleConflictSubtitle(talkItem);
      assert.match(talkSubtitle.textContent, new RegExp(Strings.labels.location));
      assert.match(talkSubtitle.textContent, /Africa Savanna/);

      const wildSubtitle = ScheduleTimeConflictContentBuilder.createScheduleConflictSubtitle(wildItem);
      assert.match(wildSubtitle.textContent, new RegExp(Strings.itinerary.selectors.meetingSpot));
      assert.match(wildSubtitle.textContent, /Mayan Temple/);
   } finally {
      RowPresenter.buildScheduledTimeFieldLine = originalField;
   }
});

test('Test_CreateWildEncounterConflictRowAndSection_TestIssues_ExpectRows', () => {
   const originalSort = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime;
   const originalImage = ScheduleTimeConflictView.buildConflictItemImageSrc;
   const originalContent = ResultRenderer.createSelectorRowContent;
   const originalText = ResultRenderer.createSelectorTextColumn;
   const originalCreateSelection = ScheduleConflictChecker.createConflictSelection;
   const originalRefresh = ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons;
   const clicks = [];

   ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = (items) => items;
   ScheduleTimeConflictView.buildConflictItemImageSrc = () => 'img.png';
   ResultRenderer.createSelectorTextColumn = ({ title }) => {
      const el = document.createElement('div');
      el.textContent = title;
      return el;
   };
   ResultRenderer.createSelectorRowContent = () => {
      const el = document.createElement('div');
      el.className = 'content';
      return el;
   };
   ScheduleConflictChecker.createConflictSelection = () => ({ items: [] });
   ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = () => {};

   const originalHandle = ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick;
   ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick = (...args) => {
      clicks.push(args);
   };

   try {
      const { section, conflictGroups } = ScheduleTimeConflictContentBuilder.createWildEncounterConflictSection([
         { items: [wildItem, talkItem] },
      ]);

      assert.equal(section.className, 'itin-save-issue-section');
      assert.equal(
         section.querySelector('.itin-save-issue-section-title')?.textContent,
         Strings.itinerary.confirmation.scheduleConflictsTitle
      );
      assert.equal(section.querySelectorAll('.itin-save-issue-conflict-row').length, 2);
      assert.equal(conflictGroups.length, 1);

      section.querySelector('.itin-save-issue-select-btn')?.click();
      assert.equal(clicks.length, 1);
   } finally {
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime = originalSort;
      ScheduleTimeConflictView.buildConflictItemImageSrc = originalImage;
      ResultRenderer.createSelectorRowContent = originalContent;
      ResultRenderer.createSelectorTextColumn = originalText;
      ScheduleConflictChecker.createConflictSelection = originalCreateSelection;
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = originalRefresh;
      ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick = originalHandle;
   }
});
