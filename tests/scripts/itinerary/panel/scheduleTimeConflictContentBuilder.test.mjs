import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleTimeConflictButtonStore } from '../../../../scripts/itinerary/panel/scheduleTimeConflictButtonStore.js';
import { ScheduleTimeConflictContentBuilder } from '../../../../scripts/itinerary/panel/scheduleTimeConflictContentBuilder.js';
import { ScheduleTimeConflictView } from '../../../../scripts/itinerary/panel/scheduleTimeConflictView.js';
import { RowPresenter } from '../../../../scripts/itinerary/panel/rowPresenter.js';
import { ScheduledOccurrenceSorter } from '../../../../scripts/itinerary/scheduledOccurrenceSorter.js';
import { ResultRenderer } from '../../../../scripts/itinerary/selectors/base/resultRenderer.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { ScheduleOverrideSelectionFragment } from '../../../../scripts/itinerary/wizard/scheduleOverrideSelectionFragment.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

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

const selectedState = 'selected';

installDomTestHooks();


test('Test_RefreshConflictSelectionButtons_TestEntries_ExpectStoreApplied', () => {
   const originalState = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState;
   const originalApply = ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState;
   const applies = [];
   ScheduleTimeConflictButtonStore.getConflictSelectionButtonState = () => selectedState;
   ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState = (...args) => {
      applies.push(args);
   };
   const button = document.createElement('button');

   try {
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(
         [{ button, item: wildItem }],
         { items: [] }
      );

      assert.deepEqual(applies, [[button, selectedState]]);
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

      assert.equal(toggles.length, Position.SECOND);
      assert.equal(refreshes.length, Position.SECOND);
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

      assert.equal(toggles.length, Position.SECOND);
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

      assert.equal(toggles.length, Position.SECOND);
   } finally {
      ScheduleConflictChecker.isConflictItemSelected = originalSelected;
      ScheduleConflictChecker.conflictItemRequiresTrimOverride = originalRequires;
      ScheduleConflictChecker.toggleConflictItemSelection = originalToggle;
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons = originalRefresh;
   }
});


test('Test_CreateScheduleConflictSubtitle_TestTalk_ExpectLocation', () => {
   const originalField = RowPresenter.buildScheduledTimeFieldLine;
   const scheduledTime = '1:00 PM – 1:30 PM';
   RowPresenter.buildScheduledTimeFieldLine = () => scheduledTime;

   try {
      const talkSubtitle = ScheduleTimeConflictContentBuilder.createScheduleConflictSubtitle(talkItem);

      assert.match(talkSubtitle.textContent, new RegExp(Strings.labels.location));
      assert.match(talkSubtitle.textContent, new RegExp(talkItem.location));
   } finally {
      RowPresenter.buildScheduledTimeFieldLine = originalField;
   }
});


test('Test_CreateScheduleConflictSubtitle_TestWildEncounter_ExpectMeetingSpot', () => {
   const originalField = RowPresenter.buildScheduledTimeFieldLine;
   const scheduledTime = '1:00 PM – 1:30 PM';
   RowPresenter.buildScheduledTimeFieldLine = () => scheduledTime;

   try {
      const wildSubtitle = ScheduleTimeConflictContentBuilder.createScheduleConflictSubtitle(wildItem);

      assert.match(wildSubtitle.textContent, new RegExp(Strings.itinerary.selectors.meetingSpot));
      assert.match(wildSubtitle.textContent, new RegExp(wildItem.meeting_spot));
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
   const originalHandle = ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick;
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
   ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick = (...args) => {
      clicks.push(args);
   };

   try {
      const { section, conflictGroups } = ScheduleTimeConflictContentBuilder.createWildEncounterConflictSection([
         { items: [wildItem, talkItem] },
      ]);
      const title = section.querySelector('.itin-save-issue-section-title')?.textContent;
      const rows = section.querySelectorAll('.itin-save-issue-conflict-row');

      assert.equal(section.className, 'itin-save-issue-section');
      assert.equal(title, Strings.itinerary.confirmation.scheduleConflictsTitle);
      assert.equal(rows.length, Position.THIRD);
      assert.equal(conflictGroups.length, Position.SECOND);

      section.querySelector('.itin-save-issue-select-btn')?.click();

      assert.equal(clicks.length, Position.SECOND);
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
