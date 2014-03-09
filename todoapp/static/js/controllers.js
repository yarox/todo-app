'use strict';

/* Controllers */

var todoAppControllers = angular.module('todoAppControllers', []);

todoAppControllers.controller('taskListController',
  ['$scope', '$http', 'ItemsDbService',

  function($scope, $http, ItemsDbService) {
    // $http.get('/items').success(function(data) {
    //   $scope.items = data.items;
    // });

    $scope.items = [];

    $scope.showItems = function() {
      ItemsDbService.getItems()
        .then(function(data) {
          $scope.items = data;
        }, function(e) {
          $window.alert(e);
        });
    };

    $scope.addItem = function(text, tags) {
      ItemsDbService.addItem(text, tags)
        .then(function() {
          $scope.showItems();

          $scope.itemText = "";
          $scope.itemTags = "";
        }, function(e) {
          $window.alert(e);
        });
    };

    $scope.deleteItem = function(id) {
      ItemsDbService.deleteItem(id)
        .then(function() {
          $scope.showItems();
        }, function(e) {
          $window.alert(e);
        });
    };

    function init() {
      ItemsDbService.openDb()
        .then(function() {
          $scope.showItems();
        });
    }

    init();

  }]);
