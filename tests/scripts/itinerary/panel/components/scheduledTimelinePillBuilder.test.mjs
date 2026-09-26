import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledTimelinePillBuilder } from '../../../../../scripts/itinerary/panel/components/scheduledTimelinePillBuilder.js';
import { ItineraryPillView } from '../../../../../scripts/itinerary/panel/components/itineraryPillView.js';
import { OpenTimelineView } from '../../../../../scripts/itinerary/panel/components/openTimelineView.js';
import { ScheduledPillPresenter } from '../../../../../scripts/itinerary/panel/scheduledPillPresenter.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { RegionColors } from '../../../../../scripts/shared/regionColors.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ApplyScheduledPillRegionColors_TestItem_ExpectDelegate', () => {
   const originalResolve = RegionColors.resolveRegionColorSlugForScheduledItem;
   const originalApply = RegionColors.applyRegionColorsToElement;
   const regionSlug = 'africa';
   const applies = [];

   RegionColors.resolveRegionColorSlugForScheduledItem = () => regionSlug;
   RegionColors.applyRegionColorsToElement = (...args) => {
      applies.push(args);
   };

   try {
      const pill = document.createElement('div');
      ScheduledTimelinePillBuilder.applyScheduledPillRegionColors(pill, { region: 'Africa' });

      assert.equal(applies.length, 1);
      assert.equal(applies.at(Position.FIRST).at(Position.SECOND), regionSlug);
   } finally {
      RegionColors.resolveRegionColorSlugForScheduledItem = originalResolve;
      RegionColors.applyRegionColorsToElement = originalApply;
   }
});


test('Test_ApplyScheduledPillDuration_TestFiniteSlot_ExpectCssVar', () => {
   const durationMinutes = 45;
   const slotMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const pill = document.createElement('div');

   ScheduledTimelinePillBuilder.applyScheduledPillDuration(pill, durationMinutes, slotMinutes);

   assert.equal(
      pill.style['--itinerary-scheduled-pill-duration-fraction']
         ?? pill.attributes?.['style:--itinerary-scheduled-pill-duration-fraction'],
      String(durationMinutes / slotMinutes)
   );
   assert.equal(pill.getAttribute('data-duration-fraction'), String(durationMinutes / slotMinutes));
});


test('Test_ApplyScheduledPillDuration_TestZeroSlot_ExpectDefaultSlot', () => {
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const pill = document.createElement('div');

   ScheduledTimelinePillBuilder.applyScheduledPillDuration(pill, durationMinutes, 0);

   assert.equal(
      pill.getAttribute('data-duration-fraction'),
      String(durationMinutes / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES)
   );
});


test('Test_MakeScheduledPillArrowButton_TestPrevious_ExpectLabel', () => {
   const ariaLabel = 'Previous';
   const direction = 'previous';

   const previous = ScheduledTimelinePillBuilder.makeScheduledPillArrowButton(ariaLabel, direction);

   assert.equal(previous.textContent, '‹');
   assert.equal(previous.getAttribute('aria-label'), ariaLabel);
   assert.ok(previous.className.includes(direction));
});


test('Test_MakeScheduledPillArrowButton_TestNext_ExpectLabel', () => {
   const ariaLabel = 'Next';
   const direction = 'next';

   const next = ScheduledTimelinePillBuilder.makeScheduledPillArrowButton(ariaLabel, direction);

   assert.equal(next.textContent, '›');
   assert.equal(next.getAttribute('aria-label'), ariaLabel);
   assert.ok(next.className.includes(direction));
});


test('Test_ReplaceGroupedScheduledPillLabel_TestSuffix_ExpectCount', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const label = 'African Lion';
   const suffixCount = 2;

   OpenTimelineView.createPillLabelNode = (text) => {
      const el = document.createElement('span');
      el.className = 'label';
      el.textContent = text;
      return el;
   };

   try {
      const mount = document.createElement('div');
      mount.appendChild(document.createElement('span'));
      ScheduledTimelinePillBuilder.replaceGroupedScheduledPillLabel(mount, {
         label,
         suffixCount,
      });

      assert.equal(mount.querySelector('.label')?.textContent, label);
      assert.equal(
         mount.querySelector('.itinerary-day-scheduled-pill-count')?.textContent,
         Strings.itinerary.dayPlanner.scheduledPillMoreCount(suffixCount)
      );
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
   }
});


test('Test_ResolveWrappedGroupIndex_TestEmptyGroup_ExpectFirst', () => {
   const index = ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(Position.FIRST, 0);

   assert.equal(index, Position.FIRST);
});


test('Test_ResolveWrappedGroupIndex_TestNegative_ExpectLast', () => {
   const groupSize = 3;

   const index = ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(-1, groupSize);

   assert.equal(index, groupSize + Position.LAST);
});


test('Test_ResolveWrappedGroupIndex_TestPastEnd_ExpectFirst', () => {
   const groupSize = 3;

   const index = ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(groupSize, groupSize);

   assert.equal(index, Position.FIRST);
});


test('Test_ResolveWrappedGroupIndex_TestInRange_ExpectSame', () => {
   const groupIndex = Position.SECOND;
   const groupSize = 3;

   const index = ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(groupIndex, groupSize);

   assert.equal(index, groupIndex);
});


test('Test_BuildGroupedScheduledPill_TestNavigation_ExpectActiveIndex', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const originalExtended = ScheduledPillPresenter.isExtendedScheduledPill;
   const originalBuild = ItineraryPillView.buildPillMenuNodes;
   const originalBind = ItineraryPillView.bindPillMenu;
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const groupItems = [
      {
         label: lion,
         item: { species: lion },
         menuItems: [{ label: 'Unschedule', onAction: () => {} }],
      },
      {
         label: tiger,
         item: { species: tiger },
         menuItems: [],
      },
   ];
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES + 10;

   OpenTimelineView.createPillLabelNode = (label) => {
      const el = document.createElement('span');
      el.textContent = label;
      return el;
   };
   ScheduledPillPresenter.isExtendedScheduledPill = () => true;
   ItineraryPillView.buildPillMenuNodes = () => ({
      menu: document.createElement('div'),
      menuButton: document.createElement('button'),
      menuPanel: document.createElement('div'),
   });
   ItineraryPillView.bindPillMenu = () => {};

   try {
      const pill = ScheduledTimelinePillBuilder.buildGroupedScheduledPill(
         groupItems,
         durationMinutes,
         { menuAriaLabel: 'Menu' }
      );
      pill.querySelector('.itinerary-day-scheduled-pill-toggle--next')?.listeners.click({
         stopPropagation() {},
      });
      const afterNext = pill.getAttribute('data-active-group-index');
      pill.querySelector('.itinerary-day-scheduled-pill-toggle--previous')?.listeners.click({
         stopPropagation() {},
      });

      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--grouped'));
      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.equal(pill.getAttribute('data-group-size'), String(groupItems.length));
      assert.equal(afterNext, String(Position.SECOND));
      assert.equal(pill.getAttribute('data-active-group-index'), String(Position.FIRST));
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
      ScheduledPillPresenter.isExtendedScheduledPill = originalExtended;
      ItineraryPillView.buildPillMenuNodes = originalBuild;
      ItineraryPillView.bindPillMenu = originalBind;
   }
});


test('Test_BuildScheduledPillWithMenu_TestExtended_ExpectMenuBound', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const originalExtended = ScheduledPillPresenter.isExtendedScheduledPill;
   const originalBuild = ItineraryPillView.buildPillMenuNodes;
   const originalBind = ItineraryPillView.bindPillMenu;
   const binds = [];
   const label = 'African Lion';
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES + 10;

   OpenTimelineView.createPillLabelNode = (text) => {
      const el = document.createElement('span');
      el.textContent = text;
      return el;
   };
   ScheduledPillPresenter.isExtendedScheduledPill = () => true;
   ItineraryPillView.buildPillMenuNodes = () => ({
      menu: document.createElement('div'),
      menuButton: document.createElement('button'),
      menuPanel: document.createElement('div'),
   });
   ItineraryPillView.bindPillMenu = (...args) => {
      binds.push(args);
   };

   try {
      const pill = ScheduledTimelinePillBuilder.buildScheduledPillWithMenu(label, durationMinutes, {
         startTime: '10:00',
         endTime: '10:40',
         menuItems: [{ label: 'Unschedule', onAction: () => {} }],
         menuAriaLabel: 'Menu',
      });

      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--with-menu'));
      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.equal(binds.length, 1);
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
      ScheduledPillPresenter.isExtendedScheduledPill = originalExtended;
      ItineraryPillView.buildPillMenuNodes = originalBuild;
      ItineraryPillView.bindPillMenu = originalBind;
   }
});


test('Test_BuildScheduledPillWithoutMenu_TestCompact_ExpectSpan', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const originalExtended = ScheduledPillPresenter.isExtendedScheduledPill;
   const label = 'African Lion';
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES - 15;

   OpenTimelineView.createPillLabelNode = (text) => {
      const el = document.createElement('span');
      el.className = 'itinerary-day-scheduled-pill-label';
      el.textContent = text;
      return el;
   };
   ScheduledPillPresenter.isExtendedScheduledPill = () => false;

   try {
      const compact = ScheduledTimelinePillBuilder.buildScheduledPillWithoutMenu(label, durationMinutes, {
         startTime: '10:00',
         endTime: '10:15',
      });

      assert.equal(compact.tagName, 'span');
      assert.equal(compact.className, 'itinerary-day-scheduled-pill');
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
      ScheduledPillPresenter.isExtendedScheduledPill = originalExtended;
   }
});


test('Test_BuildScheduledPillWithoutMenu_TestExtended_ExpectHeader', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const originalExtended = ScheduledPillPresenter.isExtendedScheduledPill;
   const label = 'African Lion';
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES + 10;

   OpenTimelineView.createPillLabelNode = (text) => {
      const el = document.createElement('span');
      el.className = 'itinerary-day-scheduled-pill-label';
      el.textContent = text;
      return el;
   };
   ScheduledPillPresenter.isExtendedScheduledPill = () => true;

   try {
      const extended = ScheduledTimelinePillBuilder.buildScheduledPillWithoutMenu(label, durationMinutes, {
         startTime: '10:00',
         endTime: '10:40',
      });

      assert.ok(extended.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.ok(extended.querySelector('.itinerary-day-scheduled-pill-header'));
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
      ScheduledPillPresenter.isExtendedScheduledPill = originalExtended;
   }
});
