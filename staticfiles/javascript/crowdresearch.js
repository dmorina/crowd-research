/**
 * Created by dmorina on 16/04/15.
 */

(function () {
    'use strict';

    angular
        .module('crowdresearch', [
        'crowdresearch.routes',
        'crowdresearch.user_management',
        'crowdresearch.config'
        ]);

    angular
        .module('crowdresearch.routes', ['ngRoute']);
    angular
        .module('crowdresearch.config', []);
})();


angular
  .module('crowdresearch')
  .run(run);

run.$inject = ['$http'];

/**
* @name run
* @desc Update xsrf $http headers to align with Django's defaults
*/
function run($http) {
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  $http.defaults.xsrfCookieName = 'csrftoken';
}