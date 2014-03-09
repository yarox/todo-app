var todoAppServices = angular.module('todoAppServices', ['ngResource']);

todoAppServices.factory('ItemsDbService', ['$window', '$q',
  function($window, $q){
    var indexedDB = $window.indexedDB;
    var db = null;

    var DB_NAME = 'todo-db';
    var DB_VERSION = 1;
    var DB_STORE_NAME = 'todo-store';


    var getObjectStore = function(storeName, mode) {
      var trans = db.transaction([storeName], mode);
      return trans.objectStore(storeName);
    };

    var openDb = function() {
      var deferred = $q.defer();
      var request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onupgradeneeded = function(e) {
        var db = e.target.result;

        if (db.objectStoreNames.contains(DB_STORE_NAME)) {
          db.deleteObjectStore(DB_STORE_NAME);
        }

        var store = db.createObjectStore(DB_STORE_NAME, {
          autoIncrement: true
        });

        e.target.transaction.onerror = indexedDB.onerror;
      };

      request.onsuccess = function(e) {
        console.log('open success');

        db = e.target.result;
        deferred.resolve();
      };

      request.onerror = function(e) {
        var msg = 'open error';

        console.log(msg, e);
        deferred.reject(msg);
      };

      return deferred.promise;
    };

    var getItems = function() {
      var deferred = $q.defer();
      var elements = [];

      var store = getObjectStore(DB_STORE_NAME, 'readonly');
      var cursorRequest = store.openCursor();

      cursorRequest.onsuccess = function(e) {
        var result = event.target.result;

        if (result) {
          elements.push({
            'value': result.value,
            'key': result.primaryKey
          });

          result.continue();
        } else {
          console.log('getItems success');
          deferred.resolve(elements);
        }
      };

      cursorRequest.onerror = function(e) {
        var msg = 'getItems error';

        console.log(msg, e);
        deferred.reject(msg);
      };

      return deferred.promise;
    };

    var deleteItem = function(id) {
      var deferred = $q.defer();

      var store = getObjectStore(DB_STORE_NAME, 'readwrite');
      var request = store.delete(id);

      request.onsuccess = function(e) {
        console.log('deleteItem success');
        deferred.resolve();
      };

      request.onerror = function(e) {
        var msg = 'deleteItem error';

        console.log(msg, e);
        deferred.reject(msg);
      };

      return deferred.promise;
    };

    var addItem = function(text, tags) {
      var deferred = $q.defer();
      var data = {
        'text': text || '<empty>',
        'tags': tags ? tags.replace(/\s/g, '').split(',') : [],
        'timestamp': new Date().getTime() / 1000
      };

      var store = getObjectStore(DB_STORE_NAME, 'readwrite');
      var request = store.put(data);

      request.onsuccess = function(e) {
        console.log('addItem success');
        deferred.resolve();
      };

      request.onerror = function(e) {
        var msg = 'addItem error';

        console.log(msg, e);
        deferred.reject(msg);
      };

      return deferred.promise;
    };

    return {
      openDb: openDb,
      getItems: getItems,
      addItem: addItem,
      deleteItem: deleteItem
    };
  }]);
