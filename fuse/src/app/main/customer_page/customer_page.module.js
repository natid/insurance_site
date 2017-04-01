(function ()
{
    'use strict';

    angular
        .module('app.customer_page', [])
        .config(config);

    /** @ngInject */
    function config($stateProvider, $translatePartialLoaderProvider, msApiProvider, msNavigationServiceProvider)
    {
        // State
        $stateProvider
            .state('app.customer_page', {
                url    : '/customer_page/:id',
                views  : {
                    'content@app': {
                        templateUrl: 'app/main/customer_page/customer_page.html',
                        controller : 'CustomerPageController as vm'
                    }
                }
            });

        // Translation
        $translatePartialLoaderProvider.addPart('app/main/customer_page');

    }

})();