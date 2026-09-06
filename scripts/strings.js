import { Common } from './strings/common.js';
import { Console } from './strings/console.js';
import { GuestStatus } from './strings/guestStatus.js';
import { Itinerary } from './strings/itinerary.js';
import { Map } from './strings/map.js';
import { Pages } from './strings/pages.js';

export class Strings {
   static actions = Common.actions;
   static apiErrors = Console.apiErrors;
   static common = Common.common;
   static confirm = Console.confirm;
   static site = Pages.site;
   static animalsPage = Pages.animalsPage;
   static guestStatus = GuestStatus.guestStatus;
   static itinerary = Itinerary.itinerary;
   static help = Console.help;
   static loadErrors = Console.loadErrors;
   static labels = Common.labels;
   static likelihood = Common.likelihood;
   static map = Map.map;
   static placeholders = Console.placeholders;
   static textareas = Console.textareas;
   static panelTitles = Console.panelTitles;
   static search = Map.search;
   static schedule = Common.schedule;
   static status = Console.status;
   static tooltips = Map.tooltips;
   static updateTypes = Console.updateTypes;
   static entityLabels = Common.entityLabels;
   static entityPhrases = Common.entityPhrases;
   static validation = Console.validation;
   static viewingScopes = Console.viewingScopes;
}
