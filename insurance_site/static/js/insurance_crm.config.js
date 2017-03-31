(function () {
    'use strict';

    angular.module('insurance_crm.demo')
        .config(['$stateProvider', '$urlRouterProvider', config])
        .run(['$http', run]);

    function config($stateProvider, $urlRouterProvider) {

        var insuranceState = {
            name: 'insurance',
            url: '/insurance',
            templateUrl: 'https://d3p5dvqck1wwt9.cloudfront.net/html/insurance_crm.html',
            controller: 'InsuranceCrmController'
          }

          var loginState = {
            name: 'login',
            url: '/login',
            templateUrl: 'https://d3p5dvqck1wwt9.cloudfront.net/html/login2.html',
            controller: 'LoginController'
          }

          $stateProvider.state(insuranceState);
          $stateProvider.state(loginState);
          $urlRouterProvider.otherwise('/login');


//        $routeProvider
//            .when('/', {
//                templateUrl: '/static/html/insurance_crm.html',
//                controller: 'InsuranceCrmController',
//            })
//            .when('/login', {
//                templateUrl: '/static/html/login2.html',
//                controller: 'LoginController'
//            })
//            .otherwise('/');
    }

    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }

})();