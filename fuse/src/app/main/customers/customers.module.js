(function ()
{
    'use strict';

    angular
        .module('app.customers', [])
        .config(config)
        .run(run);

    /** @ngInject */
    function config($stateProvider, $translatePartialLoaderProvider, msApiProvider, msNavigationServiceProvider)
    {
        // State
        $stateProvider
            .state('app.customers', {
                url    : '/customers',
                views  : {
                    'content@app': {
                        templateUrl: 'app/main/customers/customers.html',
                        controller : 'CustomersController as vm'
                    }
                }
            });

        // Translation
        $translatePartialLoaderProvider.addPart('app/main/customers');

        // // Api
        // msApiProvider.register('customers', ['app/data/customers/customers.json']);

        // Navigation
        msNavigationServiceProvider.saveItem('insurance', {
            title : 'ניהול',
            group : true,
            weight: 1
        });

        msNavigationServiceProvider.saveItem('insurance.customers', {
            title    : 'Customers',
            icon     : 'icon-tile-four',
            state    : 'app.customers',
            /*stateParams: {
                'param1': 'page'
             },*/
            translate: 'CUSTOMERS.TITLE',
            weight   : 1
        });
    }

    function run($http) {
        $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa("d@gmail.com:123"); // TODO remove after adding login
    }

})();