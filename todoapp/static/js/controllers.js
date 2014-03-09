'use strict';

/* Controllers */

var todoAppControllers = angular.module('todoAppControllers', []);

todoAppControllers.controller('taskListController', ['$scope',
  function($scope) {
    $scope.items = [
      {'name': 'Some task',
       'tags': ['tag', 'other tag']},
      {'name': 'Another important task',
       'tags': ['important']},
      {'name': 'Some other task here',
       'tags': ['tag', 'not important', 'other']},
       {'name': 'Task with no tags',
        'tags': []}
    ];
  }]);
