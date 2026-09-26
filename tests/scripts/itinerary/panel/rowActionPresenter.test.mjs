import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RowActionPresenter } from '../../../../scripts/itinerary/panel/rowActionPresenter.js';
import { ScheduleItemSearcher } from '../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { ScheduleItemKeySeparator } from '../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';


test('Test_CanShowItineraryItemScheduleControls_TestPureTransportation_ExpectFalse', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const item = { name: 'Zoomobile', added_as_attraction: false };

   const canShow = RowActionPresenter.canShowItineraryItemScheduleControls(itemType, item);

   assert.equal(canShow, false);
});


test('Test_CanShowItineraryItemScheduleControls_TestAttractionTransportation_ExpectTrue', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const item = { name: 'Zoomobile', added_as_attraction: true };

   const canShow = RowActionPresenter.canShowItineraryItemScheduleControls(itemType, item);

   assert.equal(canShow, true);
});


test('Test_CanShowItineraryItemScheduleControls_TestAnimal_ExpectTrue', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda' };

   const canShow = RowActionPresenter.canShowItineraryItemScheduleControls(itemType, item);

   assert.equal(canShow, true);
});


test('Test_CanShowItineraryItemScheduleControls_TestAttraction_ExpectTrue', () => {
   const itemType = ScheduleItemKind.ATTRACTION.itemType;
   const item = { name: 'Conservation Carousel' };

   const canShow = RowActionPresenter.canShowItineraryItemScheduleControls(itemType, item);

   assert.equal(canShow, true);
});


test('Test_BuildUnscheduleRowProps_TestPureTransportation_ExpectEmpty', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const item = {
      name: 'Zoomobile',
      added_as_attraction: false,
      start_time: '2:30 PM',
      end_time: '3:00 PM',
   };

   const props = RowActionPresenter.buildUnscheduleRowProps(itemType, item, () => {});

   assert.deepEqual(props, {});
});


test('Test_BuildUnscheduleRowProps_TestAttractionTransportation_ExpectUnschedule', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const item = {
      name: 'Zoomobile',
      added_as_attraction: true,
      start_time: '2:30 PM',
      end_time: '3:00 PM',
   };

   const props = RowActionPresenter.buildUnscheduleRowProps(itemType, item, () => {});

   assert.equal(props.actionLabel, 'Unschedule');
   assert.equal(typeof props.onAction, 'function');
});


test('Test_BuildScheduleRowProps_TestUnscheduledAnimal_ExpectScheduleAction', () => {
   const requests = [];
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', exhibit: 'Bamboo' };

   const props = RowActionPresenter.buildScheduleRowProps(
      itemType,
      item,
      (request) => {
         requests.push(request);
      }
   );
   props.onAction();

   const request = requests.at(Position.FIRST);

   assert.equal(props.actionLabel, 'Schedule');
   assert.equal(request.itemType, itemType);
   assert.ok(request.row);
});


test('Test_BuildScheduleRowProps_TestScheduledAnimal_ExpectEmpty', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', start_time: '1:00 PM', end_time: '1:30 PM' };

   const props = RowActionPresenter.buildScheduleRowProps(itemType, item, () => {});

   assert.deepEqual(props, {});
});


test('Test_BuildScheduleRowProps_TestPureTransportation_ExpectEmpty', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const item = { name: 'Zoomobile', added_as_attraction: false };

   const props = RowActionPresenter.buildScheduleRowProps(itemType, item, () => {});

   assert.deepEqual(props, {});
});


test('Test_BuildScheduleRowProps_TestMissingCallback_ExpectEmpty', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda' };

   const props = RowActionPresenter.buildScheduleRowProps(itemType, item, null);

   assert.deepEqual(props, {});
});


test('Test_BuildUnscheduleRowProps_TestMissingCallback_ExpectEmpty', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', start_time: '1:00 PM', end_time: '1:30 PM' };

   const props = RowActionPresenter.buildUnscheduleRowProps(itemType, item, null);

   assert.deepEqual(props, {});
});


test('Test_BuildUnscheduleRowProps_TestUnscheduledAnimal_ExpectEmpty', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda' };

   const props = RowActionPresenter.buildUnscheduleRowProps(itemType, item, () => {});

   assert.deepEqual(props, {});
});


test('Test_BuildUnscheduleRowProps_TestMissingKey_ExpectEmpty', () => {
   const originalKey = ScheduleItemSearcher.getItineraryItemKey;
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', start_time: '1:00 PM', end_time: '1:30 PM' };
   ScheduleItemSearcher.getItineraryItemKey = () => '';

   try {
      const props = RowActionPresenter.buildUnscheduleRowProps(itemType, item, () => {});

      assert.deepEqual(props, {});
   } finally {
      ScheduleItemSearcher.getItineraryItemKey = originalKey;
   }
});


test('Test_BuildScheduleRowProps_TestMissingTaggedRow_ExpectEmpty', () => {
   const originalTag = ScheduleItemSearcher.tagScheduleItemRow;
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', exhibit: 'Bamboo' };
   ScheduleItemSearcher.tagScheduleItemRow = () => null;

   try {
      const props = RowActionPresenter.buildScheduleRowProps(itemType, item, () => {});

      assert.deepEqual(props, {});
   } finally {
      ScheduleItemSearcher.tagScheduleItemRow = originalTag;
   }
});


test('Test_BuildUnscheduleRowProps_TestOnAction_ExpectCallback', () => {
   const requests = [];
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const species = 'Giant Panda';
   const exhibit = 'Bamboo';
   const item = {
      species,
      exhibit,
      start_time: '1:00 PM',
      end_time: '1:30 PM',
   };

   const props = RowActionPresenter.buildUnscheduleRowProps(
      itemType,
      item,
      (request) => {
         requests.push(request);
      }
   );
   props.onAction();

   assert.deepEqual(requests, [{
      itemType,
      key: [species, exhibit].join(ScheduleItemKeySeparator.VALUE),
   }]);
});


test('Test_BuildRemoveRowProps_TestSecondary_ExpectRemove', () => {
   const requests = [];
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', exhibit: 'Bamboo' };

   const props = RowActionPresenter.buildRemoveRowProps(
      itemType,
      item,
      (request) => {
         requests.push(request);
      }
   );
   props.onSecondaryAction();

   assert.equal(props.secondaryActionLabel, 'Remove');
   assert.equal(requests.length, 1);
});


test('Test_BuildRemoveRowProps_TestPrimary_ExpectRemove', () => {
   const requests = [];
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', exhibit: 'Bamboo' };

   const props = RowActionPresenter.buildRemoveRowProps(
      itemType,
      item,
      (request) => {
         requests.push(request);
      },
      { useSecondaryAction: false }
   );
   props.onAction();

   assert.equal(props.actionLabel, 'Remove');
   assert.equal(requests.length, 1);
});


test('Test_BuildRemoveRowProps_TestMissingCallback_ExpectEmpty', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda' };

   const props = RowActionPresenter.buildRemoveRowProps(itemType, item, null);

   assert.deepEqual(props, {});
});


test('Test_BuildRemoveRowProps_TestMissingKey_ExpectEmpty', () => {
   const originalKey = ScheduleItemSearcher.getItineraryItemKey;
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', exhibit: 'Bamboo' };
   ScheduleItemSearcher.getItineraryItemKey = () => '';

   try {
      const props = RowActionPresenter.buildRemoveRowProps(itemType, item, () => {});

      assert.deepEqual(props, {});
   } finally {
      ScheduleItemSearcher.getItineraryItemKey = originalKey;
   }
});


test('Test_BuildRowScheduleActionProps_TestCombined_ExpectMerged', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = { species: 'Giant Panda', exhibit: 'Bamboo' };

   const props = RowActionPresenter.buildRowScheduleActionProps(
      itemType,
      item,
      {
         onScheduleItem: () => {},
         onRemoveItem: () => {},
      }
   );

   assert.equal(props.actionLabel, 'Schedule');
   assert.equal(props.secondaryActionLabel, 'Remove');
});


test('Test_BuildRowScheduleActionProps_TestTransportationOnlyAnimal_ExpectNoActions', () => {
   const itemType = ScheduleItemKind.ANIMAL.itemType;
   const item = {
      species: 'Masai Giraffe',
      exhibit: 'Africa Savanna',
      added_by_transportation: true,
   };

   const props = RowActionPresenter.buildRowScheduleActionProps(
      itemType,
      item,
      {
         onScheduleItem: () => {},
         onRemoveItem: () => {},
      }
   );

   assert.deepEqual(props, {});
});
