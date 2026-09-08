import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RowActionPresenter } from '../../../../scripts/itinerary/panel/rowActionPresenter.js';
import { ScheduleItemSearcher } from '../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';

test('Test_CanShowItineraryItemScheduleControls_TestHidesScheduleForPureTransportations_ExpectOk', () => {
   assert.equal(
      RowActionPresenter.canShowItineraryItemScheduleControls(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: false }
      ),
      false
   );
});

test('Test_CanShowItineraryItemScheduleControls_TestAllowsScheduleForAddedAsAttractionTransportations_ExpectOk', () => {
   assert.equal(
      RowActionPresenter.canShowItineraryItemScheduleControls(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: true }
      ),
      true
   );
});

test('Test_CanShowItineraryItemScheduleControls_TestAllowsScheduleForNonTransportationItems_ExpectOk', () => {
   assert.equal(
      RowActionPresenter.canShowItineraryItemScheduleControls(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda' }
      ),
      true
   );
   assert.equal(
      RowActionPresenter.canShowItineraryItemScheduleControls(
         ScheduleItemKind.ATTRACTION.itemType,
         { name: 'Conservation Carousel' }
      ),
      true
   );
});

test('Test_BuildUnscheduleRowProps_TestHidesUnscheduleForPureTransportations_ExpectOk', () => {
   assert.deepEqual(
      RowActionPresenter.buildUnscheduleRowProps(
         ScheduleItemKind.TRANSPORTATION.itemType,
         {
            name: 'Zoomobile',
            added_as_attraction: false,
            start_time: '2:30 PM',
            end_time: '3:00 PM',
         },
         () => {}
      ),
      {}
   );
});

test('Test_BuildUnscheduleRowProps_TestAllowsUnscheduleForAddedAsAttractionTransportations_ExpectOk', () => {
   const props = RowActionPresenter.buildUnscheduleRowProps(
      ScheduleItemKind.TRANSPORTATION.itemType,
      {
         name: 'Zoomobile',
         added_as_attraction: true,
         start_time: '2:30 PM',
         end_time: '3:00 PM',
      },
      () => {}
   );

   assert.equal(props.actionLabel, 'Unschedule');
   assert.equal(typeof props.onAction, 'function');
});

test('Test_BuildScheduleRowProps_TestUnscheduledAnimal_ExpectScheduleAction', () => {
   const requests = [];
   const props = RowActionPresenter.buildScheduleRowProps(
      ScheduleItemKind.ANIMAL.itemType,
      { species: 'Giant Panda', exhibit: 'Bamboo' },
      (request) => {
         requests.push(request);
      }
   );

   assert.equal(props.actionLabel, 'Schedule');
   props.onAction();
   assert.equal(requests[0].itemType, ScheduleItemKind.ANIMAL.itemType);
   assert.ok(requests[0].row);

   assert.deepEqual(
      RowActionPresenter.buildScheduleRowProps(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda', start_time: '1:00 PM', end_time: '1:30 PM' },
         () => {}
      ),
      {}
   );
   assert.deepEqual(
      RowActionPresenter.buildScheduleRowProps(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: false },
         () => {}
      ),
      {}
   );
   assert.deepEqual(
      RowActionPresenter.buildScheduleRowProps(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda' },
         null
      ),
      {}
   );
});

test('Test_BuildUnscheduleRowProps_TestGuardBranches_ExpectEmpty', () => {
   assert.deepEqual(
      RowActionPresenter.buildUnscheduleRowProps(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda', start_time: '1:00 PM', end_time: '1:30 PM' },
         null
      ),
      {}
   );
   assert.deepEqual(
      RowActionPresenter.buildUnscheduleRowProps(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda' },
         () => {}
      ),
      {}
   );

   const originalKey = ScheduleItemSearcher.getItineraryItemKey;
   ScheduleItemSearcher.getItineraryItemKey = () => '';
   try {
      assert.deepEqual(
         RowActionPresenter.buildUnscheduleRowProps(
            ScheduleItemKind.ANIMAL.itemType,
            { species: 'Giant Panda', start_time: '1:00 PM', end_time: '1:30 PM' },
            () => {}
         ),
         {}
      );
   } finally {
      ScheduleItemSearcher.getItineraryItemKey = originalKey;
   }
});

test('Test_BuildScheduleRowProps_TestMissingTaggedRow_ExpectEmpty', () => {
   const originalTag = ScheduleItemSearcher.tagScheduleItemRow;
   ScheduleItemSearcher.tagScheduleItemRow = () => null;

   try {
      assert.deepEqual(
         RowActionPresenter.buildScheduleRowProps(
            ScheduleItemKind.ANIMAL.itemType,
            { species: 'Giant Panda', exhibit: 'Bamboo' },
            () => {}
         ),
         {}
      );
   } finally {
      ScheduleItemSearcher.tagScheduleItemRow = originalTag;
   }
});

test('Test_BuildUnscheduleRowProps_TestOnAction_ExpectCallback', () => {
   const requests = [];
   const props = RowActionPresenter.buildUnscheduleRowProps(
      ScheduleItemKind.ANIMAL.itemType,
      {
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         start_time: '1:00 PM',
         end_time: '1:30 PM',
      },
      (request) => {
         requests.push(request);
      }
   );

   props.onAction();
   assert.deepEqual(requests, [{
      itemType: ScheduleItemKind.ANIMAL.itemType,
      key: 'Giant Panda||Bamboo',
   }]);
});

test('Test_BuildRemoveRowProps_TestPrimaryAndSecondary_ExpectLabels', () => {
   const requests = [];
   const secondary = RowActionPresenter.buildRemoveRowProps(
      ScheduleItemKind.ANIMAL.itemType,
      { species: 'Giant Panda', exhibit: 'Bamboo' },
      (request) => {
         requests.push(request);
      }
   );
   assert.equal(secondary.secondaryActionLabel, 'Remove');
   secondary.onSecondaryAction();

   const primary = RowActionPresenter.buildRemoveRowProps(
      ScheduleItemKind.ANIMAL.itemType,
      { species: 'Giant Panda', exhibit: 'Bamboo' },
      (request) => {
         requests.push(request);
      },
      { useSecondaryAction: false }
   );
   assert.equal(primary.actionLabel, 'Remove');
   primary.onAction();

   assert.deepEqual(
      RowActionPresenter.buildRemoveRowProps(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Giant Panda' },
         null
      ),
      {}
   );

   const originalKey = ScheduleItemSearcher.getItineraryItemKey;
   ScheduleItemSearcher.getItineraryItemKey = () => '';
   try {
      assert.deepEqual(
         RowActionPresenter.buildRemoveRowProps(
            ScheduleItemKind.ANIMAL.itemType,
            { species: 'Giant Panda', exhibit: 'Bamboo' },
            () => {}
         ),
         {}
      );
   } finally {
      ScheduleItemSearcher.getItineraryItemKey = originalKey;
   }

   assert.equal(requests.length, 2);
});

test('Test_BuildRowScheduleActionProps_TestCombined_ExpectMerged', () => {
   const props = RowActionPresenter.buildRowScheduleActionProps(
      ScheduleItemKind.ANIMAL.itemType,
      { species: 'Giant Panda', exhibit: 'Bamboo' },
      {
         onScheduleItem: () => {},
         onRemoveItem: () => {},
      }
   );

   assert.equal(props.actionLabel, 'Schedule');
   assert.equal(props.secondaryActionLabel, 'Remove');
});
