'use strict';

/* Filters */

angular.module('todoAppFilters', []).filter('join', function() {
  return function(input) {
    return input.join(', ');
  };
});
